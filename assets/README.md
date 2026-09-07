# Profile visuals

- `twasel-streams.svg`: an original explanatory sketch of the four-region architecture described in the [TWASEL paper](https://openaccess.thecvf.com/content/CVPR2026W/MSLR/papers/Al-Azani_TWASEL_at_SignEval_2026_Adaptive_Multi-Stream_Pose_Fusion_for_Continuous_CVPRW_2026_paper.pdf). The moving connectors illustrate information flow; the pose is schematic, not a recorded sign or model inference. The decoder is summarized as gloss output.
- `crowd-reliability.svg`: an original conceptual illustration of error-risk ranking and calibration after dataset shift. The bars and curve are illustrative, not experimental measurements.
- `crowdsense-demo.gif` and `crowdsense-demo.png`: synchronized excerpts from existing [CrowdSense demo files](https://github.com/safwanx/CrowdSense/tree/main/media): `crowd_vid1.mp4`, `density.mp4`, and `overlay.mp4`. All three files contain 341 frames at 25 fps. The animation samples identical frame indices from each, beginning at frame 25, at 8 fps for six seconds. No density values were synthesized and no new model inference was run. The original videos are retained in the source project.

The SVG animations stop when reduced motion is requested. The profile uses the PNG instead of the GIF for that preference and provides a still-image link.

Rebuild with Python, Pillow, numpy, and opencv-python:

```sh
python scripts/build_research_visuals.py /path/to/CrowdSense
```

The generator uses Segoe UI from the Windows fonts directory for the video captions. To run on another OS, change its font path to a locally installed sans-serif font.
