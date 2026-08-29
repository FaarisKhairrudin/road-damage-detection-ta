#!/usr/bin/env python3
"""
Interactive Dataset & Annotation Explorer for Road Damage Detection (6 Classes).
Built with Streamlit and OpenCV.
"""

from pathlib import Path
import cv2
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import streamlit as st
import yaml

# Page configuration
st.set_page_config(
    page_title="RDD Dataset & Annotation Explorer",
    page_icon="🛣️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Class names and color mapping (RGB format for PIL / rendering)
CLASS_INFO = {
    0: {"name": "Longitudinal_Crack", "color_hex": "#00E676", "rgb": (0, 230, 118)},
    1: {"name": "Transverse_Crack", "color_hex": "#00B0FF", "rgb": (0, 176, 255)},
    2: {"name": "Alligator_Crack", "color_hex": "#FFD600", "rgb": (255, 214, 0)},
    3: {"name": "Pothole", "color_hex": "#FF1744", "rgb": (255, 23, 68)},
    4: {"name": "Penutup_Jalan", "color_hex": "#D500F9", "rgb": (213, 0, 249)},
    5: {"name": "Tambalan", "color_hex": "#FF6D00", "rgb": (255, 109, 0)},
}

CLASS_NAME_TO_ID = {v["name"]: k for k, v in CLASS_INFO.items()}
CLASS_ID_TO_NAME = {k: v["name"] for k, v in CLASS_INFO.items()}
CLASS_ID_TO_RGB = {k: v["rgb"] for k, v in CLASS_INFO.items()}


def extract_country(filename: str) -> str:
    """Extract country from filename (China, India, Japan)."""
    parts = filename.split("_")
    prefix = parts[0] if parts else "Unknown"
    if prefix in {"China", "India", "Japan"}:
        return prefix
    return "Other"


def parse_yolo_txt(txt_path: Path):
    """Parse YOLO label file and return list of dicts."""
    boxes = []
    if not txt_path.exists():
        return boxes

    with open(txt_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 5:
                try:
                    cls_id = int(float(parts[0]))
                    xc = float(parts[1])
                    yc = float(parts[2])
                    w = float(parts[3])
                    h = float(parts[4])
                    boxes.append({
                        "class_id": cls_id,
                        "class_name": CLASS_ID_TO_NAME.get(cls_id, f"Class_{cls_id}"),
                        "xc": xc,
                        "yc": yc,
                        "w": w,
                        "h": h,
                    })
                except ValueError:
                    continue
    return boxes


@st.cache_data(show_spinner=True)
def scan_dataset(yaml_path_str: str):
    """Scan dataset folder and index all images with their annotations and metadata."""
    yaml_file = Path(yaml_path_str).resolve()
    if not yaml_file.exists():
        return pd.DataFrame(), {}

    with open(yaml_file, "r", encoding="utf-8") as f:
        data_cfg = yaml.safe_load(f)

    base_dir = yaml_file.parent
    records = []

    valid_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

    for split in ["train", "val", "test"]:
        split_path_rel = data_cfg.get(split)
        if not split_path_rel:
            continue

        images_dir = (base_dir / split_path_rel).resolve()
        if not images_dir.exists():
            custom_path = data_cfg.get("path", ".")
            images_dir = (base_dir / custom_path / split_path_rel).resolve()

        if not images_dir.exists():
            continue

        labels_dir = images_dir.parent / "labels" if images_dir.name == "images" else images_dir / "labels"

        image_files = [p for p in images_dir.iterdir() if p.suffix.lower() in valid_extensions]

        for img_path in image_files:
            txt_path = labels_dir / f"{img_path.stem}.txt"
            boxes = parse_yolo_txt(txt_path)
            country = extract_country(img_path.name)
            class_ids = [b["class_id"] for b in boxes]
            class_names = [b["class_name"] for b in boxes]

            records.append({
                "filename": img_path.name,
                "image_path": str(img_path),
                "label_path": str(txt_path) if txt_path.exists() else "",
                "split": split,
                "country": country,
                "num_boxes": len(boxes),
                "class_ids": class_ids,
                "class_names": class_names,
                "has_boxes": len(boxes) > 0,
            })

    df = pd.DataFrame(records)
    return df, data_cfg


def draw_bounding_boxes(
    image_path: str,
    boxes: list,
    show_boxes: bool = True,
    show_labels: bool = True,
    box_thickness: int = 3,
    alpha_overlay: float = 0.0,
):
    """Render bounding boxes on image with high contrast colors and labels."""
    image = Image.open(image_path).convert("RGB")
    width, height = image.size

    if not show_boxes or not boxes:
        return image

    # Create overlay for optional filled boxes
    overlay = image.copy() if alpha_overlay > 0 else None
    draw_main = ImageDraw.Draw(image)
    draw_overlay = ImageDraw.Draw(overlay) if overlay else None

    # Try loading a readable default font
    try:
        font = ImageFont.load_default(size=14)
    except Exception:
        font = ImageFont.load_default()

    for box in boxes:
        cls_id = box["class_id"]
        color = CLASS_ID_TO_RGB.get(cls_id, (255, 255, 255))
        label_text = box["class_name"]

        # Normalized coordinates to pixel coordinates
        xc, yc, w, h = box["xc"], box["yc"], box["w"], box["h"]
        x1 = max(0, int((xc - w / 2.0) * width))
        y1 = max(0, int((yc - h / 2.0) * height))
        x2 = min(width - 1, int((xc + w / 2.0) * width))
        y2 = min(height - 1, int((yc + h / 2.0) * height))

        if overlay and draw_overlay:
            draw_overlay.rectangle([x1, y1, x2, y2], fill=color)

        draw_main.rectangle([x1, y1, x2, y2], outline=color, width=box_thickness)

        if show_labels:
            bbox_text = draw_main.textbbox((x1, y1), label_text, font=font)
            text_w = bbox_text[2] - bbox_text[0] + 8
            text_h = bbox_text[3] - bbox_text[1] + 6

            text_bg_y1 = max(0, y1 - text_h)
            text_bg_y2 = y1 if text_bg_y1 < y1 else y1 + text_h

            # Label badge background
            draw_main.rectangle([x1, text_bg_y1, x1 + text_w, text_bg_y2], fill=color)

            # Label badge text (black for readability on bright backgrounds)
            text_color = (0, 0, 0)
            draw_main.text((x1 + 4, text_bg_y1 + 2), label_text, fill=text_color, font=font)

    if overlay and alpha_overlay > 0:
        return Image.blend(image, overlay, alpha_overlay)

    return image


def main():
    st.title("🛣️ Road Damage Detection — Dataset & Annotation Explorer")
    st.caption("Eksplorasi interaktif dataset 6 kelas (China, India, Japan) dengan filter negara, split, dan kelas kerusakan.")

    default_yaml = "data/NRDD-2024/RDD_Split_Final_china_japan_india_6_classes/RDD_Split_Final_china_japan_india_6_classes/data.yaml"

    with st.spinner("Memindai dan mengindeks dataset..."):
        df, cfg = scan_dataset(default_yaml)

    if df.empty:
        st.error(f"Dataset tidak ditemukan di path: `{default_yaml}`")
        return

    # --- SIDEBAR FILTERS ---
    st.sidebar.header("🔍 Filter Dataset")

    # 1. Filter Split
    available_splits = sorted(df["split"].unique().tolist())
    selected_splits = st.sidebar.multiselect(
        "Split Dataset",
        options=available_splits,
        default=available_splits,
    )

    # 2. Filter Negara
    available_countries = sorted(df["country"].unique().tolist())
    selected_countries = st.sidebar.multiselect(
        "Negara Asal (Country)",
        options=available_countries,
        default=available_countries,
    )

    # 3. Filter Kelas Kerusakan
    all_class_names = [v["name"] for v in CLASS_INFO.values()]
    selected_classes = st.sidebar.multiselect(
        "Filter Keberadaan Kelas",
        options=all_class_names,
        default=[],
        help="Pilih kelas untuk hanya menampilkan gambar yang mengandung kerusakan tersebut. Kosongkan untuk menampilkan semua.",
    )

    match_mode = "Mengandung Salah Satu (OR)"
    if selected_classes:
        match_mode = st.sidebar.radio(
            "Mode Filter Kelas",
            ["Mengandung Salah Satu (OR)", "Mengandung Semua yang Dipilih (AND)"],
            index=0,
        )

    # 4. Search by Filename
    search_query = st.sidebar.text_input("Cari Nama File", placeholder="Contoh: China_MotorBike_000100")

    # --- SIDEBAR DISPLAY OPTIONS ---
    st.sidebar.markdown("---")
    st.sidebar.header("🎨 Opsi Tampilan Visual")
    show_boxes = st.sidebar.checkbox("Tampilkan Bounding Box", value=True)
    show_labels = st.sidebar.checkbox("Tampilkan Nama Label Kelas", value=True)
    box_thickness = st.sidebar.slider("Ketebalan Garis Box (px)", min_value=1, max_value=6, value=3)
    alpha_overlay = st.sidebar.slider("Transparansi Isi Box (Fill)", min_value=0.0, max_value=0.5, value=0.1, step=0.05)

    # --- COLOR LEGEND IN SIDEBAR ---
    st.sidebar.markdown("---")
    st.sidebar.subheader("🎨 Legenda Warna Kelas (6 Kelas)")
    legend_html = ""
    for cid, info in CLASS_INFO.items():
        legend_html += f"""
        <div style="display:flex; align-items:center; margin-bottom:6px;">
            <div style="width:16px; height:16px; background-color:{info['color_hex']}; border-radius:3px; margin-right:8px; border:1px solid #333;"></div>
            <span style="font-size:13px; font-weight:500;">[{cid}] {info['name']}</span>
        </div>
        """
    st.sidebar.markdown(legend_html, unsafe_allow_html=True)

    # --- FILTERING DATAFRAME ---
    filtered_df = df[df["split"].isin(selected_splits) & df["country"].isin(selected_countries)]

    if search_query.strip():
        filtered_df = filtered_df[filtered_df["filename"].str.contains(search_query.strip(), case=False, na=False)]

    if selected_classes:
        if match_mode == "Mengandung Semua yang Dipilih (AND)":
            filtered_df = filtered_df[filtered_df["class_names"].apply(lambda names: all(c in names for c in selected_classes))]
        else:
            filtered_df = filtered_df[filtered_df["class_names"].apply(lambda names: any(c in names for c in selected_classes))]

    # --- TOP METRICS BAR ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Gambar Terfilter", f"{len(filtered_df):,} / {len(df):,}")
    with col2:
        st.metric("Split Aktif", ", ".join(selected_splits) if selected_splits else "None")
    with col3:
        st.metric("Negara Terpilih", ", ".join(selected_countries) if selected_countries else "None")
    with col4:
        total_boxes = sum(filtered_df["num_boxes"])
        st.metric("Total Bounding Box", f"{total_boxes:,}")

    if filtered_df.empty:
        st.warning("Tidak ada gambar yang cocok dengan filter yang dipilih.")
        return

    # --- TABS: INSPECTOR VS GALLERY VS STATS ---
    tab_single, tab_gallery, tab_stats = st.tabs(["🔍 Single Image Inspector", "🖼️ Grid Gallery", "📊 Statistik & Distribusi"])

    # TAB 1: SINGLE IMAGE INSPECTOR
    with tab_single:
        num_items = len(filtered_df)
        
        c_slider, c_btn1, c_btn2 = st.columns([4, 1, 1])
        with c_slider:
            img_index = st.slider("Navigasi Gambar (Index)", min_value=0, max_value=num_items - 1, value=0)
        with c_btn1:
            if st.button("⬅️ Sebelumnya") and img_index > 0:
                img_index -= 1
        with c_btn2:
            if st.button("Selanjutnya ➡️") and img_index < num_items - 1:
                img_index += 1

        selected_row = filtered_df.iloc[img_index]
        image_path = selected_row["image_path"]
        label_path = Path(selected_row["label_path"]) if selected_row["label_path"] else None
        boxes = parse_yolo_txt(label_path) if label_path else []

        rendered_img = draw_bounding_boxes(
            image_path=image_path,
            boxes=boxes,
            show_boxes=show_boxes,
            show_labels=show_labels,
            box_thickness=box_thickness,
            alpha_overlay=alpha_overlay,
        )

        col_img, col_details = st.columns([3, 2])
        with col_img:
            st.image(rendered_img, use_container_width=True, caption=f"{selected_row['filename']} ({selected_row['country']} - {selected_row['split'].upper()})")

        with col_details:
            st.subheader("📋 Informasi & Metadata")
            st.write(f"**Nama File**: `{selected_row['filename']}`")
            st.write(f"**Negara**: `{selected_row['country']}`")
            st.write(f"**Split**: `{selected_row['split'].upper()}`")
            st.write(f"**Jumlah Objek**: `{len(boxes)} Bounding Box`")
            st.write(f"**Dimensi Gambar**: `{rendered_img.width} x {rendered_img.height} px`")

            if boxes:
                st.markdown("#### Detail Anotasi:")
                box_rows = []
                for i, b in enumerate(boxes, start=1):
                    # compute pixel coordinates
                    x1 = int((b["xc"] - b["w"] / 2.0) * rendered_img.width)
                    y1 = int((b["yc"] - b["h"] / 2.0) * rendered_img.height)
                    x2 = int((b["xc"] + b["w"] / 2.0) * rendered_img.width)
                    y2 = int((b["yc"] + b["h"] / 2.0) * rendered_img.height)
                    box_rows.append({
                        "No": i,
                        "Kelas": b["class_name"],
                        "Box Pixel [x1, y1, x2, y2]": f"[{x1}, {y1}, {x2}, {y2}]",
                        "YOLO [xc, yc, w, h]": f"[{b['xc']:.3f}, {b['yc']:.3f}, {b['w']:.3f}, {b['h']:.3f}]",
                    })
                st.dataframe(pd.DataFrame(box_rows), hide_index=True, use_container_width=True)
            else:
                st.info("Gambar ini tidak memiliki bounding box / label (Background image).")

    # TAB 2: GRID GALLERY
    with tab_gallery:
        st.subheader("Galeri Gambar Terfilter")
        page_size = st.selectbox("Jumlah gambar per halaman", options=[6, 12, 18, 24], index=1)
        total_pages = max(1, (len(filtered_df) + page_size - 1) // page_size)
        page = st.number_input("Halaman", min_value=1, max_value=total_pages, value=1)

        start_idx = (page - 1) * page_size
        end_idx = min(start_idx + page_size, len(filtered_df))
        page_df = filtered_df.iloc[start_idx:end_idx]

        cols_per_row = 3
        for r_idx in range(0, len(page_df), cols_per_row):
            cols = st.columns(cols_per_row)
            for c_idx in range(cols_per_row):
                item_idx = r_idx + c_idx
                if item_idx < len(page_df):
                    row = page_df.iloc[item_idx]
                    l_path = Path(row["label_path"]) if row["label_path"] else None
                    b_list = parse_yolo_txt(l_path) if l_path else []
                    img_thumb = draw_bounding_boxes(
                        image_path=row["image_path"],
                        boxes=b_list,
                        show_boxes=show_boxes,
                        show_labels=show_labels,
                        box_thickness=max(1, box_thickness - 1),
                        alpha_overlay=alpha_overlay,
                    )
                    with cols[c_idx]:
                        st.image(
                            img_thumb,
                            use_container_width=True,
                            caption=f"{row['filename'][:28]}... ({row['country']})",
                        )

    # TAB 3: STATISTIK & DISTRIBUSI
    with tab_stats:
        st.subheader("📊 Statistik Distribusi Data Terfilter")
        col_s1, col_s2 = st.columns(2)

        with col_s1:
            st.markdown("#### Distribusi Kelas Kerusakan")
            all_classes_flat = [cls for sublist in filtered_df["class_names"] for cls in sublist]
            if all_classes_flat:
                class_counts = pd.Series(all_classes_flat).value_counts().reset_index()
                class_counts.columns = ["Kelas Kerusakan", "Jumlah Bounding Box"]
                st.dataframe(class_counts, hide_index=True, use_container_width=True)
                st.bar_chart(class_counts.set_index("Kelas Kerusakan"))
            else:
                st.write("Tidak ada objek terdeteksi pada filter saat ini.")

        with col_s2:
            st.markdown("#### Distribusi Gambar per Negara & Split")
            country_split_df = filtered_df.groupby(["country", "split"]).size().unstack(fill_value=0)
            st.dataframe(country_split_df, use_container_width=True)
            st.bar_chart(country_split_df)


if __name__ == "__main__":
    main()
