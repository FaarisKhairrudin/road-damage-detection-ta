"""Regenerate domain embeddings, projections and image statistics on frozen Indo V4.

No notebook execution, training or writes into the historical V2 compatibility path.
Run with Python 3.12 and the project's torch/ultralytics plus sklearn/umap stack.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.metadata
import json
import random
import shutil
from pathlib import Path
import time
import cv2
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import normalize
import umap

ROOT = Path(__file__).resolve().parents[1]
ORDER = ['China', 'Japan', 'India', 'Indonesia']
COLORS = dict(zip(ORDER, ['#0072B2','#D55E00','#009E73','#CC79A7']))
DEFAULT_OUT = ROOT / 'runs/rdd_yolov8n_local/evaluation/domain_viz_v4'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def plot_projection(coords, domains, method, output):
    fig, ax = plt.subplots(figsize=(8, 5.5), layout='constrained')
    for domain in ORDER:
        points = coords[domains == domain]
        ax.scatter(points[:,0], points[:,1], s=13, alpha=.65,
                   color=COLORS[domain], label=f'{domain} (n={len(points)})', linewidths=0)
    ax.legend(frameon=True, fontsize=9)
    ax.set(xlabel=method+' 1', ylabel=method+' 2', title=f'{method}: source test and Indonesia V4')
    ax.spines[['top','right']].set_visible(False)
    fig.savefig(output, dpi=180)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=DEFAULT_OUT)
    parser.add_argument('--device', default='cpu')
    parser.add_argument('--batch', type=int, default=16)
    parser.add_argument('--resume', action='store_true', help='Reuse matching cached embeddings after an interrupted run.')
    args = parser.parse_args()
    raw_output = args.output.expanduser().absolute()
    if any(p.is_symlink() for p in [raw_output, *raw_output.parents]):
        raise ValueError('Output must not traverse directory compatibility aliases.')
    output = raw_output.resolve()
    if output == (ROOT/'runs/rdd_yolov8n_local/evaluation/domain_viz').resolve():
        raise ValueError('Never write current results into the legacy V2 bundle or a compatibility alias.')
    if output.exists() and not args.resume:
        raise FileExistsError(f'{output} exists; use another output or --resume after verifying cached inputs.')
    registry = json.loads((ROOT/'docs/FINAL_ARTIFACTS.json').read_text())
    source = ROOT/registry['source_datasets']['six_class']
    target = ROOT/registry['target']['dataset']
    weights = ROOT/'runs/rdd_yolov8n_local/experiments/yolov8n_class_weight/weights/best.pt'
    rows = []
    extensions = {'.jpg','.jpeg','.png','.bmp','.webp'}
    for domain in ORDER:
        folder = target/'valid/images' if domain=='Indonesia' else source/'test/images'
        pool = sorted(p for p in folder.iterdir() if p.suffix.lower() in extensions and (domain=='Indonesia' or p.name.startswith(domain+'_')))
        for image in pool:
            label = image.parent.parent/'labels'/(image.stem+'.txt')
            if not label.is_file():
                raise FileNotFoundError(label)
            rows.append({'path':str(image), 'relative_path':str(image.relative_to(ROOT)),
                         'domain':domain, 'image_sha256':sha(image), 'label_sha256':sha(label),
                         'annotations':len([x for x in label.read_text().splitlines() if x.strip()])})
    random.Random(42).shuffle(rows)
    manifest = pd.DataFrame(rows)
    expected = {'China':180,'Japan':705,'India':110,'Indonesia':307}
    if manifest.domain.value_counts().to_dict()!=expected or len(manifest)!=1302:
        raise ValueError(f'Unexpected frozen split membership: {manifest.domain.value_counts().to_dict()}')
    assert manifest.relative_path.is_unique
    target_rows = manifest[manifest.domain=='Indonesia']
    if target_rows.annotations.sum()!=502 or (target_rows.annotations==0).sum()!=39:
        raise ValueError('Target annotation inventory no longer matches frozen V4.')
    input_manifest_hash = hashlib.sha256(manifest.to_csv(index=False).encode()).hexdigest()
    import torch
    from ultralytics import YOLO
    torch.manual_seed(42)
    torch.set_num_threads(4)
    model = YOLO(str(weights))
    layer = len(model.model.model)-2
    inputs = {'manifest_sha256':input_manifest_hash, 'weights_sha256':sha(weights),
              'embedding_layer':layer, 'imgsz':640, 'batch':args.batch, 'half':False,
              'rect':True, 'device':args.device, 'seed':42, 'counts':expected,
              'target_annotations':502, 'target_empty_images':39,
              'versions':{p:importlib.metadata.version(p) for p in ['torch','torchvision','ultralytics','numpy','pandas','scikit-learn','umap-learn','opencv-python','matplotlib']}}
    output.mkdir(parents=True, exist_ok=True)
    (output/'INCOMPLETE.md').write_text('Run in progress; outputs are not final until completion is published.\n')
    (output/'run_status.json').write_text(json.dumps({'status':'running','complete':False})+'\n')
    cache_meta = output/'inputs.json'
    if args.resume and (output/'embeddings.npy').is_file():
        if not cache_meta.is_file() or json.loads(cache_meta.read_text())!=inputs:
            raise ValueError('Cached embedding provenance does not match current inputs/settings.')
        X=np.load(output/'embeddings.npy')
        print('Reused matching embeddings', X.shape, flush=True)
    else:
        cache_meta.write_text(json.dumps(inputs,indent=2)+'\n')
        manifest.to_csv(output/'manifest.csv',index=False)
        vectors=[]; start=time.perf_counter()
        with torch.inference_mode():
            for i in range(0,len(manifest),args.batch):
                paths=manifest.path.iloc[i:i+args.batch].tolist()
                vectors.extend(x.cpu().numpy() for x in model.embed(paths, embed=[layer], imgsz=640,
                                batch=args.batch, device=args.device, half=False, rect=True, verbose=False))
                if i % (args.batch*8)==0:
                    print(f'Embeddings {min(i+args.batch,len(manifest))}/{len(manifest)}; {time.perf_counter()-start:.1f}s',flush=True)
        X=np.stack(vectors).astype(np.float32)
        np.save(output/'embeddings.npy',X)
    if X.shape[0]!=1302 or X.ndim!=2 or not np.isfinite(X).all():
        raise ValueError('Invalid embedding shape or nonfinite feature.')
    domains=manifest.domain.to_numpy(dtype='U16')
    np.save(output/'domains.npy',domains)
    Xn=normalize(X)
    print('Projecting',X.shape,flush=True)
    projection_umap=umap.UMAP(n_neighbors=15,min_dist=.1,metric='euclidean',random_state=42,n_jobs=1).fit_transform(Xn)
    projection_tsne=TSNE(n_components=2,perplexity=30,random_state=42,init='pca',learning_rate='auto').fit_transform(Xn)
    for name,coords in [('umap',projection_umap),('tsne',projection_tsne)]:
        if coords.shape!=(1302,2) or not np.isfinite(coords).all():
            raise ValueError('Invalid projection shape or nonfinite coordinate.')
        np.save(output/(name+'.npy'),coords)
        plot_projection(coords,domains,'UMAP' if name=='umap' else 't-SNE',output/(name+'.png'))
    silhouette=float(silhouette_score(Xn,domains))
    records=[]
    for row in manifest.itertuples():
        image=cv2.imread(row.path)
        if image is None:raise ValueError('Unreadable image: '+row.path)
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY);hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        records.append({'relative_path':row.relative_path,'domain':row.domain,'width':image.shape[1],'height':image.shape[0],
                        'brightness':float(hsv[:,:,2].mean()),'saturation':float(hsv[:,:,1].mean()),
                        'contrast':float(gray.std()),'sharpness':float(cv2.Laplacian(gray,cv2.CV_64F).var())})
    stats=pd.DataFrame(records)
    stats.to_csv(output/'image_stats.csv',index=False)
    medians=stats.groupby('domain')[['brightness','saturation','contrast','sharpness']].median().reindex(ORDER)
    medians['images']=[expected[x] for x in ORDER]
    medians.to_csv(output/'domain_medians.csv')
    fig,axes=plt.subplots(2,2,figsize=(10,7),layout='constrained')
    for ax,column,title in zip(axes.flat,['brightness','saturation','contrast','sharpness'],['Brightness: mean HSV V','Saturation: mean HSV S','Contrast: grayscale standard deviation','Sharpness proxy: Laplacian variance']):
        ax.boxplot([stats.loc[stats.domain==d,column] for d in ORDER],showfliers=False)
        ax.set_xticks(range(1,5),ORDER)
        ax.set_title(title,fontsize=10);ax.spines[['top','right']].set_visible(False)
    fig.suptitle('Image statistics: same frozen source test and Indonesia V4')
    fig.savefig(output/'stats.png',dpi=180);plt.close(fig)
    sample_rows=[]
    fig,axes=plt.subplots(4,4,figsize=(11,10),layout='constrained')
    for i,domain in enumerate(ORDER):
        sample=manifest[manifest.domain==domain].head(4)
        for j,row in enumerate(sample.itertuples()):
            axes[i,j].imshow(cv2.cvtColor(cv2.imread(row.path),cv2.COLOR_BGR2RGB));axes[i,j].set_axis_off()
            axes[i,j].set_title(domain if j==0 else '',fontsize=11)
            sample_rows.append({'domain':domain,'relative_path':row.relative_path})
    fig.suptitle('Four examples per domain; shuffled manifest, seed 42')
    fig.savefig(output/'samples.png',dpi=150);plt.close(fig)
    pd.DataFrame(sample_rows).to_csv(output/'samples_manifest.csv',index=False)
    provenance={'inputs':inputs,'embedding_shape':list(X.shape),'silhouette_normalized_feature_space':silhouette,
                'umap':{'n_neighbors':15,'min_dist':.1,'metric':'euclidean','random_state':42},
                'tsne':{'perplexity':30,'init':'pca','learning_rate':'auto','random_state':42},
                'scope':'Exploratory descriptive analysis, not a causal explanation of accuracy or a physical distance between domains.',
                'outputs':{p.name:sha(p) for p in sorted(output.iterdir()) if p.is_file() and p.name not in {'provenance.json','run_status.json','INCOMPLETE.md'}}}
    (output/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
    published = ROOT/'docs/figures/domain_v4'
    published.mkdir(parents=True, exist_ok=True)
    for name in ['umap.png','tsne.png','stats.png','samples.png','domain_medians.csv','provenance.json']:
        shutil.copy2(output/name, published/name)
    marker=output/'INCOMPLETE.md'
    if marker.exists(): marker.unlink()
    status_tmp=output/'.run_status.tmp'
    status_tmp.write_text(json.dumps({'status':'complete','complete':True,'embedding_shape':list(X.shape)},indent=2)+'\n')
    status_tmp.replace(output/'run_status.json')
    print('Completed',output,'silhouette=',silhouette,flush=True)
    print(medians.round(2).to_string(),flush=True)


if __name__=='__main__':main()
