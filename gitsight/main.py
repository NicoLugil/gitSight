import gitlab

import gitsight.commandline_parser
import gitsight.configfile_parser
import gitsight.creators.issues_vs_time
import gitsight.data.data_classes

import sys
import os
import shutil
import pathlib
import yaml

def main():

    # parse commandline
    args=gitsight.commandline_parser.get_commandline_args()
    #print(f'Args:\n{args}')

    # parse main yaml config file
    config=gitsight.configfile_parser.get_config(args.config)
    #print(f'Config:\n{config}')

    # get issues from the project
    gl = gitlab.Gitlab.from_config(config['gitlab']['config_file_section'], 
        [os.path.abspath(os.path.expanduser(config['gitlab']['config_file']))])
    project = gl.projects.get(config['gitlab']['project_id'])   
    issues = project.issues.list(all=True)
    gs_issues = gitsight.data.data_classes.convert_gitlab_issues_to_gs_issues(issues)
    del issues
    #print(yaml.dump(gs_issues))
    print(f'Found {len(gs_issues)} issues')

    # put c3.js in place
    # TODO: let users use their version
    dirpath = pathlib.Path('c3')
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)
    shutil.copytree(os.path.join(os.environ['GITSIGHT_HOME'],'c3-0.7.20'), 'c3')

    # put gs.js in place
    shutil.copyfile(os.path.join(os.environ['GITSIGHT_HOME'],'templates/gs.css'), 'gs.css')

    # create pages
    gitsight.creators.issues_vs_time.create_page(gs_issues)