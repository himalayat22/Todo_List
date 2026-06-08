Based on everything you've shown, here's the **clean, correct end-to-end process** for your GitOps/AIOps assessment using:

* GitHub
* GitHub Actions
* Docker Hub
* EKS
* Helm
* ArgoCD
* Argo Rollouts

---

# Phase 1: Prepare the Application

## Step 1: Clone Repository

On your EC2 instance:

```bash
git clone https://github.com/Msocial123/Shine-GitOps-Project.git
cd Shine-GitOps-Project
```

---

## Step 2: Test Docker Build

```bash
docker build -t shine-app .
```

Verify:

```bash
docker images
```

---

## Step 3: Push Image to Docker Hub

Login:

```bash
docker login
```

Tag image:

```bash
docker tag shine-app YOUR_DOCKERHUB_USERNAME/shine-app:latest
```

Push:

```bash
docker push YOUR_DOCKERHUB_USERNAME/shine-app:latest
```

---

## Step 4: Update Helm Chart

Edit:

```bash
nano Retail-chart/values.yaml
```

Change:

```yaml
userprofile:
  image: YOUR_DOCKERHUB_USERNAME/shine-app:latest
```

Save.

Commit:

```bash
git add .
git commit -m "Updated image"
git push origin main
```

---

# Phase 2: Configure GitHub Actions

## Step 5: Create Docker Hub Access Token

Docker Hub → Account Settings → Security → Access Tokens

Create token.

---

## Step 6: Add GitHub Secrets

GitHub Repository:

Settings → Secrets and Variables → Actions

Add:

```text
DOCKER_USERNAME
```

Value:

```text
your dockerhub username
```

Add:

```text
DOCKER_PASSWORD
```

Value:

```text
dockerhub access token
```

---

## Step 7: Verify Workflow

File:

```text
.github/workflows/*.yml
```

Workflow should:

```text
Build Docker Image
Login to DockerHub
Push Docker Image
```

Commit and push.

---

# Phase 3: Create EKS Cluster

## Step 8: Verify EKS

```bash
kubectl get nodes
```

Expected:

```text
Ready
```

nodes should be visible.

---

## Step 9: Create Namespace

```bash
kubectl create namespace shine
```

Verify:

```bash
kubectl get ns
```

---

# Phase 4: Install ArgoCD

## Step 10: Create Namespace

```bash
kubectl create namespace argocd
```

---

## Step 11: Install ArgoCD

```bash
kubectl apply -n argocd \
-f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Wait:

```bash
kubectl get pods -n argocd
```

All should be Running.

---

## Step 12: Expose ArgoCD

```bash
kubectl patch svc argocd-server \
-n argocd \
-p '{"spec":{"type":"LoadBalancer"}}'
```

Check:

```bash
kubectl get svc -n argocd
```

Note External IP / DNS.

---

## Step 13: Get Password

```bash
argocd admin initial-password -n argocd
```

Username:

```text
admin
```

Password:

```text
output of command
```

---

## Step 14: Open ArgoCD

Browser:

```text
http://<ARGOCD-LOADBALANCER>
```

Login.

---

# Phase 5: Install Argo Rollouts

Your chart contains:

```text
userprofile-rollout.yml
```

Therefore Rollouts must be installed.

---

## Step 15: Install Rollouts

```bash
kubectl create namespace argo-rollouts
```

```bash
kubectl apply -n argo-rollouts \
-f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml
```

Verify:

```bash
kubectl get pods -n argo-rollouts
```

---

## Step 16: Verify CRD

```bash
kubectl get crd | grep rollout
```

Expected:

```text
rollouts.argoproj.io
```

---

# Phase 6: Create ArgoCD Application

Inside ArgoCD UI:

---

### General

```text
Application Name:
shine-app

Project:
default

Sync Policy:
Automatic
```

Enable:

```text
Auto Create Namespace
Prune Resources
Self Heal
```

---

### Source

```text
Repository URL:
https://github.com/Msocial123/Shine-GitOps-Project.git

Revision:
HEAD

Path:
Retail-chart
```

---

### Destination

```text
Cluster:
https://kubernetes.default.svc

Namespace:
shine
```

---

Click:

```text
Create
```

---

# Phase 7: Sync Application

Click:

```text
SYNC
```

Then:

```text
SYNCHRONIZE
```

Wait until:

```text
Healthy
Synced
```

---

# Phase 8: Verify Deployment

Check:

```bash
kubectl get pods -n shine
```

Expected:

```text
mongodb-deployment
userprofile-rollout
```

Running.

---

Check services:

```bash
kubectl get svc -n shine
```

Expected:

```text
mongodb-service
usernode-service
```

---

# Phase 9: Get Application URL

```bash
kubectl get svc -n shine
```

Look for:

```text
EXTERNAL-IP
```

Open:

```text
http://<external-ip>
```

Application should load.

---

# If Helm Gives Errors

Since you've already seen:

```text
userprofile-secret exists
```

Clean the namespace before retrying Helm tests:

```bash
kubectl delete secret userprofile-secret -n shine
```

or

```bash
kubectl delete namespace shine
kubectl create namespace shine
```

Then:

```bash
helm install shine-app ./Retail-chart -n shine
```

---

# Evidence/Screenshots for Report

Take screenshots of:

1. GitHub Repository
2. GitHub Actions successful run
3. Docker Hub image
4. EKS Nodes

```bash
kubectl get nodes
```

5. ArgoCD Dashboard showing:

```text
Healthy
Synced
```

6. Rollout resources

```bash
kubectl get rollouts -n shine
```

7. Pods

```bash
kubectl get pods -n shine
```

8. Services

```bash
kubectl get svc -n shine
```

9. Application running in browser

This is the complete workflow your project structure is designed to follow. The key thing now is **don't mix Helm manual deployment and ArgoCD deployment in the same namespace**. For the assessment, use **ArgoCD as the deployment method** after installing Argo Rollouts.
