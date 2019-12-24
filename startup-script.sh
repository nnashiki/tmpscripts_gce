#!/bin/bash
echo 'I am '`whoami`

# ロギング エージェントのインストール
curl -sSO https://dl.google.com/cloudagents/install-logging-agent.sh
bash install-logging-agent.sh

# モニタリング エージェントのインストール
curl -sSO https://dl.google.com/cloudagents/install-monitoring-agent.sh
bash install-monitoring-agent.sh

# その他セットアップ
sudo apt update
sudo apt upgrade
sudo apt install -y python3-pip

# ex.
pip3 install google-cloud-bigquery

# カスタムメタデータを取得
readonly ARG1=`curl -sS --fail "http://metadata.google.internal/computeMetadata/v1/instance/attributes/arg1" -H "Metadata-Flavor: Google"`
declare -p ARG1
readonly ARG2=`curl -sS --fail "http://metadata.google.internal/computeMetadata/v1/instance/attributes/arg2" -H "Metadata-Flavor: Google"`
declare -p ARG2
readonly BUCKET=`curl -sS --fail "http://metadata.google.internal/computeMetadata/v1/instance/attributes/bucket" -H "Metadata-Flavor: Google"`
declare -p BUCKET

# ソースをdeployしてPython scriptを実行
gsutil cp -r gs://${BUCKET}/src .
cd src/
python3 hoge.py ${ARG1} ${ARG2}

# GCEインスタンスを終了する
echo "Shutdown itself"
sudo shutdown -h now