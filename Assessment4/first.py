

# Phase 1 – Create Ubuntu EC2

Launch:

```text
AMI: Ubuntu Server 24.04 LTS
Instance Type: t3.small

Storage:
30 GB gp3

Security Group:
22 SSH
80 HTTP
443 HTTPS
8080 (optional)
```

Connect:

```bash
ssh -i key.pem ubuntu@PUBLIC_IP
```

---

# Update Server

```bash
sudo apt update
sudo apt upgrade -y
```

---

# Install Git

```bash
sudo apt install git -y
```

Verify:

```bash
git --version
```

---

# Install Docker

```bash
curl -fsSL https://get.docker.com | sudo sh
```

Add user:

```bash
sudo usermod -aG docker ubuntu
```

Apply:

```bash
newgrp docker
```

Verify:

```bash
docker version
```

---

# Install AWS CLI

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o awscliv2.zip
```

```bash
sudo apt install unzip -y
```

```bash
unzip awscliv2.zip
```

```bash
sudo ./aws/install
```

Verify:

```bash
aws --version
```

---

# Configure AWS

```bash
aws configure
```

Enter:

```text
Access Key
Secret Key
Region
Output=json
```

Verify:

```bash
aws sts get-caller-identity
```

---

# Install kubectl

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s \
https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
```

```bash
chmod +x kubectl
```

```bash
sudo mv kubectl /usr/local/bin/
```

Verify:

```bash
kubectl version --client
```

---

# Install eksctl

```bash
curl --silent --location \
"https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" \
| tar xz -C /tmp
```

```bash
sudo mv /tmp/eksctl /usr/local/bin
```

Verify:

```bash
eksctl version
```

---

# Install Helm

```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

Verify:

```bash
helm version
```

---

# Create EKS Cluster

Create file:

```yaml
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: shine-cluster
  region: ap-south-1

managedNodeGroups:
  - name: shine-devops-ng
    instanceType: t3.small
    desiredCapacity: 2
    minSize: 2
    maxSize: 3

    ssh:
      allow: true
```

Save as:

```bash
cluster.yaml
```

Create cluster:

```bash
eksctl create cluster -f cluster.yaml
```

Time:

```text
20–30 minutes
```

---

# Verify Cluster

```bash
kubectl get nodes
```

Expected:

```text
ip-xxx Ready
ip-xxx Ready
```

---

# Create Namespaces

```bash
kubectl create namespace production
```

```bash
kubectl create namespace argocd
```

```bash
kubectl create namespace monitoring
```

Verify:

```bash
kubectl get ns
```

---

# Install ArgoCD

```bash
kubectl apply -n argocd \
-f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Wait:

```bash
kubectl get pods -n argocd
```

All should be:

```text
Running
```

