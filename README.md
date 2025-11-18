# MLOps Major Assignment

This repository contains a small example ML web app and CI setup used for the course assignment.

Contents
- `train.py` - trains a tiny classifier and writes `models/savedmodel.pth`.
- `app.py` - a small Flask app that loads the model and exposes a prediction endpoint and an upload page.
- `test.py` - pytest tests for basic model load and prediction.
- `Dockerfile` - container image for the app.
- `k8s/` - Kubernetes `deployment.yaml` and `service.yaml` for deploying the app.
- `.github/workflows/ci.yml` - CI workflow to run tests.

Quick start (local)

1. Create a virtualenv and install deps:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Train a model (writes `models/savedmodel.pth`):

```bash
python train.py
```

3. Run the app locally:

```bash
python app.py
```

4. Run tests:

```bash
pytest -q
```

Docker

Build and run the image:

```bash
docker build -t mlops-assignment:latest .
docker run -p 5000:5000 mlops-assignment:latest
```

Kubernetes

Apply manifests in `k8s/` to deploy the app in a cluster (adjust image name).

Notes
- The model file is saved to `models/savedmodel.pth` by `train.py` using joblib. The `.pth` extension is a filename choice (it is a joblib file).
 
Makefile and automation

This repo includes a `Makefile` to automate common local dev tasks. Targets:

- `make build` — build the Docker image locally (tag `olivetti:latest` by default).
- `make load` — load the locally-built image into minikube so the cluster can use it.
- `make deploy` — apply the k8s manifests in `k8s/`.
- `make restart` — restart the deployment and wait for rollout to finish.
- `make status` — show pod status for the app.
- `make clean` — delete k8s resources and remove the local image.

Quick local workflow:

```bash
# build, load into minikube, deploy and wait
make build
make load
make deploy
make restart
make status
```

CI and deploy (GitHub Actions)

Two workflow templates are included:

- `.github/workflows/ci-build.yml` — runs on push, installs Python deps and runs tests, and builds the image on the runner (no push).
- `.github/workflows/deploy.yml` — a manual (workflow_dispatch) workflow that can push the image to a registry and deploy manifests to a cluster when you provide registry credentials and a kubeconfig as encrypted secrets in the repo. Review the workflow and add the required secrets before enabling automatic deploys.

If you'd like, I can help wire up GitHub Packages/ghcr or Docker Hub credentials and enable the deploy workflow.
