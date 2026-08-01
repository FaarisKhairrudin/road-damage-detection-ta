"""
Custom modules reconstructing TWO road-damage-detection YOLOv8 variants for
use as comparison baselines, since neither paper released architecture code:

  1. YOLOv8-PD — Zeng, J. & Zhong, H., Sci Rep 14, 12052 (2024).
     BoT + LSKA + C2fGhost + LSCDHead.  (see section below)
  2. YOLO-RD  — Wang, W. et al., Sensors 25, 1442 (2025).
     SOM + ARM + WTHead.               (see section further below)

Both share one `patch_ultralytics()` call and one parse_model patch (all
model classes from both papers are registered together), so a single yaml
using any mix of the modules below will work. Use a separate yaml per model
(yolov8-pd.yaml / yolo-rd.yaml) — same custom_modules.py for both.

This is a best-effort reproduction from each paper's figures/equations, not
official code — exact parameter counts / mAP will differ from the papers.
Validate against your own dataset before treating either as a strict
baseline, and see each yaml's header comment / the README for the specific
interpretation choices made where a paper's description was ambiguous.

Tested against ultralytics==8.4.108 / torchvision==0.28.0. If you're on
different versions and `patch_ultralytics()` raises an AttributeError, see
the note at the bottom of this file.
"""

import math
import torch
import torch.nn as nn

import ultralytics.nn.tasks as tasks
from ultralytics.nn.tasks import *  # noqa: F401,F403 (pulls in Conv, C2f, Detect, GhostConv, GhostBottleneck,
                                     # LOGGER, make_divisible, colorstr, etc. — reused below and needed inside
                                     # the patched parse_model so its globals() lookups resolve)
from ultralytics.nn.modules.block import DFL


# --------------------------------------------------------------------------- #
# 1) BOT module  (Figs 3-5)
# --------------------------------------------------------------------------- #
class MHSA(nn.Module):
    """Multi-Head Self-Attention with relative position embeddings (Fig 3).

    Position embeddings are lazily (re)built on the first forward call (or
    whenever the spatial size changes), so this works at any input
    resolution instead of hard-coding a 20x20 feature map.
    """

    def __init__(self, dim, heads=4):
        super().__init__()
        assert dim % heads == 0, "MHSA channel dim must be divisible by heads"
        self.heads = heads
        self.query = nn.Conv2d(dim, dim, kernel_size=1)
        self.key = nn.Conv2d(dim, dim, kernel_size=1)
        self.value = nn.Conv2d(dim, dim, kernel_size=1)
        self.softmax = nn.Softmax(dim=-1)
        self._hw = None
        self.rel_h = None
        self.rel_w = None

    def _build_pos_embed(self, dim_head, h, w, device, dtype):
        self.rel_h = nn.Parameter(torch.randn(1, self.heads, dim_head, 1, h, device=device, dtype=dtype) * 0.02)
        self.rel_w = nn.Parameter(torch.randn(1, self.heads, dim_head, w, 1, device=device, dtype=dtype) * 0.02)
        self._hw = (h, w)

    def forward(self, x):
        b, c, h, w = x.shape
        dim_head = c // self.heads
        if self._hw != (h, w):
            self._build_pos_embed(dim_head, h, w, x.device, x.dtype)

        q = self.query(x).view(b, self.heads, dim_head, h * w)
        k = self.key(x).view(b, self.heads, dim_head, h * w)
        v = self.value(x).view(b, self.heads, dim_head, h * w)

        content_content = torch.matmul(q.permute(0, 1, 3, 2), k)  # (b, heads, hw, hw)

        pos = (self.rel_h + self.rel_w).view(1, self.heads, dim_head, h * w)
        content_position = torch.matmul(pos.permute(0, 1, 3, 2), q)  # (b, heads, hw, hw)

        energy = content_content + content_position
        attn = self.softmax(energy)
        out = torch.matmul(v, attn.permute(0, 1, 3, 2))
        return out.reshape(b, c, h, w)


class BottleneckTransformer(nn.Module):
    """CBS -> MHSA -> residual add (Fig 4)."""

    def __init__(self, c1, c2, heads=4):
        super().__init__()
        self.cbs = Conv(c1, c2, 3, 1)
        self.mhsa = MHSA(c2, heads=heads)
        self.add = c1 == c2

    def forward(self, x):
        y = self.cbs(x)
        y = self.mhsa(y)
        return x + y if self.add else y


class BoT(nn.Module):
    """BOT module: CBS -> Split -> BottleneckTransformer -> Concat -> Conv (Fig 5).

    Channel-preserving (c2 == c1 in the paper's usage, applied once at the
    end of the backbone on the 20x20xC feature map).
    """

    def __init__(self, c1, c2, e=0.5, heads=4):
        super().__init__()
        self.c = int(c2 * e)
        self.cv1 = Conv(c1, 2 * self.c, 1, 1)
        self.m = BottleneckTransformer(self.c, self.c, heads=heads)
        self.cv2 = Conv(2 * self.c, c2, 1, 1)

    def forward(self, x):
        y = self.cv1(x).chunk(2, 1)
        return self.cv2(torch.cat((y[0], self.m(y[1])), 1))


# --------------------------------------------------------------------------- #
# 2) LSKA — Large Separable Kernel Attention  (Fig 6, Eq 1-5)
# --------------------------------------------------------------------------- #
class LSKA(nn.Module):
    """Large kernel decomposed into separable (1xk / kx1) depthwise branches,
    fused via avg/max-pool spatial attention, channel-preserving.
    """

    def __init__(self, c1, c2, k_sizes=(7, 11)):
        super().__init__()
        assert c1 == c2, "LSKA is channel-preserving: expected c1 == c2"
        c = c1
        self.n = len(k_sizes)
        self.branches = nn.ModuleList()
        for k in k_sizes:
            pad = k // 2
            self.branches.append(
                nn.Sequential(
                    nn.Conv2d(c, c, kernel_size=(1, k), padding=(0, pad), groups=c, bias=False),
                    nn.Conv2d(c, c, kernel_size=(k, 1), padding=(pad, 0), groups=c, bias=False),
                    nn.BatchNorm2d(c),
                )
            )
        self.sa_conv = nn.Conv2d(2, self.n, kernel_size=7, padding=3, bias=False)  # F^{2->N}, Eq 3
        self.sigmoid = nn.Sigmoid()
        self.fuse = Conv(c, c, 1, 1, act=False)  # final F conv, Eq 5

    def forward(self, x):
        feats = [b(x) for b in self.branches]           # N x (B, C, H, W), Eq 1 sub-branches
        cat = torch.cat(feats, dim=1)
        avg = torch.mean(cat, dim=1, keepdim=True)
        mx, _ = torch.max(cat, dim=1, keepdim=True)
        sa = torch.cat([avg, mx], dim=1)                 # Eq 2: SA_avg, SA_max
        sa = self.sigmoid(self.sa_conv(sa))               # Eq 3-4: per-branch spatial weights
        weighted = sum(feats[i] * sa[:, i : i + 1] for i in range(self.n))  # Eq 5
        gate = self.fuse(weighted)
        return x * torch.sigmoid(gate) + x                # residual-gated attention output


# --------------------------------------------------------------------------- #
# 3) C2fGhost  (Fig 10)
# --------------------------------------------------------------------------- #
class C2fGhost(nn.Module):
    """C2f block using GhostBottleneck instead of a standard Bottleneck."""

    def __init__(self, c1, c2, n=1, shortcut=False, g=1, e=0.5):
        super().__init__()
        self.c = int(c2 * e)
        self.cv1 = Conv(c1, 2 * self.c, 1, 1)
        self.cv2 = Conv((2 + n) * self.c, c2, 1)
        self.m = nn.ModuleList(GhostBottleneck(self.c, self.c) for _ in range(n))

    def forward(self, x):
        y = list(self.cv1(x).chunk(2, 1))
        y.extend(m(y[-1]) for m in self.m)
        return self.cv2(torch.cat(y, 1))


# --------------------------------------------------------------------------- #
# 4) LSCD-Head — Lightweight Shared Convolution Detection head  (Fig 11)
# --------------------------------------------------------------------------- #
class ConvGN(nn.Module):
    """Conv -> GroupNorm -> SiLU (the "Conv_GN" block in Fig 11)."""

    def __init__(self, c1, c2, k=1, s=1, groups_gn=16):
        super().__init__()
        p = k // 2
        self.conv = nn.Conv2d(c1, c2, k, s, p, bias=False)
        self.gn = nn.GroupNorm(min(groups_gn, c2), c2)
        self.act = nn.SiLU()

    def forward(self, x):
        return self.act(self.gn(self.conv(x)))


class ScaleLayer(nn.Module):
    """Learnable per-level scalar for the regression branch (the "Scale" box in Fig 11)."""

    def __init__(self, init=1.0):
        super().__init__()
        self.scale = nn.Parameter(torch.tensor(float(init)))

    def forward(self, x):
        return x * self.scale


class _LSCDBranch(nn.Module):
    """Shared proj -> shared Conv_GN x2 -> branch-specific 1x1 (reg or cls)."""

    def __init__(self, proj, share1, share2, out_conv, scale=None):
        super().__init__()
        self.proj = proj      # per-level 1x1 Conv_GN (NOT shared across levels)
        self.share1 = share1  # shared across levels
        self.share2 = share2  # shared across levels
        self.out_conv = out_conv  # shared across levels
        self.scale = scale    # per-level, reg branch only

    def forward(self, x):
        f = self.share2(self.share1(self.proj(x)))
        out = self.out_conv(f)
        return self.scale(out) if self.scale is not None else out


class LSCDHead(Detect):
    """Lightweight Shared Convolution Detection head (Fig 11).

    Same external interface as Detect (nc, reg_max, end2end, ch), so the
    rest of Ultralytics' loss/inference/export code works unchanged — only
    __init__ and bias_init are overridden.
    """

    def __init__(self, nc=80, reg_max=16, end2end=False, ch=()):
        nn.Module.__init__(self)
        self.nc = nc
        self.nl = len(ch)
        self.reg_max = reg_max
        self.no = nc + self.reg_max * 4
        self.stride = torch.zeros(self.nl)
        self.legacy = False
        self._end2end_flag = end2end

        hidc = max(min(ch), 16)  # shared hidden width, kept light on purpose
        self.proj = nn.ModuleList(ConvGN(c, hidc, 1) for c in ch)
        self.share_conv1 = ConvGN(hidc, hidc, 3)
        self.share_conv2 = ConvGN(hidc, hidc, 3)
        self.reg_conv = nn.Conv2d(hidc, 4 * reg_max, 1)
        self.cls_conv = nn.Conv2d(hidc, nc, 1)
        self.scale = nn.ModuleList(ScaleLayer() for _ in ch)

        self.cv2 = nn.ModuleList(
            _LSCDBranch(self.proj[i], self.share_conv1, self.share_conv2, self.reg_conv, self.scale[i])
            for i in range(self.nl)
        )
        self.cv3 = nn.ModuleList(
            _LSCDBranch(self.proj[i], self.share_conv1, self.share_conv2, self.cls_conv, None)
            for i in range(self.nl)
        )
        self.dfl = DFL(reg_max) if reg_max > 1 else nn.Identity()

        if end2end:
            import copy
            self.one2one_cv2 = copy.deepcopy(self.cv2)
            self.one2one_cv3 = copy.deepcopy(self.cv3)

    @property
    def end2end(self):
        return getattr(self, "_end2end_flag", False) and hasattr(self, "one2one_cv2")

    @end2end.setter
    def end2end(self, value):
        self._end2end_flag = value

    def bias_init(self):
        """Shared convs => one bias to initialize (not per-level)."""
        self.reg_conv.bias.data[:] = 1.0
        s = float(self.stride[-1]) if len(self.stride) and self.stride[-1] > 0 else 16.0
        self.cls_conv.bias.data[: self.nc] = math.log(5 / self.nc / (640 / s) ** 2)


# =========================================================================== #
# YOLO-RD — reimplementation based on:
# Wang, W. et al. "YOLO-RD: A Road Damage Detection Method for Effective
# Pavement Maintenance." Sensors 25, 1442 (2025). https://doi.org/10.3390/s25051442
#
# Same situation as YOLOv8-PD above: no official code released (the authors
# say they used MMYOLO/MMDetection internally, and Data Availability only
# points to the RDD2022 dataset). Reconstructed here from Figs 2-6 and Eq 1-10.
#
# Three modules, matching the paper's SOM-Backbone / MAF-PAFPN / WT-Head:
#   - SOM   (Star Operation Module, Fig 3, Eq 1-3)          -> backbone
#   - ARM   (Attention Refinement Module, Fig 4, Eq 5-7)    -> neck
#   - WTHead (Wavelet Transform Convolution head, Fig 5-6, Eq 8-10) -> head
#
# Design choice / deviation from the paper worth flagging explicitly: the
# paper's MAF module also includes a learned multi-stage weighted fusion
# (Eq 4, sum(alpha_i * F_i) with sum(alpha_i)=1). Here that step is realized
# with the standard Upsample -> Concat -> 1x1-Conv pattern already used
# everywhere else in YOLOv8 necks, rather than a bespoke softmax-weighted
# module — it is strictly more expressive (a 1x1 conv can represent an
# arbitrary per-channel linear mix, including a convex combination) and
# keeps the yaml/parser simple.
# =========================================================================== #


# --------------------------------------------------------------------------- #
# 5) SOM — Star Operation Module (Fig 3, Eq 1-3)
# --------------------------------------------------------------------------- #
class SOM(nn.Module):
    """Star Operation Module. Channel-flow exactly follows Eq 1-3:
    DWConv1->BN -> two parallel 1x1 branches (one gated by ReLU6) -> elementwise
    multiply ("star" op) -> 1x1 -> BN -> DWConv2 -> residual add -> final 1x1.
    """

    def __init__(self, c1, c2, e=3):
        super().__init__()
        c_ = int(c1 * e)  # paper uses 3C for the expanded branches
        self.dwconv1 = nn.Conv2d(c1, c1, 3, 1, 1, groups=c1, bias=False)
        self.bn1 = nn.BatchNorm2d(c1)
        self.cv_a = nn.Conv2d(c1, c_, 1, bias=False)
        self.cv_b = nn.Conv2d(c1, c_, 1, bias=False)
        self.act_b = nn.ReLU6()
        self.cv2 = nn.Conv2d(c_, c1, 1, bias=False)
        self.bn2 = nn.BatchNorm2d(c1)
        self.dwconv2 = nn.Conv2d(c1, c1, 3, 1, 1, groups=c1, bias=False)
        self.cv3 = nn.Conv2d(c1, c2, 1, bias=False)

    def forward(self, x):
        y = self.bn1(self.dwconv1(x))            # Eq 1, shared branch input
        a = self.cv_a(y)
        b = self.act_b(self.cv_b(y))
        fused = a * b                              # Eq 1: the "star" element-wise product
        t = self.dwconv2(self.bn2(self.cv2(fused)))  # Eq 2
        t = t + x                                    # Eq 2: residual
        return self.cv3(t)                           # Eq 3


# --------------------------------------------------------------------------- #
# 6) ARM — Attention Refinement Module (Fig 4, Eq 5-7)
# --------------------------------------------------------------------------- #
class ARM(nn.Module):
    """Deformable-conv based spatial refinement, channel-preserving.
    Eq 5: offsets predicted from the input; Eq 6: deformable conv using those
    offsets; Eq 7: sigmoid gate on the result.
    """

    def __init__(self, c1, c2, k=3, deform_groups=1):
        super().__init__()
        assert c1 == c2, "ARM is channel-preserving: expected c1 == c2"
        from torchvision.ops import DeformConv2d

        self.k = k
        self.offset_conv = nn.Conv2d(c1, 2 * k * k * deform_groups, k, padding=k // 2)
        self.deform_conv = DeformConv2d(c1, c2, k, padding=k // 2)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # Defensive sanitization: torchvision's deform_conv2d CPU kernel can
        # segfault (not just misbehave) if fed extreme/garbage offset values —
        # this happens in practice because ultralytics' GFLOPs profiler
        # (thop) probes the model with torch.empty(...) (uninitialized
        # memory, can contain huge/NaN values), not zeros/randn. Clamping
        # here keeps ARM safe regardless of what's upstream.
        x = torch.nan_to_num(x, nan=0.0, posinf=1e4, neginf=-1e4)
        offset = self.offset_conv(x)                 # Eq 5: Δpk
        offset = torch.clamp(offset, -64.0, 64.0)
        y = self.deform_conv(x, offset)               # Eq 6: deform_conv(F, Δpk)
        return self.sigmoid(y)                        # Eq 7


# --------------------------------------------------------------------------- #
# 7) WTC — Wavelet Transform Convolution (Fig 5-6, Eq 8-10)
# --------------------------------------------------------------------------- #
class HaarWavelet2D(nn.Module):
    """Fixed (non-learnable) orthonormal 2D Haar wavelet transform / its
    inverse, implemented as a grouped conv / conv-transpose so it plugs
    straight into a normal nn.Module pipeline. forward: (B,C,H,W) ->
    (B,4C,H/2,W/2) as [LL,LH,HL,HH] blocks per input channel. inverse=True
    reverses that.
    """

    def __init__(self, c, inverse=False):
        super().__init__()
        self.c = c
        self.inverse = inverse
        ll = torch.tensor([[0.5, 0.5], [0.5, 0.5]])
        lh = torch.tensor([[0.5, 0.5], [-0.5, -0.5]])
        hl = torch.tensor([[0.5, -0.5], [0.5, -0.5]])
        hh = torch.tensor([[0.5, -0.5], [-0.5, 0.5]])
        filt = torch.stack([ll, lh, hl, hh], dim=0).unsqueeze(1)  # (4,1,2,2)
        filt = filt.repeat(c, 1, 1, 1)  # (4c,1,2,2), grouped per input channel
        self.register_buffer("filt", filt)

    def forward(self, x):
        if not self.inverse:
            return nn.functional.conv2d(x, self.filt, stride=2, groups=self.c)
        return nn.functional.conv_transpose2d(x, self.filt, stride=2, groups=self.c)


class WTConv(nn.Module):
    """Wavelet Transform Convolution block (Eq 8-10): decompose -> small-kernel
    conv per level on the sub-bands -> recurse into LL -> recombine via
    inverse wavelet transform -> add a parallel plain-conv base path -> project
    to c2. `levels` controls the recursion depth i in Eq 9-10 (paper's Fig 5
    draws 2 levels; default kept at 2 here, but it's configurable).
    """

    def __init__(self, c1, c2, levels=2):
        super().__init__()
        self.c1 = c1
        self.levels = levels
        self.wt = HaarWavelet2D(c1, inverse=False)
        self.iwt = HaarWavelet2D(c1, inverse=True)
        self.band_convs = nn.ModuleList(
            nn.Conv2d(4 * c1, 4 * c1, 3, padding=1, groups=c1, bias=False) for _ in range(levels)
        )
        self.base_conv = Conv(c1, c1, 3, 1)  # parallel "Conv(X)" path in Fig 5
        self.out_conv = Conv(c1, c2, 1, 1)

    def forward(self, x):
        base = self.base_conv(x)
        cur = x
        bands = []
        for i in range(self.levels):
            if cur.shape[-1] < 2 or cur.shape[-2] < 2:
                break  # feature map too small to decompose further
            decomposed = self.band_convs[i](self.wt(cur))
            ll, lh, hl, hh = torch.chunk(decomposed, 4, dim=1)
            bands.append((lh, hl, hh))
            cur = ll
        z = cur
        for lh, hl, hh in reversed(bands):
            z = self.iwt(torch.cat([z, lh, hl, hh], dim=1))
        return self.out_conv(z + base)


class WTHead(Detect):
    """WT-Head: same structure as the stock Detect head, but the first 3x3 conv
    in both the box-regression and classification branches is replaced with
    WTConv. Because the resulting cv2/cv3 are still plain nn.Sequential with
    the same input/output channel contract as stock Detect, forward/bias_init/
    inference/export are all inherited unchanged.
    """

    def __init__(self, nc=80, reg_max=16, end2end=False, ch=(), wt_levels=2):
        nn.Module.__init__(self)
        self.nc = nc
        self.nl = len(ch)
        self.reg_max = reg_max
        self.no = nc + self.reg_max * 4
        self.stride = torch.zeros(self.nl)
        self.legacy = True  # keep the simple 3-conv branch layout (matches Fig 2's head)
        self._end2end_flag = end2end

        c2 = max((16, ch[0] // 4, self.reg_max * 4))
        c3 = max(ch[0], min(self.nc, 100))
        self.cv2 = nn.ModuleList(
            nn.Sequential(WTConv(x, c2, levels=wt_levels), Conv(c2, c2, 3), nn.Conv2d(c2, 4 * self.reg_max, 1))
            for x in ch
        )
        self.cv3 = nn.ModuleList(
            nn.Sequential(WTConv(x, c3, levels=wt_levels), Conv(c3, c3, 3), nn.Conv2d(c3, self.nc, 1))
            for x in ch
        )
        self.dfl = DFL(reg_max) if reg_max > 1 else nn.Identity()

        if end2end:
            import copy
            self.one2one_cv2 = copy.deepcopy(self.cv2)
            self.one2one_cv3 = copy.deepcopy(self.cv3)

    @property
    def end2end(self):
        return getattr(self, "_end2end_flag", False) and hasattr(self, "one2one_cv2")

    @end2end.setter
    def end2end(self, value):
        self._end2end_flag = value


# --------------------------------------------------------------------------- #
# Patch: register the modules above with Ultralytics' YAML model parser
# --------------------------------------------------------------------------- #
def _patched_parse_model(d, ch, verbose=True):
    """Copy of ultralytics.nn.tasks.parse_model (v8.4.34, versi terpasang) with
    BoT, LSKA, C2fGhost added to base_modules/repeat_modules, and LSCDHead/WTHead
    added to the Detect-family branch. Kept as a full copy (rather than a thin
    wrapper) because the original logic is a single large function body, not a
    registry that can be extended piecemeal.
    """
    import ast
    import contextlib

    legacy = True
    max_channels = float("inf")
    nc, act, scales, end2end = (d.get(x) for x in ("nc", "activation", "scales", "end2end"))
    reg_max = d.get("reg_max", 16)
    depth, width, kpt_shape = (d.get(x, 1.0) for x in ("depth_multiple", "width_multiple", "kpt_shape"))
    scale = d.get("scale")
    if scales:
        if not scale:
            scale = next(iter(scales.keys()))
            LOGGER.warning(f"no model scale passed. Assuming scale='{scale}'.")
        depth, width, max_channels = scales[scale]

    if act:
        Conv.default_act = eval(act)
        if verbose:
            LOGGER.info(f"{colorstr('activation:')} {act}")

    if verbose:
        LOGGER.info(f"\n{'':>3}{'from':>20}{'n':>3}{'params':>10}  {'module':<45}{'arguments':<30}")
    ch = [ch]
    layers, save, c2 = [], [], ch[-1]

    base_modules = frozenset(
        {
            Classify, Conv, ConvTranspose, GhostConv, Bottleneck, GhostBottleneck, SPP, SPPF, C2fPSA, C2PSA,
            DWConv, Focus, BottleneckCSP, C1, C2, C2f, C3k2, RepNCSPELAN4, ELAN1, ADown, AConv, SPPELAN,
            C2fAttn, C3, C3TR, C3Ghost, torch.nn.ConvTranspose2d, DWConvTranspose2d, C3x, RepC3, PSA, SCDown,
            C2fCIB, A2C2f,
            BoT, LSKA, C2fGhost,  # <-- YOLOv8-PD additions
            SOM, ARM,             # <-- YOLO-RD additions
        }
    )
    repeat_modules = frozenset(
        {
            BottleneckCSP, C1, C2, C2f, C3k2, C2fAttn, C3, C3TR, C3Ghost, C3x, RepC3, C2fPSA, C2fCIB, C2PSA, A2C2f,
            C2fGhost,  # <-- YOLOv8-PD addition
            # NOTE: SOM is deliberately NOT here. "SOM x8" in the paper means 8
            # independently-weighted stacked SOM blocks, which is exactly what
            # happens when a module is in base_modules but NOT repeat_modules:
            # parse_model builds nn.Sequential(*(SOM(*args) for _ in range(n))).
            # Putting SOM in repeat_modules would instead pass n=8 as a
            # constructor argument to a single SOM instance, which is wrong.
        }
    )
    detect_family = frozenset(
        {Detect, WorldDetect, YOLOEDetect, Segment, Segment26, YOLOESegment, YOLOESegment26, Pose, Pose26, OBB, OBB26,
         LSCDHead,  # <-- YOLOv8-PD addition
         WTHead}    # <-- YOLO-RD addition
    )

    for i, (f, n, m, args) in enumerate(d["backbone"] + d["head"]):
        m = (
            getattr(torch.nn, m[3:])
            if "nn." in m
            else getattr(__import__("torchvision").ops, m[16:])
            if "torchvision.ops." in m
            else globals()[m]
        )
        for j, a in enumerate(args):
            if isinstance(a, str):
                with contextlib.suppress(ValueError):
                    args[j] = locals()[a] if a in locals() else ast.literal_eval(a)
        n = n_ = max(round(n * depth), 1) if n > 1 else n

        if m in base_modules:
            c1, c2 = ch[f], args[0]
            if c2 != nc:
                c2 = make_divisible(min(c2, max_channels) * width, 8)
            if m is C2fAttn:
                args[1] = make_divisible(min(args[1], max_channels // 2) * width, 8)
                args[2] = int(max(round(min(args[2], max_channels // 2 // 32)) * width, 1) if args[2] > 1 else args[2])
            args = [c1, c2, *args[1:]]
            if m in repeat_modules:
                args.insert(2, n)
                n = 1
            if m is C3k2:
                legacy = False
                if scale in "mlx":
                    args[3] = True
            if m is A2C2f:
                legacy = False
                if scale in "lx":
                    args.extend((True, 1.2))
            if m is C2fCIB:
                legacy = False
        elif m is AIFI:
            args = [ch[f], *args]
        elif m in frozenset({HGStem, HGBlock}):
            c1, cm, c2 = ch[f], args[0], args[1]
            args = [c1, cm, c2, *args[2:]]
            if m is HGBlock:
                args.insert(4, n)
                n = 1
        elif m is ResNetLayer:
            c2 = args[1] if args[3] else args[1] * 4
        elif m is torch.nn.BatchNorm2d:
            args = [ch[f]]
        elif m is Concat:
            c2 = sum(ch[x] for x in f)
        elif m in detect_family:
            args.extend([reg_max, end2end, [ch[x] for x in f]])
            if m is Segment or m is YOLOESegment or m is Segment26 or m is YOLOESegment26:
                args[2] = make_divisible(min(args[2], max_channels) * width, 8)
            if m in {Detect, YOLOEDetect, Segment, Segment26, YOLOESegment, YOLOESegment26, Pose, Pose26, OBB, OBB26}:
                m.legacy = legacy
        elif m is v10Detect:
            args.append([ch[x] for x in f])
        elif m is ImagePoolingAttn:
            args.insert(1, [ch[x] for x in f])
        elif m is RTDETRDecoder:
            args.insert(1, [ch[x] for x in f])
        elif m is CBLinear:
            c2 = args[0]
            c1 = ch[f]
            args = [c1, c2, *args[1:]]
        elif m is CBFuse:
            c2 = ch[f[-1]]
        elif m in frozenset({TorchVision, Index}):
            c2 = args[0]
            c1 = ch[f]
            args = [*args[1:]]
        else:
            c2 = ch[f]

        m_ = torch.nn.Sequential(*(m(*args) for _ in range(n))) if n > 1 else m(*args)
        t = str(m)[8:-2].replace("__main__.", "")
        m_.np = sum(x.numel() for x in m_.parameters())
        m_.i, m_.f, m_.type = i, f, t
        if verbose:
            LOGGER.info(f"{i:>3}{f!s:>20}{n_:>3}{m_.np:10.0f}  {t:<45}{args!s:<30}")
        save.extend(x % i for x in ([f] if isinstance(f, int) else f) if x != -1)
        layers.append(m_)
        if i == 0:
            ch = []
        ch.append(c2)
    return torch.nn.Sequential(*layers), sorted(save)


def patch_ultralytics():
    """Call this once, before building/loading a YOLOv8-PD .yaml model."""
    tasks.parse_model = _patched_parse_model
    # also expose the new classes on the tasks module in case any other
    # ultralytics code path resolves module names via `ultralytics.nn.tasks.<Name>`
    tasks.BoT = BoT
    tasks.LSKA = LSKA
    tasks.C2fGhost = C2fGhost
    tasks.LSCDHead = LSCDHead
    tasks.SOM = SOM
    tasks.ARM = ARM
    tasks.WTConv = WTConv
    tasks.WTHead = WTHead


# NOTE for other ultralytics versions:
# If patch_ultralytics() or model-building raises AttributeError / ImportError,
# ultralytics likely renamed/reordered something in nn/tasks.py's parse_model.
# Fix: re-open your installed nn/tasks.py, diff it against the copy inlined
# above in _patched_parse_model, and port the 3 additions (base_modules,
# repeat_modules, detect_family) into the new version of the function.
