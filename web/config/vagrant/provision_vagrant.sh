#!/bin/bash

set -e

apt update
apt -y upgrade

timedatectl set-timezone America/New_York

# Install Python 3.8
apt -y install python3
apt -y install python3-pip python3-venv python3-virtualenv

# Install firejail
apt install -y firejail

# Install Docker
apt -y install docker.io
systemctl enable docker containerd
systemctl start docker containerd
usermod -aG docker vagrant

# PostsgreSQL
apt -y install postgresql
apt -y install postgresql-contrib
apt -y install libpq-dev

sqlcmd(){
    sudo -u postgres psql -U postgres -d postgres -c "$@"
}
sqlcmd "CREATE DATABASE codingclash;" || echo Database already exists
sqlcmd "CREATE USER codingclash PASSWORD 'pwd';" || echo Database user already exists
sed -Ei "s/(^local +all +all +)peer$/\1md5/g" /etc/postgresql/12/main/pg_hba.conf
service postgresql restart

# Setup Project
cd codingclash
rm -rf venv
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
cp -n codingclash/settings/secret.sample.py codingclash/settings/secret.py

python3 manage.py migrate
python3 manage.py collectstatic --noinput
