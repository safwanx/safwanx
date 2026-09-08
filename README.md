<picture>
  <source media="(max-width: 640px)" srcset="profile-coast-narrow.svg">
  <img src="profile-coast.svg" width="100%" alt="Safwan Nabeel. Machine learning and computer vision. A frisbee floats over a moonlit coast.">
</picture>

<p align="center">
  <a href="https://safwanx.github.io"><img src="https://img.shields.io/badge/Website-244D60?style=for-the-badge&amp;logo=githubpages&amp;logoColor=white" alt="Website"></a>
  <a href="https://scholar.google.com/citations?user=Bl3jULcAAAAJ&amp;hl=en"><img src="https://img.shields.io/badge/Google_Scholar-386E83?style=for-the-badge&amp;logo=googlescholar&amp;logoColor=white" alt="Google Scholar"></a>
  <a href="https://www.linkedin.com/in/safwan-nabeel-a499581b9/"><img src="https://img.shields.io/badge/LinkedIn-365D79?style=for-the-badge&amp;logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTMgOWgzLjZ2MTJIM3pNNC44IDMuMmEyLjEgMi4xIDAgMSAxIDAgNC4yIDIuMSAyLjEgMCAwIDEgMC00LjJ6TTkuNCA5aDMuNHYxLjdjLjUtLjkgMS43LTIgMy42LTIgMy44IDAgNC41IDIuNSA0LjUgNS43VjIxaC0zLjZ2LTUuOGMwLTEuNCAwLTMuMi0yLTMuMnMtMi4zIDEuNS0yLjMgMy4xVjIxSDkuNHoiLz48L3N2Zz4=" alt="LinkedIn"></a>
  <a href="mailto:safwanxnabeel@outlook.com"><img src="https://img.shields.io/badge/Email-387E73?style=for-the-badge&amp;logo=maildotru&amp;logoColor=white" alt="Email"></a>
  <a href="https://safwanx.github.io/assets/Safwan_CV.pdf"><img src="https://img.shields.io/badge/CV-PDF-526F73?style=for-the-badge&amp;logo=readdotcv&amp;logoColor=white" alt="CV PDF"></a>
</p>

## 👋 A little about me

I work on trustworthy multimodal AI: models that combine images, video, and other signals, and what happens to them once they leave the benchmark. I came to this through computer vision, after watching a model I had trained fail on people who were missing from its training data. The questions I keep returning to are when a prediction stops being reliable under distribution shift, what private information survives anonymization, and how far vision-language models can be trusted in healthcare and industrial settings.

🔍 **Research interests:** trustworthy and privacy-preserving ML, multimodal and vision-language models, reliability under distribution shift, and reliable AI for healthcare and industry.<br>
💻 I work as an **ML engineer** and mentor student research at **KAUST Academy**.<br>
🏎️ Outside work: a huge F1 fan. Also into frisbee, photography, hiking, and board games.

## 🔬 Research

**TWASEL at SignEval 2026: Adaptive Multi-Stream Pose Fusion for Continuous Sign Language Recognition**<br>
Sadam Al-Azani, **Safwan Nabeel**, Qasim Al Mahfood, Mohanad Mohamed<br>
*CVPR Workshops 2026*

<a href="https://github.com/sazani/TWASEL-SignLang"><img src="assets/twasel-streams.svg" width="100%" alt="TWASEL architecture: separate body, left-hand, right-hand, and face streams feed learned fusion, a Conformer, and gloss decoding. Conceptual illustration."></a>

Recognizing sign language from body, hand, and facial movement. The model learns which signals to use over time and reached 16.62% word error rate on the SignEval test set.

[![Paper](https://img.shields.io/badge/Paper-PDF-387E73?style=flat-square)](https://openaccess.thecvf.com/content/CVPR2026W/MSLR/papers/Al-Azani_TWASEL_at_SignEval_2026_Adaptive_Multi-Stream_Pose_Fusion_for_Continuous_CVPRW_2026_paper.pdf) [![Code](https://img.shields.io/badge/Code-GitHub-244D60?style=flat-square&logo=github)](https://github.com/sazani/TWASEL-SignLang)

**Are Crowd Counts Reliable? Post-Hoc Reliability Assessment for Crowd Counting Under Dataset Shift**<br>
**Safwan Nabeel**, Sadam Al-Azani, Muhammad Shahid Jabbar<br>
*Under review at IJCV*

<picture>
  <source media="(max-width: 640px)" srcset="assets/crowd-snow-case-narrow.png">
  <img src="assets/crowd-snow-case.png" width="100%" alt="Real JHU-CROWD++ snowy stadium example with 8,994 annotated people. STEERER predicted 1,375.1, at the 96.9th risk percentile. MPCount transferred from QNRF predicted 134.1, at the 4.4th risk percentile within its evaluation setting. Both undercounted severely, but the transferred model's risk estimate did not flag the failure.">
</picture>

In this snowy stadium, both counters missed most of the crowd, but the risk estimate for the transferred MPCount model ranked its prediction as low risk. A low risk score did not mean a small error.

We estimate error risk without retraining the crowd counter, then test how well those estimates hold up on a different dataset.

Keeping the 80% of images ranked most reliable reduced mean absolute error by **19–68%** across seven settings, though calibration did not hold up reliably after dataset shift.

<!-- Hidden until the ACCV decision. Restore by removing the comment markers.
**Privacy and identity leakage in anonymized video**<br>
*Under review, ACCV 2026*<br>
A benchmark for residual identity leakage in privacy-preserving action recognition, attacked through face, body appearance, pose, gait, and learned features. Blurring a face is not the same as hiding a person.
-->

## 🧰 Projects

### CrowdSense

One scene, three views: the crowd, the predicted density, and the two together.

<a href="https://github.com/safwanx/CrowdSense">
  <picture>
    <source media="(prefers-reduced-motion: reduce)" srcset="assets/crowdsense-demo.png">
    <img src="assets/crowdsense-demo.gif" width="100%" alt="Synchronized CrowdSense demo: overhead crowd footage beside its predicted density map and heatmap overlay.">
  </picture>
</a>

An excerpt from my existing demo outputs. The FastAPI app accepts an image and returns an estimated count and density overlay.

[![Code](https://img.shields.io/badge/Code-GitHub-244D60?style=flat-square&logo=github)](https://github.com/safwanx/CrowdSense) · [Still frame](assets/crowdsense-demo.png)

**Video-to-text summarization**: YOLO selects frames, Florence-2 describes them, and Command R+ turns them into rolling one-minute summaries. Supports live and recorded video.

## 🛠️ Tools I use

<img src="https://skillicons.dev/icons?i=python,pytorch,opencv,sklearn,fastapi,git,linux,latex&amp;perline=8" alt="Python, PyTorch, OpenCV, scikit-learn, FastAPI, Git, Linux, and LaTeX">

## 🏅 A few highlights

- **2nd of 65** in Computer Information Systems at IAU, graduating with Second Honors.
- **2nd place**, GSR Hackathon at KFUPM, 2025.
- **Best Poster**, Undergraduate AI Projects Showcase at KFUPM, 2024.
- **1st place**, Cybersecurity category, Future Technologies, MCIT, 2024.
- **Global Top 10 &amp; People's Choice**, Kaspersky Secure IT Cup, 2023.

📬 If our research interests overlap, [say hello](mailto:safwanxnabeel@outlook.com).
