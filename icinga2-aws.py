import boto3
import argparse
import os
import shutil
import subprocess

def writeTemplate(template, targetFile, targetFolder):
    with open('/etc/icinga2/conf.d/hosts/' + targetFolder + '/' + targetFile + '.conf', 'w') as out:
        template = template
        template = template.replace('{HOST}', instance.id)
        template = template.replace('{IP}', instance.public_ip_address)
        out.write(template)
        out.flush()

    out.close()

def walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]

def cleanupHosts(instances):
    for x in walklevel("/etc/icinga2/conf.d/hosts/"):
        instanceActive = False
        if (x[0].find('i-') > -1):
            for instance in instances:
                if x[0].split("/")[-1] == instance.id:
                    instanceActive = True

            if instanceActive == False:
                shutil.rmtree(x[0])

parser = argparse.ArgumentParser(description='AWS for Icinga 2')
parser.add_argument('-t', '--tags', nargs='+', required=True, help='Tag Filter: Key value pair')
parser.add_argument('-th', '--template-host', dest='templateHost', type=open, required=True, help='Which Template should be used for the host')
parser.add_argument('-tc', '--template-check', dest='templateCheck', type=open, required=True, help='Which Template should be used for the checks')

args = parser.parse_args()

filters = []

for tag in args.tags:
    tag = tag.split(':')
    filters.append({"Name": "tag:"+tag[0], "Values": [tag[1]]})


ec2 = boto3.resource('ec2')
templateHost = args.templateHost.read()
templateCheck = args.templateCheck.read()

instances = ec2.instances.filter(
    Filters=filters)

for instance in instances:
    if not os.path.exists("/etc/icinga2/conf.d/hosts/" + instance.id):
        os.makedirs("/etc/icinga2/conf.d/hosts/" + instance.id)
        writeTemplate(templateHost, instance.id, instance.id)
        writeTemplate(templateCheck, 'checks', instance.id)

cleanupHosts(instances)

subprocess.call('/etc/init.d/icinga2 reload')

