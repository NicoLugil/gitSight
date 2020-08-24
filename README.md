The initial goal of this project is to be able to visualize git issue statistiscs for gitlab projects.

It uses [python-gitlab](https://github.com/python-gitlab/python-gitlab) to retreive data from your gitlab project, and [c3js](https://c3js.org/) for plotting.

We are only getting started, there is much more to come...

# installation

For now the code isn't nicely packaged yet. Install by 
- downloading the repo
- making sure you have the packages in requirements.txt, these are the versions that have been tested. Since we use very basic functionality, earlier versions are very likely to work as well
- set the correct PYTHONPATH (to the main repo path, for example `export PYTHONPATH=<your_specific_path>/gitSight`)

# configuration

## command line

```
usage: gitsight [-h] [-c CONFIG]

Create different kind of charts from a gitlab project

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        gitsight yaml config file to use (default:
                        gitsight.yaml)

```

## main YAML configuration file 

This is the file passed via the -c/--config command line option. It is the main configuration file for the tool and is written in [YAML](https://yaml.org/) syntax. This is explained by the example below.

```
---
# settings related to python-gitlab
gitlab:
  config_file: ~/.python-gitlab.cfg
  config_file_section: gitlab public
  project_id: 19719852
...
```

The gitlab section relates to python-gitlab, see also the following section 'python-gitlab configuration file'.
- gitlab.config_file: the path to the python-gitlab config file
- config_file_section: the section in that config file to use
- project_id: the project ID of the project you want to let this tool run on. You can find this in gitlab's web interface -> Project overview

## python-gitlab configuration file

Because we 





