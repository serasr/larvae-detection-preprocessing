# Mosquito Larvae Frame Extraction, Annotation, and Augmentation

## Overview
This project prepares a dataset of mosquito larvae images for deep neural network (DNN) training.  
It includes **frame extraction**, **annotation**, and **data augmentation** to create a larger, more diverse dataset.  

---

## Project Structure
```
Mosquito_Larvae_Project/
├── extract_frames.py         # Script to extract random frames from videos
├── augment_dataset.py        # Script to apply augmentations + update JSONs
├── output_frames/            # Extracted frames from videos
│   ├── video_00/
│   └── video_01/
├── augmented_frames/         # Augmented outputs (images + JSONs)
├── annotations/              # Original annotation JSONs from LabelMe
├── samples/                  # Few sample augmented results
│   ├── annotated_frames/
│   └── augmented_images/
├── report.pdf                # One-page project report
└── README.md                 # Replication instructions (this file)
```

---

## Requirements
- Python 3.x  
- OpenCV  
- LabelMe v5.2.1  

Install dependencies:
```bash
pip install opencv-python
pip install labelme==5.2.1
```

---

## How to Run

### 1. Frame Extraction
Extract **5 random frames** per video:
```bash
python extract_frames.py
```
Frames will be saved under `output_frames/video_00` and `output_frames/video_01`.

---

### 2. Annotation
Annotate the extracted frames using **LabelMe**:
```bash
labelme 
```
- Draw bounding boxes around mosquito larvae.  
- Save annotations → `.json` files will be created next to each image.  
- Repeat for both videos.  

---

### 3. Data Augmentation
Apply augmentations and save new images + updated JSONs:
```bash
python augment_dataset.py
```

This will generate augmented images in `augmented_frames/`.  
Augmentations include:
- Random flips (horizontal, vertical, both)  
- Brightness/contrast adjustment  
- Gaussian blur  
- Small-angle rotations (±10–15°)  

---

### 4. Sample Outputs
The `samples/` folder contains example augmented images and JSONs.  
Example:
- `frame_0000_orig.jpg` (original)  
- `frame_0000_flip.jpg` (flipped)  
- `frame_0000_bright.jpg` (brightened)  

---

## Notes on Annotations
- Format: **LabelMe JSON**.  
- Each bounding box is defined by two corner points:  
  ```json
  "points": [[x1, y1], [x2, y2]]
  ```
- For **geometric augmentations**, bounding boxes are recalculated.  
- For **photometric augmentations**, bounding boxes remain the same, but `"imagePath"` is updated.  

---

## References
- [OpenCV Documentation](https://docs.opencv.org)  
- [LabelMe Annotation Tool](https://github.com/wkentaro/labelme)  

