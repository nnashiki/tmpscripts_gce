# tmpscripts_gce
捨てscriptをGCEで実行する仕組み


# 捨てscriptの実行手順

- src(deploy_src)をbucketのtopに配置する
- 必要な変数を設定して以下の`gcloud beta compute`を実行する

```
arg1=hoge
arg2=fuga
service_account='xxxxxxx@developer.gserviceaccount.com'
project_id=xxxxxxx
bucket=xxxxxxx

instance_name=vm-${arg1}-${arg2}
echo $instance_name

gcloud beta compute \
 --project=${project_id} instances create ${instance_name} \
 --zone=us-central1-a \
 --machine-type=n1-standard-1 \
 --subnet=default \
 --network-tier=PREMIUM \
 --metadata=arg1=${arg1},arg2=${arg2},bucket=${bucket} \
 --maintenance-policy=MIGRATE \
 --service-account=${service_account} \
 --scopes=https://www.googleapis.com/auth/cloud-platform \
 --image=ubuntu-1910-eoan-v20191217 \
 --image-project=ubuntu-os-cloud \
 --boot-disk-size=10GB \
 --boot-disk-type=pd-standard \
 --boot-disk-device-name=${instance_name} \
 --reservation-affinity=any \
 --metadata-from-file=startup-script=./startup-script.sh
```