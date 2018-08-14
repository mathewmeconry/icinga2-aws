<snippet>
  <content>
# Icinga2-AWS
Adds dynamically based on the passed filters and templates hosts with checks into icinga 2

## Installation
Run install.sh script
    chmod u+x install.sh
    ./install.sh

## Configfile
- path to the Icinga2 config folder
- command to reload Icinga2 configs

## Usage
usage: icinga2-aws.py [-h] -t TAGS [TAGS ...] -th TEMPLATEHOST -tc
                      TEMPLATECHECK [-nc]
                      {clean} ...

AWS for Icinga 2

optional arguments:
  -h, --help            show this help message and exit
  -t TAGS [TAGS ...], --tags TAGS [TAGS ...]
                        Tag Filter: Key value pair
  -th TEMPLATEHOST, --template-host TEMPLATEHOST
                        Which Template should be used for the host
  -tc TEMPLATECHECK, --template-check TEMPLATECHECK
                        Which Template should be used for the checks
  -nc, --no-clean       Don't clean host folders

subcommands:
  valid subcommands

  {clean}               additional help
    clean               clean help
                
## Tag Parameter
The Tags are in following format:  
{Tagname}:{Tagvalue}  
Multiple tags are delimited with a space  
  
## Interval update  
To update your config with a specific interval, use the cronjobs of your os  
Just use the same command  

## Templates  
For templates are following parameters available:  
{HOST} = instance id  
{IP} or {PublicIP} = instance public ip
{PrivateIP} = instance private ip
  
If you need more just create a feature request  

## noClean clean
sample usage of the --no-clean and clean feature
1. Create config for application:application1 with --no-clean
2. Create another config for application:application2 with --no-clean  
**if on step 2 a clean function would be called, all instances from step 1 would be deleted**
3. call the clean command with another tag like icinga:true

## Contributing
1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D


## License
MIT
</content>
</snippet>
