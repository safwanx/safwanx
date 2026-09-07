# Hi, I'm Safwan.

ML engineer, computer vision researcher, and occasional ultimate frisbee player.

[Website](https://safwanx.github.io) · [Google Scholar](https://scholar.google.com/citations?user=Bl3jULcAAAAJ&hl=en) · [LinkedIn](https://www.linkedin.com/in/safwan-nabeel-a499581b9/) · [CV](https://safwanx.github.io/assets/Safwan_CV.pdf) · [Email](mailto:safwanxnabeel@outlook.com)

<img src="banner.svg" width="100%" alt="A frisbee glides along a curved flight path.">

I got into computer vision through crowd counting. Our models struggled with people wearing shemaghs and hijabs, which made me think more about who was missing from the training data. Since then, I've been interested in understanding when models fail and whether we can spot unreliable predictions.

Alongside my engineering work, I mentor student research at KAUST Academy. Away from the screen, I play ultimate with Kingdom Ultimate when I'm at KAUST, take photos, hike, and play board games.

## Research

**TWASEL at SignEval 2026: Adaptive Multi-Stream Pose Fusion for Continuous Sign Language Recognition**<br>
Sadam Al-Azani, **Safwan Nabeel**, Qasim Al Mahfood, Mohanad Mohamed<br>
*CVPR Workshops 2026*

Recognizing sign language from body, hand, and facial movement. The model learns which signals to use over time and reached 16.62% word error rate on the SignEval test set.

[Paper](https://openaccess.thecvf.com/content/CVPR2026W/MSLR/papers/Al-Azani_TWASEL_at_SignEval_2026_Adaptive_Multi-Stream_Pose_Fusion_for_Continuous_CVPRW_2026_paper.pdf) · [Code](https://github.com/sazani/TWASEL-SignLang)

**Are Crowd Counts Reliable? Post-Hoc Reliability Assessment for Crowd Counting Under Dataset Shift**<br>
**Safwan Nabeel**, Sadam Al-Azani, Muhammad Shahid Jabbar<br>
*Under review at IJCV*

Can a crowd-counting model tell which predictions are likely to be wrong? We estimate error risk without retraining the model, then test how well those estimates hold up on a different dataset.

<!-- Hidden until the ACCV decision. Restore by removing the comment markers.
**Privacy and identity leakage in anonymized video**<br>
*Under review, ACCV 2026*<br>
A benchmark for residual identity leakage in privacy-preserving action recognition, attacked through face, body appearance, pose, gait, and learned features. Blurring a face is not the same as hiding a person.
-->

## Projects

- **[CrowdSense](https://github.com/safwanx/CrowdSense)**: upload an image to get a crowd count and density heatmap, served through FastAPI.
- **Video-to-text summarization**: YOLO selects frames, Florence-2 describes them, and Command R+ turns them into rolling one-minute summaries. Supports live and recorded video.

I mainly work with Python, PyTorch, OpenCV, and FastAPI.
