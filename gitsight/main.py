import gitlab

import gitsight.commandline_parser
import gitsight.configfile_parser
import gitsight.util_issuedates
import gitsight.open_issues

import sys
import os
import shutil
import pathlib

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
    issues = project.issues.list()
    #print(f'Found {len(issues)} issues')
    #print(issues[0])

    # put c3.js in place
    # TODO: let users use their version
    dirpath = pathlib.Path('c3')
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)
    shutil.copytree(os.path.join(os.environ['GITSIGHT_HOME'],'c3-0.7.20'), 'c3')

    # put gs.js in place
    shutil.copyfile(os.path.join(os.environ['GITSIGHT_HOME'],'templates/gs.css'), 'gs.css')

    # create open issues page
    map=gitsight.util_issuedates.get_issues_created_and_closed_dates(issues)
    xy_open=gitsight.open_issues.create_open_issues_list(map)
    xy_open_bucketized=gitsight.open_issues.bucketize_dates(xy_open,'last')
    xy_opened,xy_closed=gitsight.open_issues.create_opened_and_closed_issues_list(map)
    xy_opened_bucketized=gitsight.open_issues.bucketize_dates(xy_opened,'last')
    xy_closed_bucketized=gitsight.open_issues.bucketize_dates(xy_closed,'last')
    gitsight.open_issues.create_plot(xy_open_bucketized,xy_opened_bucketized,xy_closed_bucketized)
