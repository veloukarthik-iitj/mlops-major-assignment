#!/usr/bin/env bash
set -euo pipefail

# Local deploy helper: builds image, loads into minikube and deploys k8s manifests.
# Usage: ./deploy/local.sh

IMAGE=${IMAGE:-olivetti:latest}

echo "Building ${IMAGE}"
docker build -t "${IMAGE}" .

echo "Loading ${IMAGE} into minikube"
minikube image load "${IMAGE}"

echo "Applying k8s manifests"
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

echo "Restarting deployment and waiting for rollout"
kubectl rollout restart deployment/olivetti-app
kubectl rollout status deployment/olivetti-app --timeout=120s

echo "Done. Run 'kubectl get pods -l app=olivetti -o wide' to check status."
