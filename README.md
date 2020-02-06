# tmpscripts_gce
捨てPython scriptをGCEで実行させて、終了後にインスタンスが停止する仕組み

# 捨てscriptの実行手順

- サービスアカウントを作成する
- バケットを作成する
- deploy_src/requirements.txt に必要なパッケージ名を追加する
- startup.pyのmain関数を実装する
- service_account、project_id、bucket部分を置き換えて以下のshellを実行していく
    - `gcloud beta compute`でGCEインスタンスが立ち上がる。(経過はstackdriverで"")

``` {bash}
# tmpscripts_gce直下で実行しましょう

# GCPアカウント
service_account='xxxxxxx@developer.gserviceaccount.com'
project_id=xxxxxxx
bucket=xxxxxxx

# startup.pyに渡したい引数を指定
arg1=hoge
arg2=fuga

# マシンスペックを決めましょう
machine_type=n1-standard-1
boot_disk_size=10G

# deploy_srcをbucketのtopに配置する
gsutil cp -r ./deploy_src/ gs://$bucket

# GCEでスクリプトを実行する
instance_name=vm-${arg1}-${arg2}
gcloud beta compute \
 --project=${project_id} instances create ${instance_name} \
 --zone=us-central1-a \
 --machine-type=${machine_type} \
 --subnet=default \
 --network-tier=PREMIUM \
 --metadata=arg1=${arg1},arg2=${arg2},bucket=${bucket} \
 --maintenance-policy=MIGRATE \
 --service-account=${service_account} \
 --scopes=https://www.googleapis.com/auth/cloud-platform \
 --image=ubuntu-1910-eoan-v20191217 \
 --image-project=ubuntu-os-cloud \
 --boot-disk-size=${boot_disk_size} \
 --boot-disk-type=pd-standard \
 --boot-disk-device-name=${instance_name} \
 --reservation-affinity=any \
 --metadata-from-file=startup-script=./startup-script.sh
```