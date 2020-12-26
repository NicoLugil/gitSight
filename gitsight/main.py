import gitlab

import gitsight.commandline_parser
import gitsight.configfile_parser
import gitsight.creators.issues_vs_time
import gitsight.data.data_classes

import sys
import os
import errno
import shutil
import pathlib
import yaml
import pickle

def main():

    # parse commandline
    args=gitsight.commandline_parser.get_commandline_args()
    #print(f'Args:\n{args}')

    # parse main yaml config file
    config=gitsight.configfile_parser.get_config(args.config)
    #print(f'Config:\n{config}')

    if args.loadfile:
        print(f'Loading git project from {args.loadfile}')
        with open(args.loadfile, 'rb') as outfile:
            project = pickle.load(outfile)        
    else:    
        gl = gitlab.Gitlab.from_config(config['gitlab']['config_file_section'], 
            [os.path.abspath(os.path.expanduser(config['gitlab']['config_file']))])
        project = gl.projects.get(config['gitlab']['project_id'])   

    if args.dumpfile:
        print(f'Dumping git project in {args.dumpfile}')
        with open(args.dumpfile, 'wb') as outfile:
            pickle.dump(project, outfile)
        with open(args.dumpfile+'.yaml', 'w') as outfile:
            yaml.dump(project, outfile)  # for debug   

    # get users
    users = project.users.list(all=True)
    gs_users = gitsight.data.data_classes.convert_gitlab_users_to_gs_users(users)
    del users
    print(f'Found {gs_users.get_number_of_users()} users')

    # get issues from the project
    issues = project.issues.list(all=True)
    gs_issues = gitsight.data.data_classes.convert_gitlab_issues_to_gs_issues(issues, gs_users)
    active_users=gitsight.data.data_classes.drop_idle_users(gs_users,gs_issues)
    del gs_users
    del issues
    print(f'Found {gs_issues.get_number_of_issues()} issues')

    # we often will need the issues per user, create this dict, also put the project issues in this dict (key -1)
    # keys will be either:
    #   user id
    #   -1 : for all the project issues
    #   None: issues without assignee
    # This also drops users with no assigned issues
    issues_per_user=gitsight.data.data_classes.get_issues_per_user(active_users, gs_issues)
    del gs_issues

    # put c3.js in place
    # TODO: let users use their version
    dirpath = pathlib.Path('c3')
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)
    shutil.copytree(os.path.join(os.environ['GITSIGHT_HOME'],'c3-0.7.20'), 'c3')

    # put gs.js in place
    shutil.copyfile(os.path.join(os.environ['GITSIGHT_HOME'],'templates/gs.css'), 'gs.css')

    # create pages
    gitsight.creators.issues_vs_time.create_page(active_users,issues_per_user)

    # point index.html to main page
    try:
        os.symlink('dashboard.html','index.html')
    except OSError as e:
        if e.errno == errno.EEXIST:
            pass
        else:
            raise