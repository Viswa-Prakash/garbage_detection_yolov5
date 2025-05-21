# garbage_detection_yolov5# 🗑️ Garbage Classification using YOLOv5

**GC-YOLOv5** is a computer vision project that automates the detection and classification of garbage into six categories using the YOLOv5 object detection model. The goal is to enhance waste segregation efficiency and reduce human effort in the sorting process.

[datalink](https://universe.roboflow.com/material-identification/garbage-classification-3/dataset/2)

### 🔍 Classes Detected:
- **BIODEGRADABLE**
- **CARDBOARD**
- **GLASS**
- **METAL**
- **PAPER**
- **PLASTIC**

---

## 📊 End-to-End Automated Pipeline

### 📥 1. Data Ingestion
- Annotated garbage images using [Roboflow](https://roboflow.com/) in YOLO format.
- Exported and downloaded as a `.zip` file.
- Extracted images and labels for training.

### ✅ 2. Data Validation
- Checks the presence of expected files and folders.
- Verifies consistency between images and label files.
- Training only proceeds if validation passes.

### 🔄 3. Data Transformation
- No transformation required.
- YOLOv5 handles resizing and augmentation during training internally.

### 🧠 4. Model Training
- Fine-tuned a pre-trained YOLOv5 model on the annotated dataset.
- Real-time object detection across the six garbage categories.
- YOLOv5 provides faster and more accurate detection due to fewer parameters and optimized architecture.

### 📤 5. Model Pusher
- Final trained model weights are saved and pushed to an AWS S3 bucket for safe storage and deployment.

### ☁️ 6. Deployment
- Deployed the entire pipeline on **AWS EC2** using:
  - **Docker** for containerization
  - **AWS ECR** for container registry
  - **GitHub Actions** for CI/CD pipeline

### 🌐 7. Web Application
- A simple **Flask** web app allows users to upload garbage images.
- Returns real-time predictions with bounding boxes and labels.

---

## 🛠️ Tech Stack

- **YOLOv5 (PyTorch)**
- **Roboflow** for image annotation
- **AWS EC2 / S3 / ECR**
- **Docker**
- **GitHub Actions** (CI/CD)
- **Flask** (Web Application)

---


## 🧾 Git Commands

```bash
git add .
git commit -m "Updated"
git push origin main

## ▶️ How to Run Locally

```bash
conda create -n garbage python=3.10 -y
conda activate garbage
pip install -r requirements.txt
python app.py

## ☁️ AWS CLI Configuration
```bash
aws configure

## 🚀 AWS CI/CD Deployment with GitHub Actions
🔐 1. IAM Setup
 - Log in to your AWS Console.
 - Create a new IAM user with programmatic access.
 - Assign the following policies:
  - AmazonEC2ContainerRegistryFullAccess
  - AmazonEC2FullAccess

📦 2. ECR (Elastic Container Registry)
 - Create an ECR repository to store Docker images.
 - Example ECR URI: 637423357032.dkr.ecr.us-east-2.amazonaws.com/yolov5ecr

 💻 3. EC2 (Elastic Compute Cloud)
 - Launch a new EC2 Ubuntu instance.
 - Connect to the instance and install Docker:
 
 ```bash
 # Optional
sudo apt-get update -y
sudo apt-get upgrade

# Required
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker


## 🧪 GitHub Actions Workflow
 ## 🏃‍♂️ 4. Configure EC2 as a Self-hosted Runner
 1. Go to your GitHub repo:
    Settings → Actions → Runners → New self-hosted runner

 2. Choose OS (Ubuntu) and follow the setup commands provided.
 - 🔑 5. Set GitHub Secrets
  - Go to Settings → Secrets and variables → Actions and add the following:
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - AWS_REGION = us-east-2
    - AWS_ECR_LOGIN_URI = 637423357032.dkr.ecr.us-east-2.amazonaws.com
    - ECR_REPOSITORY_NAME = yolov5ecr