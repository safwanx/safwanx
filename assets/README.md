# Profile visuals

- `twasel-results.png`: static chart of the final-model results reported in the [TWASEL paper](https://openaccess.thecvf.com/content/CVPR2026W/MSLR/papers/Al-Azani_TWASEL_at_SignEval_2026_Adaptive_Multi-Stream_Pose_Fusion_for_Continuous_CVPRW_2026_paper.pdf). Both bars are development-set WER: CTC greedy 20.42%, AR beam search 11.85%. The separate test-set result is 16.62%. No synthetic pose sequence or inferred training curve is used.
- `crowd-snow-case.png`: image 0814 from the JHU-CROWD++ test set and the two matching rows from the crowd-reliability project's `findings/tables/visual_failure_cases.csv`. Exact source values used for the labels are retained in `crowd-case-values.csv`. Counts, absolute errors, and within-setting risk percentiles are rounded for display. A risk percentile is a relative rank, not a confidence probability. The source manuscript discusses these two cases in its representative-failures figure. The image is fitted without cropping or altering the scene.
- `crowdsense-demo.gif` and `crowdsense-demo.png`: synchronized excerpts from existing [CrowdSense demo files](https://github.com/safwanx/CrowdSense/tree/main/media): `crowd_vid1.mp4`, `density.mp4`, and `overlay.mp4`. All three files contain 341 frames at 25 fps. The animation samples identical frame indices from each, beginning at frame 25, at 8 fps for six seconds. No density values were synthesized and no new model inference was run. The original videos are retained in the source project.

Both research figures are static. The profile uses the PNG instead of the CrowdSense GIF when reduced motion is requested and provides a still-image link.

Rebuild with Python, Pillow, numpy, and opencv-python:

```sh
python scripts/build_research_visuals.py /path/to/CrowdSense
python scripts/build_static_research.py /path/to/Crowd
```

The video generator uses Segoe UI from the Windows fonts directory for the captions. To run on another OS, change its font path to a locally installed sans-serif font. The static-figure generator also requires matplotlib and reads the original research project's case table and image.
