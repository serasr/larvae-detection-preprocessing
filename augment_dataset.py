import cv2
import os
import random
import json

# Adjust bounding boxes for flip augmentations
def adjust_bbox_flip(shape, w, h, flip_type):  
    (x1, y1), (x2, y2) = shape["points"]

    if flip_type == 1:  # Horizontal flip
        new_x1 = w - x2
        new_x2 = w - x1
        shape["points"] = [[new_x1, y1], [new_x2, y2]]

    elif flip_type == 0:  # Vertical flip
        new_y1 = h - y2
        new_y2 = h - y1
        shape["points"] = [[x1, new_y1], [x2, new_y2]]

    elif flip_type == -1:  # Both flips
        new_x1 = w - x2
        new_x2 = w - x1
        new_y1 = h - y2
        new_y2 = h - y1
        shape["points"] = [[new_x1, new_y1], [new_x2, new_y2]]

# Adjust bounding boxes for rotation using affine matrix
def adjust_bbox_rotation(shape, M):
    (x1, y1), (x2, y2) = shape["points"]
    pts = [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]
    rotated_pts = []
    for x, y in pts:
        new_x = int(M[0,0]*x + M[0,1]*y + M[0,2])
        new_y = int(M[1,0]*x + M[1,1]*y + M[1,2])
        rotated_pts.append([new_x, new_y])
    xs, ys = zip(*rotated_pts)
    shape["points"] = [[min(xs), min(ys)], [max(xs), max(ys)]]

# Save augmented image and JSON
def save_augmented(img, data, base_name, suffix, output_folder):
    img_name = base_name + suffix + ".jpg"
    json_name = base_name + suffix + ".json"

    data["imagePath"] = img_name
    cv2.imwrite(os.path.join(output_folder, img_name), img)

    with open(os.path.join(output_folder, json_name), "w") as f:
        json.dump(data, f, indent=2)

def image_augment(image_path, json_path, output_folder):
    img = cv2.imread(image_path)
    h, w = img.shape[:2]

    with open(json_path, 'r') as j:
        data = json.load(j)
    
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Save original image first
    save_augmented(img, json.loads(json.dumps(data)), base_name, "_orig", output_folder)

    # Random flip the image
    flip_type = random.choice([1, 0, -1])
    flipped = cv2.flip(img, flip_type)
    flip_data = json.loads(json.dumps(data)) 
    for shape in flip_data["shapes"]:
        adjust_bbox_flip(shape, w, h, flip_type)
    save_augmented(flipped, flip_data, base_name, f"_flip{flip_type}", output_folder)

    # Modify Brightness and Contrast of the image
    bright = cv2.convertScaleAbs(img, alpha=1.2, beta=30)
    bc_data = json.loads(json.dumps(data)) 
    save_augmented(bright, bc_data, base_name, "_bright", output_folder)

    # Apply Gaussian Blur to the image
    blur = cv2.GaussianBlur(img, (5, 5), 0)
    blur_data = json.loads(json.dumps(data))  
    save_augmented(blur, blur_data, base_name, "_blur", output_folder)

    # Random rotate the image
    angle = random.choice([-15, -10, 10, 15])
    M = cv2.getRotationMatrix2D((w/2, h/2), angle, 1.0)
    rotated = cv2.warpAffine(img, M, (w, h))
    rot_data = json.loads(json.dumps(data)) 
    for shape in rot_data["shapes"]:
        adjust_bbox_rotation(shape, M)
    save_augmented(rotated, rot_data, base_name, f"_rot{angle}", output_folder)

def batch_augment(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file in os.listdir(input_folder):
        if file.endswith(".json"):
            json_path = os.path.join(input_folder, file)
            image_path = json_path.replace(".json", ".jpg")
            if not os.path.exists(image_path):
                print(f"Skipping {json_path}, no matching image")
                continue
            image_augment(image_path, json_path, output_folder)

# --- Run for your folders ---
batch_augment("output_frames/video_00", "augmented_frames/video_00")
batch_augment("output_frames/video_01", "augmented_frames/video_01")