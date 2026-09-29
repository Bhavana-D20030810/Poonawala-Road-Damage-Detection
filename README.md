# Road damage detection and severity assessment

Poonawalla Fincorp SIP case: bounding-box detection for D00 longitudinal cracks, D10 transverse cracks, D20 alligator cracks, and D40 potholes on Indian roads. The demo adds an illustrative Low/Medium/High severity estimate.

## Quick reproduction

Open `Run_Roboflow_Quick.ipynb` in Google Colab with a T4 GPU and run cells in order. It downloads [Prakhar's RDD2022-India v5](https://universe.roboflow.com/prakhar-kpb1v/rdd2022-india-il8ju/dataset/5) directly in YOLOv8 format, then selects up to 600 training, 100 validation and 100 test images with four remapped classes. The published dataset has 7,706 images and ten classes; the small sample is a time-limited proof of concept. Original split partitions are retained.

Training starts with pretrained YOLOv8n weights at 512 pixels, batch 16, 8 epochs, seed 42. `src/train.py` saves periodic checkpoints to Drive and computes held-out precision, recall, mAP50 and mAP50–95 in `RESULTS.md`. After training, `models/best.pt` contains the weights. Run `pip install -r requirements.txt` and `python app.py` for the demo.

## Limitations

The source annotations do not label severity. The demo uses an **unvalidated image-area proxy**: box area under 1% Low, 1–4% Medium, and above 4% High. Camera viewpoint and distance can change it. Do not claim severity accuracy or full-data benchmark performance.

## Files

- `src/prepare_roboflow.py`: subset and four-class remapping
- `src/train.py`: checkpointing, held-out evaluation and real prediction
- `app.py`: upload and annotated inference
- `Run_Roboflow_Quick.ipynb`: full Colab workflow
- `RESULTS.md`: measured metrics only after training
- `models/best.pt`: add only after a successful run

Dataset: Prakhar, RDD2022-India v5, Roboflow Universe, CC BY 4.0. Original RDD2022 source: https://github.com/sekilab/RoadDamageDetector.
