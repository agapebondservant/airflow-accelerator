# Airflow Accelerator

This is an accelerator that can be used to generate a Kubernetes deployment for [Apache Airflow pipelines](https://airflow.apache.org/).

* Install App Accelerator: (see https://docs.vmware.com/en/Tanzu-Application-Platform/1.0/tap/GUID-cert-mgr-contour-fcd-install-cert-mgr.html)
```
tanzu package available list accelerator.apps.tanzu.vmware.com --namespace tap-install
tanzu package install accelerator -p accelerator.apps.tanzu.vmware.com -v 1.0.1 -n tap-install -f resources/app-accelerator-values.yaml
Verify that package is running: tanzu package installed get accelerator -n tap-install
Get the IP address for the App Accelerator API: kubectl get service -n accelerator-system
```

Publish Accelerators:
```
tanzu plugin install --local <path-to-tanzu-cli> all
tanzu acc create airflow --git-repository https://github.com/agapebondservant/airflow-accelerator.git --git-branch main
```

## Contents
1. [Install Airflow via TAP/tanzu cli](#tanzu)
2. [Install Airflow with vanilla Kubernetes](#k8s)
3. [Integrate with TAP](#tapintegrate)

### Install Airflow via TAP/tanzu cli<a name="tanzu"/> (Work in progress)

#### Before you begin (one time setup):
1. Create an environment file `.env` (use `.env-sample` as a template), then run:
```
source .env
```

### Install Airflow via vanilla Kubernetes<a name="k8s"/>
1. Generate an SSH key (enter **airflow** when prompted for file name):
```
ssh-keygen -t rsa -b 4096 -C "airflow@gmail.com"
```

2. In your GitHub repo, go to Settings -> Deploy Keys -> Add deploy key, and copy the contents of **airflow.pub** as a new deploy key.

3. Deploy Airflow:
```
#export AIRFLOW_SSH_SECRET=$(cat airflow | base64)
#envsubst < resources/secret.in.yaml > resources/secret.yaml
helm install airflow bitnami/airflow --version 16.0.0 -f resources/values.yaml --namespace airflow --create-namespace --wait
watch kubectl get all -nairflow
```

4. To uninstall:
```
helm uninstall airflow --namespace airflow
kubectl delete ns airflow
```

Airflow UI should be accessible at http://<LoadBalancerIP>.

#### Before you begin:
Create an environment file `.env` (use `.env-sample` as a template), then run:
```
source .env
```

1. 


## Integrate with TAP<a name="tapintergrate"/>

* Deploy the app:
```
source .env
tanzu apps workload create airflow -f resources/workload.yaml --yes
```

* Tail the logs of the main app:
```
tanzu apps workload tail airflow --since 64h
```

* Once deployment succeeds, get the URL for the main app:
```
tanzu apps workload get airflow     #should yield airflow.default.<your-domain>
```

* To delete the app:
```
tanzu apps workload delete airflow --yes
```
