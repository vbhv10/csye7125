deploy:
	kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml
	kubectl apply -f dashboard.yaml
	kubectl -n kubernetes-dashboard create token admin-user
	kubectl proxy

deploy-helm:
	( \
		helm repo add kubernetes-dashboard https://kubernetes.github.io/dashboard/; \
		helm upgrade --install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard --create-namespace --namespace kubernetes-dashboard; \
		kubectl apply -f dashboard.yaml; \
		kubectl -n kubernetes-dashboard create token admin-user; \
		export POD_NAME=$$(kubectl get pods -n kubernetes-dashboard -l "app.kubernetes.io/name=kubernetes-dashboard,app.kubernetes.io/instance=kubernetes-dashboard" -o jsonpath="{.items[0].metadata.name}"); \
		echo https://127.0.0.1:8443/; \
		kubectl port-forward $$POD_NAME 8443:8443 -n kubernetes-dashboard; \
	)
