
Evaluasi yolov8n_class_weight — val
Ultralytics 8.4.108  Python-3.12.3 torch-2.5.1+cu121 CUDA:0 (NVIDIA GeForce RTX 4070 SUPER, 12282MiB)
Model summary (fused): 73 layers, 3,006,818 parameters, 0 gradients, 8.1 GFLOPs
val: Fast image access  (ping: 0.00.0 ms, read: 1088.2282.4 MB/s, size: 79.8 KB)
val: Scanning D:\Faaris\Project-TA\road-damage-detection-ta\data\NRDD-2024\RDD_Split_Final_china_japan_india_6_classes\RDD_Split_Final_china_japan_india_6_classes\val\labels.cache... 1898 images, 0 backgrounds, 0 corrupt: 100% ━━━━━━━━━━━━ 1898/1898  0.0s
val: D:\Faaris\Project-TA\road-damage-detection-ta\data\NRDD-2024\RDD_Split_Final_china_japan_india_6_classes\RDD_Split_Final_china_japan_india_6_classes\val\images\Japan_006916_jpg.rf.6409c53af3c26b4c760f816734ecafc8.jpg: 1 duplicate labels removed
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 119/119 8.0it/s 14.9s0.1s
                   all       1898       4772      0.684      0.598      0.657      0.365
    Longitudinal_Crack        788       1257      0.687      0.571      0.637      0.353
      Transverse_Crack        532        897      0.626      0.518      0.586      0.273
       Alligator_Crack        960       1245      0.688      0.607      0.684      0.357
               Pothole        354        597      0.692      0.484       0.57      0.248
               manhole        469        644      0.767      0.764      0.801      0.427
           patchy_road        104        132      0.645      0.644      0.665      0.529
Speed: 0.3ms preprocess, 2.0ms inference, 0.0ms loss, 0.5ms postprocess per image
Saving D:\Faaris\Project-TA\road-damage-detection-ta\runs\rdd_yolov8n_local\evaluation\yolov8n_class_weight_val\predictions.json...
Results saved to D:\Faaris\Project-TA\road-damage-detection-ta\runs\rdd_yolov8n_local\evaluation\yolov8n_class_weight_val

Evaluasi yolov8n_class_weight — test
Ultralytics 8.4.108  Python-3.12.3 torch-2.5.1+cu121 CUDA:0 (NVIDIA GeForce RTX 4070 SUPER, 12282MiB)
WARNING val: Slow image access detected (ping: 0.10.0 ms, read: 16.71.3 MB/s, size: 79.9 KB). Use local storage instead of remote/mounted storage for better performance. See https://docs.ultralytics.com/guides/model-training-tips/
val: Scanning D:\Faaris\Project-TA\road-damage-detection-ta\data\NRDD-2024\RDD_Split_Final_china_japan_india_6_classes\RDD_Split_Final_china_japan_india_6_classes\test\labels.cache... 995 images, 0 backgrounds, 0 corrupt: 100% ━━━━━━━━━━━━ 995/995  0.0s
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 63/63 4.3it/s 14.6s0.2s
                   all        995       2425      0.643      0.599      0.648      0.364
    Longitudinal_Crack        395        635      0.686      0.594      0.664      0.375
      Transverse_Crack        266        446      0.625      0.522      0.599       0.28
       Alligator_Crack        480        642      0.697      0.637        0.7      0.371
               Pothole        177        312      0.623      0.471      0.526      0.225
               manhole        234        321      0.775      0.816      0.825      0.473
           patchy_road         52         69      0.451      0.551      0.571      0.461
Speed: 0.3ms preprocess, 3.7ms inference, 0.0ms loss, 0.6ms postprocess per image
Saving D:\Faaris\Project-TA\road-damage-detection-ta\runs\rdd_yolov8n_local\evaluation\yolov8n_class_weight_test\predictions.json...
Results saved to D:\Faaris\Project-TA\road-damage-detection-ta\runs\rdd_yolov8n_local\evaluation\yolov8n_class_weight_test
  val  mAP50: 0.6571
  test mAP50: 0.6476

Evaluasi yolov12n_class_weight — val
Ultralytics 8.4.108  Python-3.12.3 torch-2.5.1+cu121 CUDA:0 (NVIDIA GeForce RTX 4070 SUPER, 12282MiB)
YOLOv12n summary (fused): 159 layers, 2,557,898 parameters, 0 gradients, 6.3 GFLOPs
val: Fast image access  (ping: 0.00.0 ms, read: 1154.5357.5 MB/s, size: 74.7 KB)
val: Scanning D:\Faaris\Project-TA\road-damage-detection-ta\data\NRDD-2024\RDD_Split_Final_china_japan_india_6_classes\RDD_Split_Final_china_japan_india_6_classes\val\labels.cache... 1898 images, 0 backgrounds, 0 corrupt: 100% ━━━━━━━━━━━━ 1898/1898  0.0s
val: D:\Faaris\Project-TA\road-damage-detection-ta\data\NRDD-2024\RDD_Split_Final_china_japan_india_6_classes\RDD_Split_Final_china_japan_india_6_classes\val\images\Japan_006916_jpg.rf.6409c53af3c26b4c760f816734ecafc8.jpg: 1 duplicate labels removed
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 119/119 8.2it/s 14.5s0.1s
                   all       1898       4772      0.669        0.6      0.656      0.368
    Longitudinal_Crack        788       1257      0.698      0.578      0.656      0.363
      Transverse_Crack        532        897       0.59      0.543      0.595      0.281
       Alligator_Crack        960       1245      0.677      0.614      0.672      0.361
               Pothole        354        597      0.649      0.486      0.568       0.25
               manhole        469        644      0.771      0.766      0.791       0.42
           patchy_road        104        132      0.629      0.614      0.654      0.534
Speed: 0.3ms preprocess, 2.0ms inference, 0.0ms loss, 0.5ms postprocess per image
Saving D:\Faaris\Project-TA\road-damage-detection-ta\runs\rdd_yolov8n_local\evaluation\yolov12n_class_weight_val\predictions.json...
Results saved to D:\Faaris\Project-TA\road-damage-detection-ta\runs\rdd_yolov8n_local\evaluation\yolov12n_class_weight_val

Evaluasi yolov12n_class_weight — test
Ultralytics 8.4.108  Python-3.12.3 torch-2.5.1+cu121 CUDA:0 (NVIDIA GeForce RTX 4070 SUPER, 12282MiB)
val: Fast image access  (ping: 0.00.0 ms, read: 1009.1299.1 MB/s, size: 81.6 KB)
val: Scanning D:\Faaris\Project-TA\road-damage-detection-ta\data\NRDD-2024\RDD_Split_Final_china_japan_india_6_classes\RDD_Split_Final_china_japan_india_6_classes\test\labels.cache... 995 images, 0 backgrounds, 0 corrupt: 100% ━━━━━━━━━━━━ 995/995  0.0s
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 63/63 7.8it/s 8.1s0.1s
                   all        995       2425      0.638      0.608      0.654      0.371
    Longitudinal_Crack        395        635      0.681      0.587       0.68      0.399
      Transverse_Crack        266        446       0.59      0.565      0.582      0.282
       Alligator_Crack        480        642      0.699      0.645      0.708       0.38
               Pothole        177        312      0.626      0.458      0.535      0.222
               manhole        234        321      0.764      0.826      0.833      0.467
           patchy_road         52         69       0.47      0.565      0.587      0.478
Speed: 0.3ms preprocess, 2.4ms inference, 0.0ms loss, 0.5ms postprocess per image
Saving D:\Faaris\Project-TA\road-damage-detection-ta\runs\rdd_yolov8n_local\evaluation\yolov12n_class_weight_test\predictions.json...
Results saved to D:\Faaris\Project-TA\road-damage-detection-ta\runs\rdd_yolov8n_local\evaluation\yolov12n_class_weight_test
  val  mAP50: 0.6560
  test mAP50: 0.6542

  
Evaluasi yolov26n_class_weight — val
Ultralytics 8.4.108  Python-3.12.3 torch-2.5.1+cu121 CUDA:0 (NVIDIA GeForce RTX 4070 SUPER, 12282MiB)
YOLO26n summary (fused): 122 layers, 2,376,006 parameters, 0 gradients, 5.2 GFLOPs
WARNING val: Slow image access detected (ping: 0.00.0 ms, read: 13.80.3 MB/s, size: 76.8 KB). Use local storage instead of remote/mounted storage for better performance. See https://docs.ultralytics.com/guides/model-training-tips/
val: Scanning D:\Faaris\Project-TA\road-damage-detection-ta\data\NRDD-2024\RDD_Split_Final_china_japan_india_6_classes\RDD_Split_Final_china_japan_india_6_classes\val\labels.cache... 1898 images, 0 backgrounds, 0 corrupt: 100% ━━━━━━━━━━━━ 1898/1898  0.0s
val: D:\Faaris\Project-TA\road-damage-detection-ta\data\NRDD-2024\RDD_Split_Final_china_japan_india_6_classes\RDD_Split_Final_china_japan_india_6_classes\val\images\Japan_006916_jpg.rf.6409c53af3c26b4c760f816734ecafc8.jpg: 1 duplicate labels removed
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 119/119 4.6it/s 25.7s0.2s
                   all       1898       4772      0.681      0.572      0.633       0.36
    Longitudinal_Crack        788       1257      0.708      0.558      0.625      0.358
      Transverse_Crack        532        897       0.59      0.491      0.544      0.261
       Alligator_Crack        960       1245       0.69      0.587      0.654       0.35
               Pothole        354        597      0.671      0.491       0.55      0.241
               manhole        469        644      0.736      0.716      0.772      0.417
           patchy_road        104        132      0.688      0.591      0.654      0.532
Speed: 0.3ms preprocess, 3.2ms inference, 0.0ms loss, 0.1ms postprocess per image
Saving D:\Faaris\Project-TA\road-damage-detection-ta\runs\rdd_yolov8n_local\evaluation\yolov26n_class_weight_val\predictions.json...
Results saved to D:\Faaris\Project-TA\road-damage-detection-ta\runs\rdd_yolov8n_local\evaluation\yolov26n_class_weight_val

Evaluasi yolov26n_class_weight — test
Ultralytics 8.4.108  Python-3.12.3 torch-2.5.1+cu121 CUDA:0 (NVIDIA GeForce RTX 4070 SUPER, 12282MiB)
WARNING val: Slow image access detected (ping: 0.10.0 ms, read: 16.36.1 MB/s, size: 82.2 KB). Use local storage instead of remote/mounted storage for better performance. See https://docs.ultralytics.com/guides/model-training-tips/
val: Scanning D:\Faaris\Project-TA\road-damage-detection-ta\data\NRDD-2024\RDD_Split_Final_china_japan_india_6_classes\RDD_Split_Final_china_japan_india_6_classes\test\labels.cache... 995 images, 0 backgrounds, 0 corrupt: 100% ━━━━━━━━━━━━ 995/995  0.0s
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 63/63 4.4it/s 14.3s0.2s
                   all        995       2425      0.642       0.58      0.625      0.358
    Longitudinal_Crack        395        635      0.678      0.557      0.639       0.37
      Transverse_Crack        266        446      0.609        0.5      0.567       0.29
       Alligator_Crack        480        642      0.698      0.626      0.675      0.367
               Pothole        177        312      0.637      0.455      0.538      0.232
               manhole        234        321       0.76      0.804       0.82      0.463
           patchy_road         52         69      0.469      0.536      0.512      0.425
Speed: 0.3ms preprocess, 3.0ms inference, 0.0ms loss, 0.1ms postprocess per image
Saving D:\Faaris\Project-TA\road-damage-detection-ta\runs\rdd_yolov8n_local\evaluation\yolov26n_class_weight_test\predictions.json...
Results saved to D:\Faaris\Project-TA\road-damage-detection-ta\runs\rdd_yolov8n_local\evaluation\yolov26n_class_weight_test
  val  mAP50: 0.6331
  test mAP50: 0.6251

Evaluasi yolov8_pd_class_weight — val
Ultralytics 8.4.108  Python-3.12.3 torch-2.5.1+cu121 CUDA:0 (NVIDIA GeForce RTX 4070 SUPER, 12282MiB)
YOLOv8-pd summary: 156 layers, 2,468,085 parameters, 0 gradients, 7.6 GFLOPs
val: Fast image access  (ping: 0.00.0 ms, read: 1163.3340.5 MB/s, size: 80.7 KB)
val: Scanning D:\Faaris\Project-TA\road-damage-detection-ta\data\NRDD-2024\RDD_Split_Final_china_japan_india_6_classes\RDD_Split_Final_china_japan_india_6_classes\val\labels.cache... 1898 images, 0 backgrounds, 0 corrupt: 100% ━━━━━━━━━━━━ 1898/1898  0.0s
val: D:\Faaris\Project-TA\road-damage-detection-ta\data\NRDD-2024\RDD_Split_Final_china_japan_india_6_classes\RDD_Split_Final_china_japan_india_6_classes\val\images\Japan_006916_jpg.rf.6409c53af3c26b4c760f816734ecafc8.jpg: 1 duplicate labels removed
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 119/119 7.9it/s 15.0s0.1s
                   all       1898       4772      0.677      0.604      0.651      0.366
    Longitudinal_Crack        788       1257      0.685      0.592      0.656       0.37
      Transverse_Crack        532        897      0.633       0.54      0.593      0.278
       Alligator_Crack        960       1245      0.666      0.606      0.663      0.345
               Pothole        354        597      0.626        0.5      0.555      0.247
               manhole        469        644      0.765      0.758      0.785      0.423
           patchy_road        104        132      0.686      0.628      0.655      0.532
Speed: 0.3ms preprocess, 1.9ms inference, 0.0ms loss, 0.5ms postprocess per image
Saving D:\Faaris\Project-TA\road-damage-detection-ta\runs\rdd_yolov8n_local\evaluation\yolov8_pd_class_weight_val\predictions.json...
Results saved to D:\Faaris\Project-TA\road-damage-detection-ta\runs\rdd_yolov8n_local\evaluation\yolov8_pd_class_weight_val

Evaluasi yolov8_pd_class_weight — test
Ultralytics 8.4.108  Python-3.12.3 torch-2.5.1+cu121 CUDA:0 (NVIDIA GeForce RTX 4070 SUPER, 12282MiB)
YOLOv8-pd summary: 156 layers, 2,468,085 parameters, 0 gradients, 7.6 GFLOPs
val: Fast image access  (ping: 0.00.0 ms, read: 744.7342.0 MB/s, size: 55.5 KB)
val: Scanning D:\Faaris\Project-TA\road-damage-detection-ta\data\NRDD-2024\RDD_Split_Final_china_japan_india_6_classes\RDD_Split_Final_china_japan_india_6_classes\test\labels.cache... 995 images, 0 backgrounds, 0 corrupt: 100% ━━━━━━━━━━━━ 995/995  0.0s
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 63/63 7.8it/s 8.0s0.1s
                   all        995       2425      0.675      0.591      0.646      0.362
    Longitudinal_Crack        395        635      0.723      0.591      0.678      0.385
      Transverse_Crack        266        446      0.623        0.5      0.572      0.278
       Alligator_Crack        480        642      0.705      0.638      0.702      0.371
               Pothole        177        312      0.684      0.457      0.541      0.226
               manhole        234        321      0.768       0.81      0.819      0.467
           patchy_road         52         69      0.546      0.551      0.562      0.444
Speed: 0.3ms preprocess, 1.9ms inference, 0.0ms loss, 0.5ms postprocess per image
Saving D:\Faaris\Project-TA\road-damage-detection-ta\runs\rdd_yolov8n_local\evaluation\yolov8_pd_class_weight_test\predictions.json...
Results saved to D:\Faaris\Project-TA\road-damage-detection-ta\runs\rdd_yolov8n_local\evaluation\yolov8_pd_class_weight_test
  val  mAP50: 0.6510
  test mAP50: 0.6457

Evaluasi yolo_rd_class_weight — val
Ultralytics 8.4.108  Python-3.12.3 torch-2.5.1+cu121 CUDA:0 (NVIDIA GeForce RTX 4070 SUPER, 12282MiB)
YOLO-rd summary: 163 layers, 7,086,104 parameters, 0 gradients, 12.8 GFLOPs
val: Fast image access  (ping: 0.00.0 ms, read: 1026.9136.9 MB/s, size: 76.2 KB)
val: Scanning D:\Faaris\Project-TA\road-damage-detection-ta\data\NRDD-2024\RDD_Split_Final_china_japan_india_6_classes\RDD_Split_Final_china_japan_india_6_classes\val\labels.cache... 1898 images, 0 backgrounds, 0 corrupt: 100% ━━━━━━━━━━━━ 1898/1898  0.0s
val: D:\Faaris\Project-TA\road-damage-detection-ta\data\NRDD-2024\RDD_Split_Final_china_japan_india_6_classes\RDD_Split_Final_china_japan_india_6_classes\val\images\Japan_006916_jpg.rf.6409c53af3c26b4c760f816734ecafc8.jpg: 1 duplicate labels removed
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 119/119 7.2it/s 16.6s0.1s
                   all       1898       4772       0.52      0.506      0.493      0.225
    Longitudinal_Crack        788       1257      0.463      0.525       0.46      0.189
      Transverse_Crack        532        897      0.475      0.426      0.405      0.149
       Alligator_Crack        960       1245      0.486      0.366      0.403      0.143
               Pothole        354        597      0.558      0.526      0.539       0.24
               manhole        469        644       0.68      0.787      0.769       0.41
           patchy_road        104        132      0.455      0.405      0.383       0.22
Speed: 0.3ms preprocess, 2.6ms inference, 0.0ms loss, 0.5ms postprocess per image
Saving D:\Faaris\Project-TA\road-damage-detection-ta\runs\rdd_yolov8n_local\evaluation\yolo_rd_class_weight_val\predictions.json...
Results saved to D:\Faaris\Project-TA\road-damage-detection-ta\runs\rdd_yolov8n_local\evaluation\yolo_rd_class_weight_val

Evaluasi yolo_rd_class_weight — test
Ultralytics 8.4.108  Python-3.12.3 torch-2.5.1+cu121 CUDA:0 (NVIDIA GeForce RTX 4070 SUPER, 12282MiB)
YOLO-rd summary: 163 layers, 7,086,104 parameters, 0 gradients, 12.8 GFLOPs
val: Fast image access  (ping: 0.00.0 ms, read: 903.2460.3 MB/s, size: 69.6 KB)
val: Scanning D:\Faaris\Project-TA\road-damage-detection-ta\data\NRDD-2024\RDD_Split_Final_china_japan_india_6_classes\RDD_Split_Final_china_japan_india_6_classes\test\labels.cache... 995 images, 0 backgrounds, 0 corrupt: 100% ━━━━━━━━━━━━ 995/995  0.0s
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 63/63 7.0it/s 9.0s0.1s
                   all        995       2425      0.504      0.524        0.5      0.234
    Longitudinal_Crack        395        635      0.498      0.556      0.478      0.205
      Transverse_Crack        266        446       0.45      0.439      0.408      0.148
       Alligator_Crack        480        642      0.509      0.454      0.446      0.171
               Pothole        177        312      0.542      0.497      0.526      0.223
               manhole        234        321      0.693      0.822      0.823      0.461
           patchy_road         52         69      0.329      0.377      0.318      0.197
Speed: 0.3ms preprocess, 2.8ms inference, 0.0ms loss, 0.5ms postprocess per image
Saving D:\Faaris\Project-TA\road-damage-detection-ta\runs\rdd_yolov8n_local\evaluation\yolo_rd_class_weight_test\predictions.json...
Results saved to D:\Faaris\Project-TA\road-damage-detection-ta\runs\rdd_yolov8n_local\evaluation\yolo_rd_class_weight_test
  val  mAP50: 0.4930
  test mAP50: 0.4999

  {
  "model": "yolov8n_class_weight",
  "run_name": "yolov8n_class_weight",
  "weights": "D:\\Faaris\\Project-TA\\road-damage-detection-ta\\runs\\rdd_yolov8n_local\\experiments\\yolov8n_class_weight\\weights\\best.pt",
  "data_yaml": "D:\\Faaris\\Project-TA\\road-damage-detection-ta\\runs\\rdd_yolov8n_local\\rdd6_local.yaml",
  "imgsz": 640,
  "epochs": 300,
  "focal_gamma": 1.5,
  "val_results": {
    "metrics/precision(B)": 0.6841094104523305,
    "metrics/recall(B)": 0.5981101318843972,
    "metrics/mAP50(B)": 0.6571468507947696,
    "metrics/mAP50-95(B)": 0.3645532810463561,
    "fitness": 0.3645532810463561
  },
  "test_results": {
    "metrics/precision(B)": 0.6428699763667756,
    "metrics/recall(B)": 0.5986250136743864,
    "metrics/mAP50(B)": 0.6475620251204575,
    "metrics/mAP50-95(B)": 0.3642077997640151,
    "fitness": 0.3642077997640151
  },
  "f1_summary": {
    "val_macro_f1": 0.6358865740823081,
    "val_weighted_f1": 0.631598791481478,
    "test_macro_f1": 0.6165495872460304,
    "test_weighted_f1": 0.6360303124791741
  },
  "test_speed_ms_per_image": {
    "preprocess": 0.3130863309514957,
    "inference": 3.667143115249636,
    "loss": 0.00029577868967200046,
    "postprocess": 0.571256180658899
  },
  "test_fps_estimate": 219.70848245650242
}

──────────────────────────────────────────────────
Model: yolov12n_class_weight
F1 summary:

{
  "model": "yolov12n_class_weight",
  "run_name": "yolov12n_class_weight",
  "weights": "D:\\Faaris\\Project-TA\\road-damage-detection-ta\\runs\\rdd_yolov8n_local\\experiments\\yolov12n_class_weight\\weights\\best.pt",
  "data_yaml": "D:\\Faaris\\Project-TA\\road-damage-detection-ta\\runs\\rdd_yolov8n_local\\rdd6_local.yaml",
  "imgsz": 640,
  "epochs": 300,
  "focal_gamma": 1.5,
  "val_results": {
    "metrics/precision(B)": 0.6691017582518524,
    "metrics/recall(B)": 0.5999725042614352,
    "metrics/mAP50(B)": 0.6560280313188929,
    "metrics/mAP50-95(B)": 0.3680463344617546,
    "fitness": 0.3680463344617546
  },
  "test_results": {
    "metrics/precision(B)": 0.6383582678664443,
    "metrics/recall(B)": 0.6077484219457616,
    "metrics/mAP50(B)": 0.6542363270786261,
    "metrics/mAP50-95(B)": 0.3713671151218136,
    "fitness": 0.3713671151218136
  },
  "f1_summary": {
    "val_macro_f1": 0.6312007840548098,
    "val_weighted_f1": 0.6313214179520696,
    "test_macro_f1": 0.619161224993913,
    "test_weighted_f1": 0.6366580508259538
  },
  "test_speed_ms_per_image": {
    "preprocess": 0.2885757791037536,
    "inference": 2.383668845327543,
    "loss": 0.00029125615916959004,
    "postprocess": 0.45995366754918243
  },
  "test_fps_estimate": 319.2645888864537
}

{
  "model": "yolov26n_class_weight",
  "run_name": "yolov26n_class_weight",
  "weights": "D:\\Faaris\\Project-TA\\road-damage-detection-ta\\runs\\rdd_yolov8n_local\\experiments\\yolov26n_class_weight\\weights\\best.pt",
  "data_yaml": "D:\\Faaris\\Project-TA\\road-damage-detection-ta\\runs\\rdd_yolov8n_local\\rdd6_local.yaml",
  "imgsz": 640,
  "epochs": 300,
  "focal_gamma": 1.5,
  "val_results": {
    "metrics/precision(B)": 0.680543220927361,
    "metrics/recall(B)": 0.5721474069701576,
    "metrics/mAP50(B)": 0.6331494434901891,
    "metrics/mAP50-95(B)": 0.35982926969846607,
    "fitness": 0.35982926969846607
  },
  "test_results": {
    "metrics/precision(B)": 0.6418234801211165,
    "metrics/recall(B)": 0.5797587293375941,
    "metrics/mAP50(B)": 0.625095592275163,
    "metrics/mAP50-95(B)": 0.3579071940953951,
    "fitness": 0.3579071940953951
  },
  "f1_summary": {
    "val_macro_f1": 0.6204382054164671,
    "val_weighted_f1": 0.6170883375066175,
    "test_macro_f1": 0.6055884922148321,
    "test_weighted_f1": 0.6219189109969571
  },
  "test_speed_ms_per_image": {
    "preprocess": 0.32594009962438336,
    "inference": 2.975039597104617,
    "loss": 0.000256984424426328,
    "postprocess": 0.10814261295126011
  },
  "test_fps_estimate": 293.3306315119534
}

──────────────────────────────────────────────────
Model: yolov8_pd_class_weight
F1 summary:

{
  "model": "yolov8_pd_class_weight",
  "run_name": "yolov8_pd_class_weight",
  "weights": "D:\\Faaris\\Project-TA\\road-damage-detection-ta\\runs\\rdd_yolov8n_local\\experiments\\yolov8_pd_class_weight\\weights\\best.pt",
  "data_yaml": "D:\\Faaris\\Project-TA\\road-damage-detection-ta\\runs\\rdd_yolov8n_local\\rdd6_local.yaml",
  "imgsz": 640,
  "epochs": 300,
  "focal_gamma": 1.5,
  "val_results": {
    "metrics/precision(B)": 0.6768729793597402,
    "metrics/recall(B)": 0.6041252189110474,
    "metrics/mAP50(B)": 0.6510252473494227,
    "metrics/mAP50-95(B)": 0.3658653546271799,
    "fitness": 0.3658653546271799
  },
  "test_results": {
    "metrics/precision(B)": 0.674883188401287,
    "metrics/recall(B)": 0.5910313573508588,
    "metrics/mAP50(B)": 0.6456793813918266,
    "metrics/mAP50-95(B)": 0.36174514846939887,
    "fitness": 0.36174514846939887
  },
  "f1_summary": {
    "val_macro_f1": 0.6376896651827384,
    "val_weighted_f1": 0.6330029246247607,
    "test_macro_f1": 0.6265885179754257,
    "test_weighted_f1": 0.6401510931540665
  },
  "test_speed_ms_per_image": {
    "preprocess": 0.2982926639218127,
    "inference": 1.9269229146890603,
    "loss": 0.0003019088046185335,
    "postprocess": 0.48945547624411595
  },
  "test_fps_estimate": 368.36875621139205
}

──────────────────────────────────────────────────
Model: yolo_rd_class_weight
F1 summary:

{
  "model": "yolo_rd_class_weight",
  "run_name": "yolo_rd_class_weight",
  "weights": "D:\\Faaris\\Project-TA\\road-damage-detection-ta\\runs\\rdd_yolov8n_local\\experiments\\yolo_rd_class_weight\\weights\\best.pt",
  "data_yaml": "D:\\Faaris\\Project-TA\\road-damage-detection-ta\\runs\\rdd_yolov8n_local\\rdd6_local.yaml",
  "imgsz": 640,
  "epochs": 300,
  "focal_gamma": 1.5,
  "val_results": {
    "metrics/precision(B)": 0.5195902634497575,
    "metrics/recall(B)": 0.5059135482219714,
    "metrics/mAP50(B)": 0.4930380542501877,
    "metrics/mAP50-95(B)": 0.2253233813672026,
    "fitness": 0.2253233813672026
  },
  "test_results": {
    "metrics/precision(B)": 0.5035703801298894,
    "metrics/recall(B)": 0.5242824734492835,
    "metrics/mAP50(B)": 0.4999433933271756,
    "metrics/mAP50-95(B)": 0.23402316122437833,
    "fitness": 0.23402316122437833
  },
  "f1_summary": {
    "val_macro_f1": 0.5098194030300544,
    "val_weighted_f1": 0.5011801753903324,
    "test_macro_f1": 0.512039648319056,
    "test_weighted_f1": 0.5227718992698864
  },
  "test_speed_ms_per_image": {
    "preprocess": 0.28377135714806206,
    "inference": 2.792372060331268,
    "loss": 0.0003043225212911865,
    "postprocess": 0.4855316583928301
  },
  "test_fps_estimate": 280.76676807895694
}