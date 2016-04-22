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
    AWS for Icinga 2
    
    optional arguments:
      -h, --help            show this help message and exit
      -t TAGS [TAGS ...], --tags TAGS [TAGS ...]
                            Tag Filter: Key value pair
      -th TEMPLATEHOST, --template-host TEMPLATEHOST
                            Which Template should be used for the host
      -tc TEMPLATECHECK, --template-check TEMPLATECHECK
                            Which Template should be used for the checks
                
## Tag Parameter
The Tags are in following format:  
{Tagname}:{Tagvalue}  
Multiple tags are delimited with a space  
  
## Interval update  
To update your config with a specific interval, use the cronjobs of your os  
Just use the same command  

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
