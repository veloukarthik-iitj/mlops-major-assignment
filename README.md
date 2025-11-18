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

Repository secrets and deployment (how-to)

To enable the deploy workflow to push to Docker Hub and deploy to a cluster you need to add a few repository secrets.

1) Create a Docker Hub access token

- Sign in at https://hub.docker.com
- Go to Account Settings -> Security -> New Access Token
- Give it a name (for CI), create it and copy the token value (you will only see it once).

2) Add GitHub repository secrets

- In your GitHub repository go to Settings -> Security -> Secrets and variables -> Actions -> New repository secret.
- Add the following secrets (exact names used by the workflow):
	- `DOCKERHUB_USERNAME` — your Docker Hub username (for example `karthikvelouiitj`)
	- `DOCKERHUB_TOKEN` — the access token you created above
	- `KUBECONFIG` (optional) — the base64-encoded contents of your kubeconfig file if you want the workflow to deploy automatically to your Kubernetes cluster

How to create the `KUBECONFIG` secret value (example on macOS / Linux):

```bash
# Encode kubeconfig to base64 and copy to clipboard (macOS)
cat ~/.kube/config | base64 | pbcopy

# Or just print the base64 to the terminal and paste it into the GitHub secret value
cat ~/.kube/config | base64
```

Alternatively, you can add the raw kubeconfig as a secret and modify the workflow to use it directly, but the current workflow expects a base64 string.

3) Optional: Update `k8s/deployment.yaml` to reference your Docker Hub image

If you want your manifests to point to the Docker Hub image directly (so other clusters can pull it), edit `k8s/deployment.yaml` and set:

```yaml
image: your-dockerhub-username/olivetti:latest
imagePullPolicy: IfNotPresent
```

Replace `your-dockerhub-username` with the value of `DOCKERHUB_USERNAME` (for example `karthikvelouiitj`). Then commit and push the change so the repo manifest matches the image in the registry.

