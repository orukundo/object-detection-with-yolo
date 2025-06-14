# 1. Install YOLOv8
!pip install -q ultralytics

import os
import random
import torch
import shutil
from google.colab import drive
from tqdm import tqdm
from ultralytics import YOLO


# Set random seed for reproducibility
random.seed(42)

# Device CPU or GPU
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# 3. Mount Google Drive
drive.mount('/content/drive')

# Check if image and label folder exist
dataset_path = '/content/drive/MyDrive/'

# Check for images and labels folders
images_path = os.path.join(dataset_path, 'images')
labels_path = os.path.join(dataset_path, 'labels')

print("Checking if folders exist...")

if os.path.exists(images_path) and os.path.exists(labels_path):
    print("Found both 'images' and 'labels' folders.")
else:
    if not os.path.exists(images_path):
        print(" 'images' folder is missing!")
    if not os.path.exists(labels_path):
        print(" 'labels' folder is missing!")

# Define original and new paths
original_images_path = '/content/drive/MyDrive/.../images'
original_labels_path = '/content/drive/MyDrive/.../labels'
new_base_path = '/content/drive/MyDrive/..._split'

# Image and label destination folders
train_img_dir = os.path.join(new_base_path, 'images/train')
val_img_dir = os.path.join(new_base_path, 'images/val')
test_img_dir = os.path.join(new_base_path, 'images/test')

train_lbl_dir = os.path.join(new_base_path, 'labels/train')
val_lbl_dir = os.path.join(new_base_path, 'labels/val')
test_lbl_dir = os.path.join(new_base_path, 'labels/test')

# Create directories
for path in [train_img_dir, val_img_dir, test_img_dir, train_lbl_dir, val_lbl_dir, test_lbl_dir]:
    os.makedirs(path, exist_ok=True)

# List all images
all_images = [f for f in os.listdir(original_images_path) if f.lower().endswith(('.png'))]
print(f"Found {len(all_images)} images.")

# Shuffle and split
random.shuffle(all_images)

n_total = len(all_images)
n_train = int(0.7 * n_total)
n_val = int(0.15 * n_total)
n_test = n_total - n_train - n_val

train_images = all_images[:n_train]
val_images = all_images[n_train:n_train + n_val]
test_images = all_images[n_train + n_val:]

print(f"Train: {len(train_images)}, Val: {len(val_images)}, Test: {len(test_images)}")

# Move images and corresponding labels
def move_files(file_list, img_dest_dir, lbl_dest_dir):
    for file_name in tqdm(file_list, desc=f"Moving to {img_dest_dir.split('/')[-1]}"):
        src_img_path = os.path.join(original_images_path, file_name)
        dst_img_path = os.path.join(img_dest_dir, file_name)
        shutil.copy2(src_img_path, dst_img_path)

        # Move label
        label_name = os.path.splitext(file_name)[0] + '.txt'
        src_lbl_path = os.path.join(original_labels_path, label_name)
        dst_lbl_path = os.path.join(lbl_dest_dir, label_name)

        if os.path.exists(src_lbl_path):
            shutil.copy2(src_lbl_path, dst_lbl_path)
        else:
            print(f"Label file not found for {file_name}")

# Move all splits
move_files(train_images, train_img_dir, train_lbl_dir)
move_files(val_images, val_img_dir, val_lbl_dir)
move_files(test_images, test_img_dir, test_lbl_dir)

print("Dataset split with images and labels completed!")

# Create dataset.yaml
dataset_yaml_path = os.path.join(new_base_path, 'dataset.yaml')
dataset_yaml = f"""
path: {new_base_path}
train: images/train
val: images/val
test: images/test
names:
  0: adenovirus
"""

with open(dataset_yaml_path, 'w') as f:
    f.write(dataset_yaml)

print("dataset.yaml file created!")

# Load a new YOLO model
print("Loading YOLOv8 model for training...")
model = YOLO('yolov8n.pt')  # Nano model

# Train the model with hyperparameters
print("Starting training...")
model.train(
    data=dataset_yaml_path,
    epochs=1000,
    imgsz=640,
    batch=16,
    patience=0,
    name='adenovirus_detection',
    device=device,
    seed=42,
    lr0=0.01,
    optimizer='SGD',
    momentum=0.937,
    weight_decay=0.0005
)

# Save the best model to Drive
best_model_path = '/content/drive/MyDrive/best_adenovirus_model.pt'
print(f"Saving best model to {best_model_path}...")
!cp /content/runs/detect/adenovirus_detection/weights/best.pt "{best_model_path}"

print("Model saved!")

# Load the best trained model
print("Loading the best trained YOLOv8 model...")
model = YOLO(best_model_path)

# Evaluate on the test set
print("Running evaluation on test set...")
metrics = model.val(
    data=dataset_yaml_path,
    split='test'
)

print("Evaluation Metrics on Test Set:")
print(metrics)

# 1. Install YOLOv8
!pip install -q ultralytics

import os
import random
import torch
import shutil
from google.colab import drive
from tqdm import tqdm
from ultralytics import YOLO


# Set random seed for reproducibility
random.seed(42)

# Device CPU or GPU
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# 3. Mount Google Drive
drive.mount('/content/drive')

# Check if image and label folder exist
dataset_path = '/content/drive/MyDrive/bbxNoverlap'

# Check for images and labels folders
images_path = os.path.join(dataset_path, 'images')
labels_path = os.path.join(dataset_path, 'labels')

print("Checking if folders exist...")

if os.path.exists(images_path) and os.path.exists(labels_path):
    print("Found both 'images' and 'labels' folders.")
else:
    if not os.path.exists(images_path):
        print(" 'images' folder is missing!")
    if not os.path.exists(labels_path):
        print(" 'labels' folder is missing!")

# Define original and new paths
original_images_path = '/content/drive/MyDrive/.../images'
original_labels_path = '/content/drive/MyDrive/.../labels'
new_base_path = '/content/drive/MyDrive/..._split'

# Image and label destination folders
train_img_dir = os.path.join(new_base_path, 'images/train')
val_img_dir = os.path.join(new_base_path, 'images/val')
test_img_dir = os.path.join(new_base_path, 'images/test')

train_lbl_dir = os.path.join(new_base_path, 'labels/train')
val_lbl_dir = os.path.join(new_base_path, 'labels/val')
test_lbl_dir = os.path.join(new_base_path, 'labels/test')

# Create directories
for path in [train_img_dir, val_img_dir, test_img_dir, train_lbl_dir, val_lbl_dir, test_lbl_dir]:
    os.makedirs(path, exist_ok=True)

# List all images
all_images = [f for f in os.listdir(original_images_path) if f.lower().endswith(('.png'))]
print(f"Found {len(all_images)} images.")

# Shuffle and split
random.shuffle(all_images)

n_total = len(all_images)
n_train = int(0.7 * n_total)
n_val = int(0.15 * n_total)
n_test = n_total - n_train - n_val

train_images = all_images[:n_train]
val_images = all_images[n_train:n_train + n_val]
test_images = all_images[n_train + n_val:]

print(f"Train: {len(train_images)}, Val: {len(val_images)}, Test: {len(test_images)}")

# Move images and corresponding labels
def move_files(file_list, img_dest_dir, lbl_dest_dir):
    for file_name in tqdm(file_list, desc=f"Moving to {img_dest_dir.split('/')[-1]}"):
        src_img_path = os.path.join(original_images_path, file_name)
        dst_img_path = os.path.join(img_dest_dir, file_name)
        shutil.copy2(src_img_path, dst_img_path)

        # Move label
        label_name = os.path.splitext(file_name)[0] + '.txt'
        src_lbl_path = os.path.join(original_labels_path, label_name)
        dst_lbl_path = os.path.join(lbl_dest_dir, label_name)

        if os.path.exists(src_lbl_path):
            shutil.copy2(src_lbl_path, dst_lbl_path)
        else:
            print(f"Label file not found for {file_name}")

# Move all splits
move_files(train_images, train_img_dir, train_lbl_dir)
move_files(val_images, val_img_dir, val_lbl_dir)
move_files(test_images, test_img_dir, test_lbl_dir)

print("Dataset split with images and labels completed!")

# Create dataset.yaml
dataset_yaml_path = os.path.join(new_base_path, 'dataset.yaml')
dataset_yaml = f"""
path: {new_base_path}
train: images/train
val: images/val
test: images/test
names:
  0: adenovirus
"""

with open(dataset_yaml_path, 'w') as f:
    f.write(dataset_yaml)

print("dataset.yaml file created!")

# Load a new YOLO model
print("Loading YOLOv8 model for training...")
model = YOLO('yolov8n.pt')  # Nano model

# Train the model with hyperparameters
print("Starting training...")
model.train(
    data=dataset_yaml_path,
    epochs=1000,
    imgsz=640,
    batch=16,
    patience=0,
    name='adenovirus_detection',
    device=device,
    seed=42,
    lr0=0.01,
    optimizer='SGD',
    momentum=0.937,
    weight_decay=0.0005
)

# Save the best model to Drive
best_model_path = '/content/drive/MyDrive/best_adenovirus_model.pt'
print(f"Saving best model to {best_model_path}...")
!cp /content/runs/detect/adenovirus_detection/weights/best.pt "{best_model_path}"

print("Model saved!")

# Load the best trained model
print("Loading the best trained YOLOv8 model...")
model = YOLO(best_model_path)

# Evaluate on the test set
print("Running evaluation on test set...")
metrics = model.val(
    data=dataset_yaml_path,
    split='test'
)

print("Evaluation Metrics on Test Set:")
print(metrics)
