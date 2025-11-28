# 🚀 ML Kubernetes Capstone Project

**Course:** MSIT 3404 – DevOps & Cloud Computing  
**Student:** Ganesh Prasad Bhandari  
**Repository:** https://github.com/GaneshPrasadBhandari/ml-kubernetes-capstone-project

This project demonstrates a full **containerized multi-tier application** deployed on **Kubernetes (Minikube)** using:

- **Flask** backend API (Python)
- **Nginx** frontend (HTML + JS)
- **Docker** containers
- **Docker Hub** for image hosting
- **Kubernetes Deployments + Services**
- **NodePort** + `minikube service` for external access

The final app:

- Shows an **image served from the backend**  
- Calls a **backend API** on button click and displays JSON response  
- Runs as **two microservices** inside a local Kubernetes cluster

---

## 🧱 1. Architecture Overview

**Frontend (Nginx)**  
- Serves `index.html`  
- Calls `/api/hello` and `/api/image` (relative URLs)  
- Uses Nginx **reverse proxy** to forward `/api/*` to `backend-service:5000` inside the cluster  

**Backend (Flask)**  
- `/api/hello` → returns JSON  
- `/api/image` → returns image (`static/myimage.jpg`)  
- Runs on port `5000` in container  

**Kubernetes Objects**

- `backend-deployment` (2 replicas)  
- `frontend-deployment` (2 replicas)  
- `backend-service` (ClusterIP)  
- `frontend-service` (NodePort 30002)  

**Request Flow**

```text
Browser → frontend-service (NodePort)
        → Nginx (pod) → proxy /api/* → backend-service:5000
        → Flask backend → JSON / image → back to browser

**📁 2. Project Structure**

ml-kubernetes-capstone-project/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── static/
│       └── myimage.jpg
├── frontend/
│   ├── index.html
│   ├── nginx.conf
│   └── Dockerfile
├── k8s/
│   ├── backend.yaml
│   └── frontend.yaml
├── .gitignore
└── README.md


**🛠 3. Prerequisites**

On Windows 10/11 with WSL2 (Ubuntu):

 Docker Desktop installed and running (with WSL2 integration enabled)

 WSL2 Ubuntu (20.04 or 22.04)

 kubectl installed

 Minikube installed (using Docker driver)

 Git installed in WSL

Check versions inside WSL:

```bash
docker --version
kubectl version --client
minikube version
git --version
```

**🌐 4. Clone the Repository (WSL)**

```bash
cd /mnt/d/myeuron/clark_university/project_assignments_fall2025

# Clone using SSH (recommended)
git clone git@github.com:GaneshPrasadBhandari/ml-kubernetes-capstone-project.git

cd ml-kubernetes-capstone-project
pwd        # confirm you are in the project folder
ls
```

If using HTTPS instead of SSH:

```bash
git clone https://github.com/GaneshPrasadBhandari/ml-kubernetes-capstone-project.git
```

**👤 5. (Optional) Git One-Time Setup in WSL**

```bash
git config --global user.name "Ganesh Prasad Bhandari"
git config --global user.email "your_github_email@example.com"

git config --global --list   # verify
```

**🐍 6. (Optional) Local Python Virtual Environment**

Only needed if you want to run backend locally (without Docker).

```bash
cd backend

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python app.py   # Flask dev server on port 5000

# When done
deactivate
```

**🐳 7. Build & Push Docker Images**

Important: These commands assume Docker Hub username ganeshprasadbhandari.
If you fork this repo, change the username or use minikube image load.

From the project root:

```bash
cd /mnt/d/myeuron/clark_university/project_assignments_fall2025/ml-kubernetes-capstone-project
```

**7.1 Backend Image**

```bash
# Build backend image
docker build -t backend-app:latest ./backend

# Tag for Docker Hub
docker tag backend-app:latest ganeshprasadbhandari/backend-app:latest

# Login and push
docker login
docker push ganeshprasadbhandari/backend-app:latest
```

**7.2 Frontend Image**

```bash
# Build frontend image
docker build -t frontend-app:latest ./frontend

# Tag for Docker Hub
docker tag frontend-app:latest ganeshprasadbhandari/frontend-app:latest

# Push
docker push ganeshprasadbhandari/frontend-app:latest
```

**☸️ 8. Start Minikube (Docker Driver)**

```bash
minikube start --driver=docker

minikube status    # should show kubelet, apiserver, etc. "Running"
kubectl get nodes  # should show 'minikube' in Ready state
```

If you later restart your machine and cluster stops:
```bash
minikube start --driver=docker
```

**📦 9. Deploy to Kubernetes**

From project root:

9.1 Apply Backend

```bash
kubectl apply -f k8s/backend.yaml

kubectl get pods -o wide
kubectl get svc
```
Expected:

Backend pods: backend-deployment-xxxx in Running

Service: backend-service (ClusterIP, port 5000)


**9.2 Apply Frontend**

```bash
kubectl apply -f k8s/frontend.yaml

kubectl get pods -o wide
kubectl get svc
```

Expected:

Frontend pods: frontend-deployment-xxxx in Running

Service: frontend-service as NodePort on 30002
(e.g., 80:30002/TCP)

**🌐 10. Access the Application**
Option A – Using minikube service (recommended)

```bash
minikube service frontend-service --url
```

This prints a URL such as:
```bash
http://127.0.0.1:41459
```

Open that URL in your Windows browser.

You should see:

Page title: Frontend Nginx App

An image (served from backend)

A button “Call Backend API”

Clicking the button shows JSON from backend, for example:

```bash
{
  "message": "Hello from Flask backend via Kubernetes!"
}
```

**Option B – Direct NodePort Access**

You can also use the Minikube IP and NodePort:

```bash
Option B – Direct NodePort Access

You can also use the Minikube IP and NodePort:
```

Then open in browser:
```bash
http://<MINIKUBE_IP>:30002
```

Example:
```bash
http://192.168.49.2:30002
```

**🔧 11. Useful Kubernetes Commands**

```bash
# Get all pods (wide info)
kubectl get pods -o wide

# Get all services
kubectl get svc

# Describe a specific pod
kubectl describe pod <pod-name>

# View logs for frontend pods
kubectl logs -l app=frontend

# View logs for backend pods
kubectl logs -l app=backend

# Delete and reapply manifests
kubectl delete -f k8s/frontend.yaml --ignore-not-found
kubectl delete -f k8s/backend.yaml --ignore-not-found

kubectl apply -f k8s/backend.yaml
kubectl apply -f k8s/frontend.yaml
```

**🧪 12. Local Testing of Containers (Optional)**
**Backend Container Locally**

```bash
docker run -d --name backend-local -p 5000:5000 backend-app:latest

curl http://localhost:5000/api/hello
curl http://localhost:5000/api/image --output test.jpg

docker stop backend-local && docker rm backend-local
```

**Frontend Container Locally**

Note: For fully functional local testing, backend URL in index.html must be updated to hit http://host.docker.internal:5000 or similar.
In the Kubernetes version, the frontend always uses /api/* and relies on Nginx proxy to backend-service.

```bash
docker run -d --name frontend-local -p 8080:80 frontend-app:latest
# open http://localhost:8080
docker stop frontend-local && docker rm frontend-local
```

**🧹 13. Stopping / Cleaning Up**

```bash
# Delete Kubernetes resources
kubectl delete -f k8s/frontend.yaml --ignore-not-found
kubectl delete -f k8s/backend.yaml --ignore-not-found

# Stop Minikube (optional)
minikube stop

# Delete Minikube cluster completely (careful)
minikube delete
```

**🧩 14. Common Issues & Troubleshooting**
1. ImagePullBackOff for frontend/backend pods

Check the image name in YAML:
```bash
image: ganeshprasadbhandari/frontend-app:latest
image: ganeshprasadbhandari/backend-app:latest
```

Ensure images exist on Docker Hub:

https://hub.docker.com/r/ganeshprasadbhandari/backend-app

https://hub.docker.com/r/ganeshprasadbhandari/frontend-app

Rebuild and push:
```bash
docker build -t frontend-app:latest ./frontend
docker tag frontend-app:latest ganeshprasadbhandari/frontend-app:latest
docker push ganeshprasadbhandari/frontend-app:latest
```

**2. kubectl errors like connect: connection refused**

Minikube cluster is not running. Start it:
```bash
2. kubectl errors like connect: connection refused

Minikube cluster is not running. Start it:
```

**3. Frontend loads but image/API show TypeError: Failed to fetch**

Make sure Nginx reverse proxy is in place (frontend/nginx.conf):
```bash
location /api/ {
    proxy_pass http://backend-service:5000;
}
```

**Ensure backend pods and backend-service are running:**
```bash
kubectl get pods -l app=backend
kubectl get svc backend-service
```

**📎 15. Git Commands Used (Summary)**

From project root:

```bash
# See status
git status

# Stage all changes
git add .

# Commit
git commit -m "Describe changes"

# Set main branch and push to GitHub
git branch -M main
git remote -v             # verify remote URL
git push -u origin main
```

**👨‍💻 16. Author**

**Ganesh Prasad Bhandari**

MSIT Student – Clark University

Docker, Kubernetes, MLOps & AI Enthusiast

**📜 17. License**

This project is for academic / educational purposes as part of MSIT 3404 – DevOps & Cloud Computing.
You may fork and extend it for learning, but please give proper credit.










