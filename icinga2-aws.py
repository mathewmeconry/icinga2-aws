import boto3
import argparse
import os
import shutil
import subprocess
import configparser
import sys

def writeTemplate(template, targetFile, targetFolder, instance):
    with open(icinga2ConfigDir + 'conf.d/hosts/' + targetFolder + '/' + targetFile + '.conf', 'w') as out:
        template = template
        template = template.replace('{HOST}', instance.id)
        template = template.replace('{PrivateIP}', instance.private_ip_address)

        if instance.public_ip_address:
            template = template.replace(
                '{PublicIP}', instance.public_ip_address)
            # Backwards compatibility
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
    for x in walklevel(icinga2ConfigDir + "conf.d/hosts/"):
        instanceActive = False
        if (x[0].find('i-') > -1):
            folder_instance_id = x[0].split("/")[-1]
            for instance in instances:
                if folder_instance_id == instance.id:
                    instanceActive = True

            if instanceActive == False:
                shutil.rmtree(x[0])
                for directory in os.listdir(config['Default']['pnp4nagiosPerfDataFolder']):
                    if(directory.find(folder_instance_id) > -1):
                        if os.path.exists(config['Default']['pnp4nagiosPerfDataFolder'] + directory):
                            shutil.rmtree(
                                config['Default']['pnp4nagiosPerfDataFolder'] + folder_instance_id)

def get_instances(tags):
    filters = []
    filters.append({"Name": 'instance-state-name', "Values": ['running']})
    for tag in tags:
        tag = tag.split(':')
        filters.append({"Name": "tag:" + tag[0], "Values": [tag[1]]})

    ec2 = boto3.resource('ec2')
    instances = ec2.instances.filter(
    Filters=filters)

    return instances

def create_configs(instances, templateHost, templateCheck, noClean):
    for instance in instances:
        if not os.path.exists(icinga2ConfigDir + "conf.d/hosts/" + instance.id):
            os.makedirs(icinga2ConfigDir + "conf.d/hosts/" + instance.id)
            writeTemplate(templateHost, instance.id, instance.id, instance)
            writeTemplate(templateCheck, 'checks', instance.id, instance)

    if noClean == False or noClean == None:
        cleanupHosts(instances)

def __add_main_parser(parser):
    parser.add_argument('-t', '--tags', nargs='+', required=True,
                    help='Tag Filter: Key value pair')
    parser.add_argument('-th', '--template-host', dest='templateHost', type=open,
                        required=True, help='Which Template should be used for the host')
    parser.add_argument('-tc', '--template-check', dest='templateCheck', type=open,
                        required=True, help='Which Template should be used for the checks')
    parser.add_argument('-nc', '--no-clean', dest='noClean',
                        default=False, action='store_true', required=False, help='Don\'t clean host folders')

def __add_clean_parser(parser):
    subparsers = parser.add_subparsers(
        title='subcommands', description='valid subcommands', help='additional help', dest="command")
        
    parser_clean = subparsers.add_parser('clean', help='clean help')
    parser_clean.add_argument('-t', '--tags', nargs='+',
                            required=True, help='Tag Filter: Key value pair')

config = configparser.ConfigParser()
config.read('config.ini')

icinga2ConfigDir = config['Default']['icinga2ConfigDir']

parser = argparse.ArgumentParser(description='AWS for Icinga 2')

# little hack to show the correct help and the really required params
if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
    __add_main_parser(parser)
    __add_clean_parser(parser)
elif len(sys.argv) > 1 and sys.argv[1] == 'clean':
    __add_clean_parser(parser)
else:
    __add_main_parser(parser)
    
args = parser.parse_args()

instances = get_instances(args.tags)

if hasattr(args, 'command') and args.command == 'clean':
    cleanupHosts(instances)
else:
    templateHost = args.templateHost.read()
    templateCheck = args.templateCheck.read()
    create_configs(instances, templateHost, templateCheck, args.noClean)


subprocess.call(config['Default']['icinga2ReloadCommand'], shell=True)
