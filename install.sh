apt-get update
apt-get install -y python3 python3-setuptools python-pip
pip install awscli --ignore-installed six
easy_install3 boto3 pyhton-dateutil
python3 setup.py install