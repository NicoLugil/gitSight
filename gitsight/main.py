import gitlab

import gitsight.commandline_parser
import gitsight.configfile_parser
import gitsight.util_issuedates
import gitsight.burndown_chart

import sys
import os

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

    # create burndown chart
    map=gitsight.util_issuedates.get_issues_created_and_closed_dates(issues)
    xy=gitsight.burndown_chart.create_burndown_list(map)
    xy_bucketized=gitsight.burndown_chart.bucketize_dates(xy,'last')
    gitsight.burndown_chart.create_plot(xy_bucketized)
