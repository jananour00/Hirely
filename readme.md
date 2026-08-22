# ORCA Robotics — Computer Vision / Deep Learning Intern
## Interview Question Bank (100 Questions)

Role focus: dataset labeling & curation, model training/evaluation (detection & segmentation), integration into a perception pipeline, and performance analysis — on real robotic platforms in a startup setting.

Suggested use: pick ~12–15 questions per candidate spanning multiple sections, plus 1 live problem-solving exercise. Sections are ordered roughly from foundational → applied → systems → behavioral, so you can escalate depth based on how the candidate is performing.

---

## 1. Computer Vision & Image Processing Fundamentals (10)

1. Walk me through the difference between image classification, object detection, and semantic/instance segmentation. When would you choose each?
2. What is IoU (Intersection over Union), and how is it used during both training and evaluation?
3. Explain the difference between semantic segmentation and instance segmentation with a concrete example.
4. What is non-maximum suppression (NMS), and why do detectors need it?
5. How does anchor-based detection differ from anchor-free detection? Name an example architecture of each.
6. What's the difference between a convolution and a transposed convolution (deconvolution)? Where would you use each?
7. Explain what a feature pyramid network (FPN) does and why it helps with detecting objects at multiple scales.
8. What is the purpose of data augmentation in computer vision, and can you name augmentations that would help vs. hurt on a robotics camera feed specifically (e.g., motion blur, lighting)?
9. How would you handle images captured in poor lighting, glare, or motion blur from a moving robot?
10. What's the difference between stereo vision and monocular depth estimation? What are the tradeoffs for a robotics application?

## 2. Deep Learning Fundamentals (10)

11. Explain backpropagation in your own words — no need for exact math, just the intuition.
12. What is the vanishing gradient problem, and how do modern architectures mitigate it?
13. Compare batch normalization and layer normalization — when is each typically used?
14. What's the difference between overfitting and underfitting, and how do you diagnose each from training curves?
15. Explain dropout and why it helps generalization.
16. What is transfer learning, and when would you fine-tune a full network vs. freeze most layers?
17. Walk me through how you'd choose a learning rate and scheduler for a new training run.
18. What's the difference between L1 and L2 regularization, and how do they affect learned weights differently?
19. Explain the difference between a CNN and a Vision Transformer (ViT) at a high level. What are the practical tradeoffs (data needs, compute, inductive bias)?
20. What is Focal Loss, and what specific problem was it designed to solve?

## 3. Object Detection — Architectures & Tradeoffs (10)

21. Compare one-stage detectors (e.g., YOLO, RetinaNet) with two-stage detectors (e.g., Faster R-CNN). What are the speed/accuracy tradeoffs?
22. Walk me through the YOLO architecture at a high level — how does it predict bounding boxes and class scores in a single pass?
23. What is anchor box design, and how would you choose anchor sizes/ratios for a new dataset (e.g., small obstacles vs. large ones)?
24. How would you handle detecting very small objects in an image (e.g., a small obstacle far from the robot)?
25. What's the role of the Region Proposal Network (RPN) in Faster R-CNN?
26. If a detector shows high precision but low recall, what could be causing that, and how would you address it?
27. Conversely, if you have high recall but low precision, what's your diagnosis and fix?
28. How would you decide between YOLOv5/YOLOv8 vs. RetinaNet vs. a transformer-based detector (e.g., DETR) for a real-time robotics application?
29. What is mAP (mean Average Precision), and how is it computed? What does mAP@0.5 vs mAP@0.5:0.95 tell you differently?
30. How would you approach multi-class detection where some classes have very few labeled examples?

## 4. Segmentation (8)

31. Walk me through the U-Net architecture — what problem do the skip connections solve?
32. What's the difference between using a segmentation mask vs. a bounding box for downstream robot navigation or manipulation?
33. How would you evaluate a segmentation model — what metrics beyond pixel accuracy matter, and why?
34. What is Dice loss, and why is it often preferred over plain cross-entropy for segmentation, especially with class imbalance?
35. How would you handle segmenting an object that's partially occluded in the camera frame?
36. What's the difference between panoptic segmentation and instance segmentation?
37. If your segmentation model performs well on validation but poorly on real robot camera footage, what would you investigate first?
38. How does image resolution affect segmentation accuracy vs. inference speed, and how would you balance that for a real-time system?

## 5. Dataset Curation, Labeling & Annotation (10)

39. Walk me through your process for setting up a labeling pipeline from scratch for a new object category.
40. What annotation tools have you used (e.g., CVAT, LabelImg, Roboflow, Label Studio)? What did you like/dislike about them?
41. How would you write clear labeling guidelines so multiple annotators label consistently?
42. How do you handle disagreement between annotators (inter-annotator disagreement) on ambiguous cases?
43. What's your strategy for catching and fixing mislabeled data before it goes into training?
44. How would you decide what to prioritize labeling first with a limited annotation budget?
45. How would you approach active learning — using a partially trained model to help prioritize which new images to label?
46. What's the difference between labeling for detection (bounding boxes) vs. labeling for segmentation (polygons/masks) in terms of time cost and precision needed?
47. How would you structure a dataset split (train/val/test) to avoid data leakage, especially with video frames from a robot's camera?
48. If you inherited a dataset with inconsistent or noisy labels, how would you audit and clean it?

## 6. Class Imbalance & Domain Shift (7)

49. What is class imbalance, and how did you handle it in past projects (e.g., Focal Loss, resampling, weighted loss)?
50. What is domain shift, and how might it show up when a model trained on one dataset is deployed on a robot in a different environment?
51. How would you detect that your model is suffering from domain shift in production (e.g., outdoor lighting vs. training data)?
52. What techniques would you use to make a model more robust to domain shift (e.g., domain adaptation, augmentation, synthetic data)?
53. How would synthetic data or simulation help in a robotics CV pipeline, and what are its limitations?
54. If a rare-but-critical object (e.g., a specific obstacle type) is underrepresented in your dataset, what's your plan?
55. How would you approach oversampling vs. undersampling vs. loss reweighting — what are the tradeoffs?

## 7. Model Training, Evaluation & Iteration (10)

56. Walk me through your typical experiment workflow — how do you track experiments and compare model versions?
57. What metrics would you report to a non-technical stakeholder vs. a technical teammate, and why the difference?
58. How do you decide a model is "good enough" to move from experimentation to integration?
59. What's your process when a model's validation metrics look great but real-world performance disappoints?
60. How would you use a confusion matrix to diagnose which classes need more work?
61. What's the role of a held-out test set that's never touched during development, and why does it matter?
62. How would you set up a baseline before jumping into a complex architecture?
63. What's your approach to hyperparameter tuning — grid search, random search, Bayesian optimization (e.g., Optuna)? When is each worth the cost?
64. How do you decide when to stop training (early stopping) and what do you monitor?
65. Describe a time a model you built underperformed. What did you do to diagnose and fix it?

## 8. Deployment & Perception Pipeline Integration (10)

66. What does "real-time inference" mean in a robotics context, and what latency/FPS would you consider acceptable for obstacle detection?
67. How would you optimize a trained model for faster inference on limited hardware (e.g., quantization, pruning, TensorRT, ONNX)?
68. Walk me through how you'd integrate a trained detection model into a ROS-based perception pipeline.
69. What's the difference between running inference on CPU vs. GPU vs. an edge device (e.g., Jetson), and how does that affect your model choice?
70. How would you handle a case where your model's inference time is too slow for the robot's control loop?
71. What would you do if the camera feed frame rate and the model's inference rate don't match?
72. How would you design a fallback behavior if the perception model fails to detect anything for several frames (e.g., sensor occlusion)?
73. How would you combine detection/segmentation output with other sensors (e.g., LiDAR, ultrasonic) for more robust perception?
74. What's your experience with model serving frameworks (FastAPI, Streamlit, TorchServe, Triton)? How would that differ for a robot vs. a web app?
75. How would you version and roll back a deployed perception model if a new version performs worse in the field?

## 9. Debugging, Failure Modes & Practical Judgment (8)

76. If your detector consistently misses objects at the edges of the frame, what would you suspect and how would you test your hypothesis?
77. If your model performs well in the lab but fails outdoors, what variables would you investigate first?
78. How would you distinguish between a data problem and a model architecture problem when performance is poor?
79. What would you check if training loss is decreasing but validation loss is increasing?
80. If two team members get very different results training "the same" model, how would you debug reproducibility?
81. How would you approach explaining a wrong model prediction to a teammate — what tools (e.g., Grad-CAM) would you reach for?
82. If a stakeholder asks "why did the robot not see that obstacle," how would you investigate end-to-end (data → model → deployment)?
83. What's your process for regression testing — making sure a new model version doesn't break performance on cases the old one handled well?

## 10. Collaboration, Communication & Startup Fit (9)

84. Tell me about a time you had to explain a technical CV/ML concept to a non-technical teammate or stakeholder.
85. Describe a brainstorming session where you helped shape a labeling or classification approach from scratch. What was your contribution?
86. How do you prioritize when you have multiple competing tasks (e.g., labeling, training, debugging) with a tight deadline?
87. Tell me about a time you disagreed with a teammate's technical approach. How did you handle it?
88. What excites you specifically about working on a physical robotic platform rather than a purely software/dataset project?
89. Startups often mean ambiguous scope and changing priorities. Describe a time you had to adapt quickly to a change in project direction.
90. How comfortable are you working with incomplete or messy real-world data versus clean benchmark datasets (e.g., COCO, ImageNet)?
91. What's a computer vision project you're most proud of, and what would you do differently if you rebuilt it today?
92. Why ORCA Robotics specifically — what about autonomous robots interests you over other CV application areas (e.g., medical imaging, retail)?

## 11. Live Problem-Solving Prompts (8 — pick 1–2 for a whiteboard/live-coding segment)

93. Given a dataset of 5,000 images with a 1:20 class imbalance between "obstacle" and "background," walk me through how you'd approach training a detector, step by step.
94. You have a YOLO model that runs at 8 FPS on the robot's onboard computer, but you need 20 FPS. Walk me through your optimization plan.
95. Sketch out (verbally or on a whiteboard) how you'd design a labeling schema for a new object category the robot needs to detect and avoid.
96. Given a confusion matrix showing your model frequently confuses "pedestrian" and "pole" at a distance, propose two hypotheses and how you'd test each.
97. Write pseudocode (or real code, your language of choice) for computing IoU between two bounding boxes.
98. You're given raw, unlabeled video from a robot's onboard camera. Describe your end-to-end pipeline from raw footage to a trained, deployed detection model.
99. A teammate says "let's just use the biggest model available for best accuracy." How do you respond, considering the robotics deployment constraints?
100. Design a simple evaluation dashboard (metrics + visuals) you'd want to see after every training run to quickly judge whether a new model is better than the last.

---

### Notes for interviewers
- For junior/intern candidates, weight Sections 1–2, 5, and 10 more heavily; use Sections 7–9 to gauge growth potential rather than expecting mastery.
- Section 11 prompts are best for a 15–20 minute live segment — look for structured thinking and the right clarifying questions, not a "perfect" answer.
- Cross-reference answers against the candidate's CV/portfolio projects where possible (e.g., ask them to defend a specific design choice they made in a past detection or segmentation project).
