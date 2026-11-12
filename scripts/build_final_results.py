#!/usr/bin/env python3
"""Generate canonical research tables and documentation figures without inference.

Run from any directory: python scripts/build_final_results.py
Inputs are selected by docs/FINAL_ARTIFACTS.json. Outputs are confined to
RESULTS_TABLE.md, docs/figures/final_results/, and evaluation/final_report/.
Original run CSVs, notebooks, raw logs and manuscript assets are never rewritten.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
import re
import statistics

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[1]
MODELS = ['yolov8n', 'yolov12n', 'yolov26n', 'yolov8_pd', 'yolo_rd']
DISPLAY = dict(zip(MODELS, ['YOLOv8n', 'YOLOv12n', 'YOLO26n', 'YOLOv8-PD', 'YOLO-RD']))
COLORS = ['#2878a0', '#e08b36', '#458b66', '#a65b85', '#6c66a6']
NAMES = ['Longitudinal_Crack', 'Transverse_Crack', 'Alligator_Crack', 'Pothole', 'manhole', 'patchy_road']
CODES = ['D00', 'D10', 'D20', 'D40', 'D70', 'D80']
METRICS = ['precision', 'recall', 'f1', 'mAP50', 'mAP50-95']
REPORT = ROOT / 'runs/rdd_yolov8n_local/evaluation/final_report'
FIGURES = ROOT / 'docs/figures/final_results'


class Inputs:
    def __init__(self, root):
        self.root, self.paths = root, set()

    def path(self, name):
        path = self.root / name
        if not path.is_file():
            raise FileNotFoundError(f'Required canonical artifact is missing: {name}')
        self.paths.add(path)
        return path

    def json(self, name):
        return json.loads(self.path(name).read_text())

    def csv(self, name):
        with self.path(name).open(newline='') as file:
            return [{key.strip(): value.strip() for key, value in row.items()} for row in csv.DictReader(file)]

    def yaml(self, name):
        return yaml.safe_load(self.path(name).read_text())


def per_class(rows, model):
    result = []
    for raw in rows:
        cid = int(raw['class_id'])
        if raw.get('model', model) != model:
            continue
        row = {'model': model, 'class_id': cid, 'class_name': raw['class_name'], 'support': int(float(raw['support']))}
        if row['class_name'] != NAMES[cid]:
            raise ValueError(f'Class order mismatch for {model}: {raw}')
        row['evaluated'] = raw.get('evaluated', str(row['support'] > 0)).lower() == 'true'
        for metric in METRICS:
            row[metric] = float(raw[metric]) if raw[metric] else None
        if row['evaluated'] and (row['support'] <= 0 or any(row[key] is None for key in METRICS)):
            raise ValueError(f'Incomplete evaluated row: {row}')
        result.append(row)
    if len({row['class_id'] for row in result}) != len(result):
        raise ValueError(f'Duplicate per-class rows for {model}')
    return sorted(result, key=lambda row: row['class_id'])


def aggregate(rows, ids):
    ids = set(ids)
    selected = [row for row in rows if row['class_id'] in ids]
    if {row['class_id'] for row in selected} != ids or any(not row['evaluated'] for row in selected):
        raise ValueError(f'Cannot compare missing or unevaluated classes: {ids}')
    result = {key: statistics.mean(row[key] for row in selected) for key in METRICS}
    result['weighted_f1'] = sum(row['f1'] * row['support'] for row in selected) / sum(row['support'] for row in selected)
    result['support'] = sum(row['support'] for row in selected)
    return result


def comparison(model, source, target, ids):
    left, right = aggregate(source, ids), aggregate(target, ids)
    return {'model': model, 'source_mAP50': left['mAP50'], 'target_mAP50': right['mAP50'],
            'absolute_drop_pp': 100 * (left['mAP50'] - right['mAP50']),
            'relative_drop_pct': 100 * (1 - right['mAP50'] / left['mAP50']),
            'source_macro_f1': left['f1'], 'target_macro_f1': right['f1'],
            'source_weighted_f1': left['weighted_f1'], 'target_weighted_f1': right['weighted_f1']}


def country_table(text):
    block = text.split(r'\label{tab:country-four}', 1)[1].split(r'\end{tabular}', 1)[0]
    reverse = {value: key for key, value in DISPLAY.items()}
    rows = []
    for match in re.finditer(r'^(YOLO[^&\n]+)&\s*([\d.]+)\s*&\s*([\d.]+)\s*&\s*([\d.]+)', block, re.M):
        name, china, japan, india = [part.strip() for part in match.groups()]
        rows.append(dict(model=reverse[name], China=float(china), Japan=float(japan), India=float(india)))
    if [row['model'] for row in rows] != MODELS:
        raise ValueError('Could not extract the documented common-four-class country table.')
    return rows


def build_tables(root=ROOT):
    inputs = Inputs(root)
    registry = inputs.json('docs/FINAL_ARTIFACTS.json')
    experiments = {(row['model'], row['regime']): row for row in registry['experiments']}
    complexity = inputs.json(registry['source_complexity'])
    target_raw = inputs.csv(registry['indonesia_evaluation']['per_class'])
    paper = inputs.path(registry['manuscripts']['source_paper']).read_text()
    overlaps = {row['model']: int(row['n_true']) for row in inputs.csv('runs/rdd_yolov8n_local/fp_overlap_6cls_vs_4cls_test.csv')}
    tables = {key: [] for key in ['source_six_class', 'source_per_class', 'transfer_four_class', 'target_per_class',
                                    'ablation_four_vs_six', 'country_four_class', 'supplementary_five_class', 'training_configuration']}
    for model in MODELS:
        six, four = experiments[model, 'source_six'], experiments[model, 'source_four']
        source = per_class(inputs.csv(six['test_per_class']), model)
        ablation = per_class(inputs.csv(four['test_per_class']), model)
        target = per_class(target_raw, model)
        source_all = aggregate(source, range(6))
        if source_all['support'] != 2425 or sum(row['support'] for row in ablation) != 2035:
            raise ValueError(f'Source inventory mismatch: {model}')
        if sum(row['support'] for row in target) != 502 or aggregate(target, range(4))['support'] != 481:
            raise ValueError(f'Target V4 inventory mismatch: {model}')
        if target[4]['evaluated'] or target[4]['support'] != 0:
            raise ValueError('Target manhole must be unevaluated, not assigned AP=0.')
        summary = inputs.json(six['summary'])
        if not math.isclose(source_all['mAP50'], summary['test_results']['metrics/mAP50(B)'], abs_tol=1e-10):
            raise ValueError(f'Source mAP disagrees with the final run summary: {model}')
        timing = summary['test_speed_ms_per_image']
        fps = 1000 / sum(timing[key] for key in ['preprocess', 'inference', 'postprocess'])
        if not math.isclose(fps, summary['test_fps_estimate'], abs_tol=.01):
            raise ValueError('Archived throughput does not match its recorded timing components.')
        curve = inputs.csv(six['training_curve'])
        best = max(curve, key=lambda row: float(row['metrics/mAP50-95(B)']))
        tables['source_six_class'].append({'model': model, **source_all,
            'params_M_fused': complexity['models'][model]['params_M'], 'GFLOPs_fused': complexity['models'][model]['gflops'],
            'FPS_archived': fps, 'best_epoch': int(best['epoch']), 'total_epochs': int(curve[-1]['epoch']),
            'training_hours': float(curve[-1]['time']) / 3600})
        tables['source_per_class'].extend(source)
        tables['target_per_class'].extend(target)
        tables['transfer_four_class'].append(comparison(model, source, target, range(4)))
        tables['supplementary_five_class'].append(comparison(model, source, target, [0,1,2,3,5]))
        before, after = aggregate(source, range(4)), aggregate(ablation, range(4))
        tables['ablation_four_vs_six'].append({'model': model, 'six_class_training_mAP50': before['mAP50'],
            'four_class_training_mAP50': after['mAP50'], 'delta_four_minus_six': after['mAP50'] - before['mAP50'],
            'six_class_pothole_AP50': source[3]['mAP50'], 'four_class_pothole_AP50': ablation[3]['mAP50'],
            'six_class_pothole_overlap_boxes': overlaps[model+'_6cls'], 'four_class_pothole_overlap_boxes': overlaps[model+'_4cls']})
        for regime, experiment in [('source_six', six), ('source_four', four)]:
            args = inputs.yaml(experiment['args'])
            tables['training_configuration'].append({'model': model, 'regime': regime, 'args_path': experiment['args'],
                **{key: args[key] for key in ['epochs','patience','batch','imgsz','optimizer','seed','amp','workers',
                   'warmup_bias_lr','weight_decay','cos_lr','mosaic','mixup','fliplr','translate','scale','degrees']}})
    tables['country_four_class'] = country_table(paper)
    return tables, inputs, complexity['protocol']


def write_csv(path, rows):
    with path.open('w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def save_figure(fig, name):
    fig.savefig(FIGURES / (name+'.png'), dpi=180, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def heatmap(rows, ids, title, name):
    array = np.array([[next(row['mAP50'] for row in rows if row['model']==model and row['class_id']==cid) for cid in ids] for model in MODELS])
    fig, ax = plt.subplots(figsize=(10,3.8), layout='constrained')
    image = ax.imshow(array, vmin=0, vmax=1, cmap='Blues', aspect='auto')
    ax.set_xticks(range(len(ids)), [CODES[cid]+'\n'+NAMES[cid].replace('_',' ') for cid in ids], fontsize=9)
    ax.set_yticks(range(5), [DISPLAY[model] for model in MODELS])
    for i in range(5):
        for j in range(len(ids)):
            ax.text(j,i,f'{array[i,j]:.3f}',ha='center',va='center',color='white' if array[i,j]>.6 else '#152d46')
    ax.set_title(title, loc='left', pad=15)
    fig.colorbar(image, ax=ax, label='AP@0.5', shrink=.9)
    save_figure(fig,name)


def draw_figures(tables):
    FIGURES.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False})
    labels = [DISPLAY[model] for model in MODELS]
    for name, title, table in [('transfer_four_class','Primary transfer: the same four damage classes','transfer_four_class'),
                                ('supplementary_five_class','Supplement: five shared classes, including patchy road','supplementary_five_class')]:
        rows=tables[table];x=np.arange(5)
        fig,ax=plt.subplots(figsize=(9,4.6),layout='constrained')
        for offset,key,label,color in [(-.19,'source_mAP50','Source test','#315c83'),(.19,'target_mAP50','Indonesia V4: zero-shot','#e58a38')]:
            bars=ax.bar(x+offset,[row[key] for row in rows],width=.36,label=label,color=color)
            ax.bar_label(bars,fmt='%.3f',padding=3,fontsize=10)
        ax.set_xticks(x,labels);ax.set_ylim(0,.86);ax.set_ylabel('mAP@0.5');ax.set_title(title,loc='left',pad=16)
        ax.legend(frameon=False,loc='upper right');ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True)
        save_figure(fig,name)
    rows=tables['source_six_class']
    fig,ax=plt.subplots(figsize=(8,4.2),layout='constrained')
    bars=ax.bar(labels,[row['mAP50'] for row in rows],color=COLORS)
    ax.bar_label(bars,fmt='%.3f',padding=3);ax.set_ylim(0,.78)
    ax.set_ylabel('mAP@0.5 (six classes)');ax.set_title('Source test: 995 images',loc='left',pad=14)
    ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True);save_figure(fig,'source_accuracy')
    heatmap(tables['source_per_class'],range(6),'Source-test AP by class','source_per_class')
    heatmap(tables['target_per_class'],[0,1,2,3,5],'Indonesia V4 AP by class (manhole has no ground truth)','target_per_class')
    rows=tables['ablation_four_vs_six'];x=np.arange(5)
    fig,ax=plt.subplots(figsize=(9,4.4),layout='constrained')
    for offset,key,label,color in [(-.19,'six_class_training_mAP50','Six-class training','#315c83'),(.19,'four_class_training_mAP50','Four-class training','#458b66')]:
        bars=ax.bar(x+offset,[row[key] for row in rows],width=.36,label=label,color=color)
        ax.bar_label(bars,fmt='%.4f',padding=3,fontsize=9)
    ax.set_xticks(x,labels);ax.set_ylim(0,.84);ax.set_ylabel('mAP@0.5 (same four damage classes)')
    ax.set_title('Training-label ablation on the source test',loc='left',pad=16);ax.legend(frameon=False,loc='upper right')
    ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True);save_figure(fig,'ablation_four_vs_six')
    rows=tables['country_four_class'];array=np.array([[row[c] for c in ['China','Japan','India']] for row in rows])
    fig,ax=plt.subplots(figsize=(8,3.6),layout='constrained')
    image=ax.imshow(array,vmin=0,vmax=1,cmap='Blues',aspect='auto')
    ax.set_xticks(range(3),['China (180 images)','Japan (705)','India (110)']);ax.set_yticks(range(5),labels)
    for i in range(5):
        for j in range(3):ax.text(j,i,f'{array[i,j]:.3f}',ha='center',va='center',color='white' if array[i,j]>.6 else '#152d46')
    ax.set_title('Country subsets: the same four damage classes',loc='left',pad=15)
    fig.colorbar(image,ax=ax,label='mAP@0.5');save_figure(fig,'country_four_class')
    rows=tables['source_six_class'];fig,ax=plt.subplots(figsize=(8,4.8),layout='constrained')
    for row,color in zip(rows,COLORS):
        ax.scatter(row['FPS_archived'],row['mAP50'],s=row['params_M_fused']*65,color=color,alpha=.85,edgecolor='white',linewidth=1)
        ax.annotate(DISPLAY[row['model']],(row['FPS_archived'],row['mAP50']),xytext=(0,12),textcoords='offset points',ha='center',fontsize=10)
    ax.set_xlim(155,405);ax.set_ylim(.61,.68);ax.set_xlabel('Archived GPU throughput estimate (FPS)')
    ax.set_ylabel('Source mAP@0.5 (six classes)');ax.set_title('Accuracy / throughput; bubble size = fused parameters',loc='left',pad=14)
    ax.grid(alpha=.2);ax.set_axisbelow(True)
    fig.text(.13,-.025,'RTX 4070 SUPER, 640 px; preprocess + inference + postprocess. Not an edge benchmark.',fontsize=9)
    save_figure(fig,'efficiency_tradeoff')


def md_table(headers, rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','|'+'|'.join('---' for _ in headers)+'|']+
                     ['| '+' | '.join(map(str,row))+' |' for row in rows])


def per_class_table(rows, ids):
    return md_table(['Model']+[CODES[cid] for cid in ids],
                    [[DISPLAY[model]]+[f"{next(row['mAP50'] for row in rows if row['model']==model and row['class_id']==cid):.3f}" for cid in ids] for model in MODELS])


def markdown(tables, complexity_protocol):
    source=tables['source_six_class'];transfer=tables['transfer_four_class'];ablation=tables['ablation_four_vs_six']
    lines=['# Hasil final — tabel acuan penelitian','',
      'Dibangun dari artefak final yang dipilih di [FINAL_ARTIFACTS.json](FINAL_ARTIFACTS.json), bukan dari konstanta notebook atau angka yang diketik ulang. '
      'Generator hanya menghitung ulang agregasi CSV dan membuat visual; tidak menjalankan training atau inferensi. '
      '[RESULTS.md](RESULTS.md) tetap menjadi log mentah historis.','',
      '**Pisahkan cakupan:** overall sumber memakai enam kelas; transfer utama, ablasi dan perbandingan negara memakai empat kelas kerusakan yang sama. '
      'Analisis lima kelas bersama disajikan terpisah sebagai tambahan. Semua hasil berasal dari satu seed per konfigurasi.','',
      '## Data dan protokol','',
      '- Sumber: N-RDD2024 Asia, split train/val/test 6.777/1.898/995 gambar. Uji sumber enam kelas memiliki 2.425 anotasi; versi empat kelas memiliki 2.035 anotasi pada gambar uji yang sama.',
      '- Target final: Roboflow `rdd-indo-crop` **versi 4**, folder `data/RDD-indo-v4`, split `valid` sebagai uji target: **307 gambar, 502 anotasi, 39 gambar tanpa anotasi**. Empat kelas kerusakan menyumbang 481 anotasi; patchy road 21; manhole tidak memiliki GT.',
      '- Zero-shot berarti menerapkan checkpoint enam kelas tanpa fine-tuning pada target. Seluruh gambar target dan keluaran enam kelas model dipertahankan; agregasi utama memakai ID sumber 0–3.',
      '- Evaluasi AP: imgsz 640, confidence minimum 0,001, NMS IoU 0,6 bila berlaku. Confidence tampilan contoh prediksi 0,25 adalah pengaturan yang berbeda.',
      '- F1 makro berasal dari P/R per kelas pada ambang Ultralytics yang memaksimalkan mean-F1 pada evaluasi asli masing-masing split; bukan F1 pada confidence tampilan 0,25. Agregasi empat/lima kelas memakai P/R yang sudah tersimpan, tanpa memilih ulang threshold khusus subset.',
      '- Kelas tanpa GT tidak dievaluasi dan tidak diisi AP=0. Mapping target→sumber tetap `{0:2, 1:0, 2:5, 3:3, 4:1}`.','',
      '## Sumber: uji enam kelas','',
      md_table(['Model','Presisi','Recall','mAP@0,5','mAP@0,5:0,95','F1 makro','F1 berbobot'],
       [[DISPLAY[row['model']]]+[f'{row[key]:.3f}' for key in ['precision','recall','mAP50','mAP50-95','f1','weighted_f1']] for row in source]),'',
      '![Akurasi sumber](figures/final_results/source_accuracy.png)','',
      'YOLO-RD memperoleh mAP@0,5 sumber tertinggi pada run ini (0,661). mAP@0,5:0,95 YOLO-RD dan YOLOv12n sama-sama membulat menjadi 0,371. '
      'Kedua model custom adalah reimplementasi lokal; peringkat ini bukan bukti superioritas statistik atau efek arsitektur yang terisolasi.','',
      '### AP@0,5 per kelas sumber','',per_class_table(tables['source_per_class'],range(6)),'',
      'D00: longitudinal crack; D10: transverse crack; D20: alligator crack; D40: pothole; D70: manhole; D80: patchy road.','',
      '![AP sumber per kelas](figures/final_results/source_per_class.png)','',
      '## Transfer utama: empat kelas kerusakan yang sama','',
      md_table(['Model','Sumber mAP@0,5','Target V4 mAP@0,5','Selisih (pp)','Penurunan relatif'],
       [[DISPLAY[row['model']],f"{row['source_mAP50']:.3f}",f"{row['target_mAP50']:.3f}",f"{row['absolute_drop_pp']:.2f}",f"{row['relative_drop_pct']:.1f}%"] for row in transfer]),'',
      'Penurunan relatif = `100 × (1 − target/source)`, dihitung dari AP per kelas tanpa membulatkan terlebih dahulu. '
      'Selisih dalam percentage points (pp) adalah `100 × (source − target)`. Angka sumber di bagian ini berbeda dari overall enam kelas karena cakupannya empat kelas.','',
      '![Transfer empat kelas](figures/final_results/transfer_four_class.png)','',
      'YOLOv12n memiliki mAP@0,5 target tertinggi (0,413) dan penurunan relatif terkecil (34,1%). '
      'Perubahan peringkat sumber→target menggambarkan hasil pada dua dataset ini; besarnya penurunan bukan ukuran kausal tekstur, pencahayaan atau lokasi.','',
      '### F1 pada empat kelas yang sama','',
      md_table(['Model','F1 makro sumber','F1 makro target','F1 berbobot sumber','F1 berbobot target'],
       [[DISPLAY[row['model']]]+[f'{row[key]:.3f}' for key in ['source_macro_f1','target_macro_f1','source_weighted_f1','target_weighted_f1']] for row in transfer]),'',
      '### AP@0,5 per kelas target','',per_class_table(tables['target_per_class'],[0,1,2,3,5]),'',
      'D80 dipertahankan sebagai informasi tambahan; tidak dimasukkan ke agregat utama empat kelas.','',
      '![AP target per kelas](figures/final_results/target_per_class.png)','',
      '## Ablasi: training enam versus empat kelas','',
      'Kedua rezim dinilai pada empat kelas kerusakan yang sama dan gambar sumber yang sama.','',
      md_table(['Model','Training 6 kelas','Training 4 kelas','Δ (4 − 6)','Overlap pothole 6 / 4'],
       [[DISPLAY[row['model']],f"{row['six_class_training_mAP50']:.4f}",f"{row['four_class_training_mAP50']:.4f}",f"{row['delta_four_minus_six']:+.4f}",f"{row['six_class_pothole_overlap_boxes']} / {row['four_class_pothole_overlap_boxes']}"] for row in ablation]),'',
      '![Ablasi label](figures/final_results/ablation_four_vs_six.png)','',
      'Penambahan label manhole/patchy road tidak menunjukkan manfaat yang konsisten untuk mAP empat kelas pada run ini. '
      'Overlap adalah **jumlah kotak prediksi pothole**, confidence ≥0,25, yang bertumpang tindih dengan minimal satu GT distractor pada IoU ≥0,5; bukan false-positive rate objek dengan matching unik. '
      'Terdapat 390 GT distractor (321 manhole + 69 patchy); jumlah kecil ini tidak mendukung klaim signifikansi dari proxy lama.','',
      '## Negara sumber: empat kelas kerusakan bersama','',
      md_table(['Model','China (180 gambar)','Japan (705)','India (110)'],
       [[DISPLAY[row['model']]]+[f'{row[key]:.3f}' for key in ['China','Japan','India']] for row in tables['country_four_class']]),'',
      'Nilai diturunkan dari tabel `country-four` pada [source paper](../latex/IEEE-Conference/main.tex) **pada presisi pelaporan tiga desimal**; '
      'generator tidak mengarang digit tambahan atau menghitungnya dari AP per kelas yang sudah dibulatkan. '
      'Ketiga negara ada dalam training. India memiliki hanya enam instance transverse-crack pada test; komposisi/ukuran subgroup membatasi interpretasi.', '',
      '![Perbandingan negara](figures/final_results/country_four_class.png)','',
      '## Kompleksitas, throughput dan biaya training','',
      md_table(['Model','Params fused (M)','GFLOPs','FPS arsip','Training (jam)','Epoch terbaik / akhir'],
       [[DISPLAY[row['model']],f"{row['params_M_fused']:.3f}",f"{row['GFLOPs_fused']:.1f}",f"{row['FPS_archived']:.1f}",f"{row['training_hours']:.1f}",f"{row['best_epoch']} / {row['total_epochs']}"] for row in source]),'',
      f'Kompleksitas mengikuti audit tersimpan: `{complexity_protocol}`. Jumlah parameter dalam juta hanya tersedia pada presisi audit tiga desimal; tidak diubah menjadi hitungan parameter eksak. '
      'Ini menggantikan nilai unfused/legacy yang tercampur pada tabel lama. FPS dibentuk dari jumlah waktu preprocess + inference + postprocess pada test, '
      'dengan RTX 4070 SUPER 12 GB, imgsz 640, Ultralytics 8.4.108, PyTorch 2.5.1+CUDA 12.1 sebagaimana dicatat pada log penelitian. '
      'Throughput ini bukan benchmark perangkat edge. Waktu training dan epoch berhenti berbeda antar run, sehingga tidak mengisolasi biaya arsitektur saja.','',
      '![Trade-off sumber](figures/final_results/efficiency_tradeoff.png)','',
      '## Konfigurasi training aktual','',
      md_table(['Model','Rezim','Batch','Max epoch','Patience','Seed','AMP','Workers','Warmup bias LR'],
       [[DISPLAY[row['model']],row['regime'],row['batch'],row['epochs'],row['patience'],row['seed'],str(row['amp']),row['workers'],row['warmup_bias_lr']] for row in tables['training_configuration']]),'',
      'Konfigurasi diambil dari `args.yaml`, bukan sel notebook. Seluruh run memakai input 640, optimizer `auto`, weight decay 0,0005, '
      'Mosaic 1,0, MixUp 0,05, flip horizontal 0,5, translate 0,1, scale 0,5, dan rotasi 0. '
      'Intervensi imbalance yang terverifikasi adalah bobot kelas effective-number (β=0,999) pada BCE klasifikasi, **bukan Focal Loss**. '
      'AMP pada custom empat kelas berbeda dari enam kelas; RD empat kelas juga berbeda pada workers dan warmup bias LR. '
      'Perbedaan initialization/pretrained transfer dan pengaturan tersebut membatasi klaim sebab-akibat. '
      'Kurva training PD empat kelas tidak tersedia; tidak disubstitusi dengan run lain.','',
      '## Tambahan: lima kelas bersama','',
      'Bagian ini mencakup D00, D10, D20, D40 dan D80. Manhole dikeluarkan dari kedua domain. '
      'Nilai target 0,337 untuk YOLOv12n tetap benar untuk **lima kelas**; tidak bertentangan dengan hasil utama empat kelas 0,413.','',
      md_table(['Model','Sumber 5 kelas','Target V4 5 kelas','Penurunan relatif','F1 makro sumber / target','F1 berbobot sumber / target'],
       [[DISPLAY[row['model']],f"{row['source_mAP50']:.3f}",f"{row['target_mAP50']:.3f}",f"{row['relative_drop_pct']:.1f}%",f"{row['source_macro_f1']:.3f} / {row['target_macro_f1']:.3f}",f"{row['source_weighted_f1']:.3f} / {row['target_weighted_f1']:.3f}"] for row in tables['supplementary_five_class']]),'',
      '![Tambahan lima kelas](figures/final_results/supplementary_five_class.png)','',
      '## Sumber, reproduksi dan batas pembaruan','',
      '- Jalankan `python scripts/build_final_results.py`. Entry point lama `python scripts/paper/paper_figs_summary.py` sekarang memanggil generator yang sama dan tidak menimpa gambar LaTeX.',
      '- [Daftar artefak final](FINAL_ARTIFACTS.json) memilih bobot, args dan CSV; [keluaran CSV/JSON](../runs/rdd_yolov8n_local/evaluation/final_report/) menyimpan tabel tanpa pembulatan dan `provenance.json` berisi SHA-256 input.',
      '- [Versi tabel sebelum pembaruan](archive/content-before-update/docs/RESULTS_TABLE.md) dan [generator lama](archive/content-before-update/scripts/paper/paper_figs_summary.py) dipertahankan tanpa perubahan byte.',
      '- Validasi tidak dicampur dengan hasil test. Tabel validasi dan ekspor Indonesia lama tersedia sebagai bukti historis, bukan hasil utama alternatif.',
      '- Notebook, source/PDF LaTeX, CSV run asli dan log mentah tidak diubah oleh generator. Penghitungan ulang UMAP/V4 merupakan pipeline terpisah dan tidak dipalsukan dengan mengganti label grafik V2.',
      '- Semua perbandingan model masih single-seed tanpa confidence interval/uji signifikansi. Sampel target lokal dan satu annotator membatasi generalisasi.', '']
    return '\n'.join(lines)


def main():
    tables, inputs, protocol = build_tables()
    REPORT.mkdir(parents=True, exist_ok=True)
    for name, rows in tables.items():
        write_csv(REPORT/(name+'.csv'),rows)
    draw_figures(tables)
    (ROOT/'docs/RESULTS_TABLE.md').write_text(markdown(tables,protocol))
    provenance={'generator':'scripts/build_final_results.py','inference_run':False,
        'primary_class_ids':[0,1,2,3],'supplementary_class_ids':[0,1,2,3,5],
        'country_precision':'Manuscript table country-four, three reported decimal places; no added precision.',
        'input_files':[{'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()} for path in sorted(inputs.paths)],
        'output_tables':list(tables),'output_figures':[path.name for path in sorted(FIGURES.glob('*.png'))]}
    (REPORT/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
    print(f'Generated {len(tables)} tables, 8 figures and docs/RESULTS_TABLE.md; no training/inference.')


if __name__=='__main__':
    main()
