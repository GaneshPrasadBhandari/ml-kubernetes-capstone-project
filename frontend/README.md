# 🚀 MSIT 3404 Kubernetes Capstone Project: Two-Tier Deployment

This repository contains the finalized code and deployment manifests for a scaled, two-tier application deployed on **Minikube**.

**Student Name:** Ganesh Prasad Bhandari
**Submission Date:** 23rd Nov 2025
**Docker Hub Namespace:** `ganeshprasadbhandari`

## 1. Project Overview and Status

The application consists of a **Python Flask Backend** (using Gunicorn) and an **Nginx Frontend**.

**Final Status:** All technical requirements are met. The application is scaled correctly (4 Frontend, 3 Backend), communication is successful (**CORS-enabled**), and the required static image is served from the backend and displayed on the frontend.

| Component | Technology | Replicas | Port | Functionality |
| :--- | :--- | :--- | :--- | :--- |
| **Backend** | Python/Flask/Gunicorn | **3** | 5000 | `/api/hello` endpoint, **CORS enabled**, serves static image. |
| **Frontend** | Nginx/HTML/JavaScript | **4** | 80 | Displays webpage, calls backend API, displays static image. |

## 2. Repository Structure and Code Changes

| File | Location | Purpose |
| :--- | :--- | :--- |
| `backend/app.py` | `backend/` | Includes `from flask_cors import CORS` and `CORS(app)` to fix the browser communication error. |
| `backend/Dockerfile` | `backend/` | Includes `COPY static /app/static` to copy the image file. |
| `frontend/index.html` | `frontend/` | Includes `<img src="http://backend-service:5000/static/myimage.jpg"...` to display the static image. |
| `backend.yaml` | Root | Configures Deployment (**3 replicas**) and NodePort Service (30001). **Includes `imagePullPolicy: Always`**. |
| `frontend.yaml` | Root | Configures Deployment (**4 replicas**) and NodePort Service (30002). **Includes `imagePullPolicy: Always`**. |

---

## 3. Setup and Image Preparation

### Step 3.1: Start Minikube and Set Docker Context
Start your Minikube cluster and ensure your Docker command line is building images directly into the Minikube environment.

```bash
minikube start
eval $(minikube docker-env)
```

**Step 3.2: Build and Push Final Images**
Build the finalized images (which contain the working CORS fix, static files, and image link) and push them to your Docker Hub.

```bash
# Build and Push Backend Image (Python/Flask)
docker build -t ganeshprasadbhandari/backend-app:latest ./backend
docker push ganeshprasadbhandari/backend-app:latest

# Build and Push Frontend Image (Nginx)
docker build -t ganeshprasadbhandari/frontend-app:latest ./frontend
docker push ganeshprasadbhandari/frontend-app:latest
```


**4.Kubernetes Deployment and Configuration**
Step 4.1: Deploy Manifests
Apply the YAML files. The included imagePullPolicy: Always will force Minikube to use the newly pushed images, resolving the final cache issue.

```bash
kubectl apply -f backend.yaml
kubectl apply -f frontend.yaml
```

**Step 4.2: Verify Pod Scaling**
Confirm that all required Pods are running (4 frontend and 3 backend).

```bash
kubectl get pods
```

**Step 4.3: Verify Services**
Check that the NodePort Services are active and correctly mapped.

```bash
kubectl get svc
```

**Step 4.4: Apply Custom Label (Assignment Requirement)**
Apply the required custom label to a specific pod for demonstration.

```bash
# 1. Get the name of one of your running frontend pods
kubectl get pods -l app=frontend 

# 2. Apply the label (Replace <POD_NAME> with the actual pod name)
kubectl label pod <POD_NAME> run=testp

# 3. Verify the label is present
kubectl get pods --show-labels
```

**5. Verification and Diagnostics**
Step 5.1: Internal Connectivity Test (Proof of concept)
This test confirms that internal Kubernetes DNS and routing are perfectly functional, proving that the previous browser error was a CORS/External issue.

```bash
# 1. Get the name of a frontend pod again
kubectl get pods -l app=frontend 

# 2. Execute curl from the frontend pod to the backend service
kubectl exec -it <FRONTEND_POD_NAME> -- curl http://backend-service:5000/api/hello
# Expected Output: {"message": "Hello from Flask backend!"}
```

**Step 5.2: Final End-to-End Browser Test**
Stop any existing tunnels and open the finalized application in the browser.

```bash
# Stop any active minikube service sessions (Ctrl+C)

# Open the frontend service
minikube service frontend-service
```

**Expected Outcome:** Both the static JPEG image loads, and clicking the "Call Backend API" button successfully shows the JSON response.

**6. Git Submission**
Use these commands to initialize your repository, commit all the finalized files (including the YAMLs, Dockerfiles, and code), and push everything to your GitHub repository for submission.

```bash
# Initialize a new Git repository
git init

# Stage ALL project files
git add .

# Commit all changes
git commit -m "Finalizing project code and configurations: Implemented CORS fix, image serving, imagePullPolicy: Always in YAMLs, and created submission files."

# Connect to GitHub and push (REPLACE THE URL with your actual repository URL)
git branch -M main
git remote add origin [https://github.com/GaneshPrasadBhandari/ml-kubernetes-capstone.git](https://github.com/GaneshPrasadBhandari/ml-kubernetes-capstone.git)
git push -u origin main
```