# github-django-actions

## To activate this environment, use

``` Bash
conda activate github-action
```

## To deactivate an active environment, use

``` Bash
conda deactivate
```

## Connect to cluster

``` Bash
aws eks --region us-east-1 update-kubeconfig --name eks-dev-cluster
```

## ssh into pods

``` Bash
kubectl exec -it <PODID> bash
```

``` Bash
kubectl exec -it "$(kubectl get pods | awk '$0 ~ /app-deployment-/ {print $1}' | head -1)" bash
```

``` Bash
# Check manage.py
python manage.py check
```

``` Bash
# Check manage.py
python manage.py shell

# import
from django.conf import settings
print(settings.DATABASES)
```

## Migrate DB

``` Bash
kubectl exec -it "$(kubectl get pods | awk '$0 ~ /app-deployment-/ {print $1}' | head -1)" python manage.py migrate
```

## Create Superuser

``` Bash
kubectl exec -it "$(kubectl get pods | awk '$0 ~ /app-deployment-/ {print $1}' | head -1)" python manage.py createsuperuser
```

## [Blog post](https://medium.com/intelligentmachines/github-actions-end-to-end-ci-cd-pipeline-for-django-5d48d6f00abf)

## [Github Action with EKS](https://dev.to/leandronsp/deploy-to-kubernetes-using-github-actions-including-slack-notification-11je)

## [Helm 3 Github Action](https://github.com/marketplace/actions/helm-3)

## [Kubernetes unnecessarily requiring quoting on numeric env vars](https://github.com/kubernetes/kubernetes/issues/82296)

## [DGANGO wildcard in ALLOWED HOST](https://xxx-cook-book.gitbooks.io/django-cook-book/content/Settings/allowed-hosts.html)

## [Storing Django static files on S3](https://testdriven.io/blog/storing-django-static-and-media-files-on-amazon-s3/)
