IMAGE ?= olivetti:latest
K8S_MANIFESTS := k8s/deployment.yaml k8s/service.yaml

.PHONY: all build load deploy restart status clean tag

all: build load deploy restart status

build:
	docker build -t $(IMAGE) .

load:
	@echo "Loading $(IMAGE) into minikube..."
	minikube image load $(IMAGE)

deploy:
	@echo "Applying k8s manifests..."
	kubectl apply -f k8s/deployment.yaml
	kubectl apply -f k8s/service.yaml

restart:
	@echo "Restarting deployment and waiting for rollout..."
	kubectl rollout restart deployment/olivetti-app
	kubectl rollout status deployment/olivetti-app --timeout=120s

status:
	kubectl get pods -l app=olivetti -o wide

clean:
	kubectl delete -f k8s/deployment.yaml --ignore-not-found
	kubectl delete -f k8s/service.yaml --ignore-not-found
	docker rmi $(IMAGE) || true

tag:
	@echo "Tag current image as $(IMAGE) (no-op if already tagged)"
	docker tag olivetti:latest $(IMAGE) || true
