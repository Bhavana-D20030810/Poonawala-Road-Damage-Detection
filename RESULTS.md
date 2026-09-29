# Small-subset held-out test results

These numbers are from this subset run, not the earlier full-data experiment.

| Class | Precision | Recall | mAP50 | mAP50–95 |
|---|---:|---:|---:|---:|
| All | 0.313 | 0.251 | 0.180 | 0.050 |
| Longitudinal crack | 0.169 | 0.114 | 0.066 | 0.018 |
| Transverse crack | 0.454 | 0.181 | 0.185 | 0.023 |
| Alligator crack | 0.299 | 0.479 | 0.304 | 0.106 |
| Pothole | 0.331 | 0.228 | 0.166 | 0.052 |

Training: YOLOv8n, 8 epochs, 512 pixels, batch 16, seed 42, device 0.
Severity uses an unvalidated image-area proxy; no severity accuracy is claimed.
