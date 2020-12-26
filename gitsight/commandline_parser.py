import argparse

def get_commandline_args():
    parser = argparse.ArgumentParser(description='Create different kind of charts from a gitlab project', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c','--config', dest='config', action='store', default='gitsight.yaml', help='gitsight yaml config file to use')
    parser.add_argument('--loadfile', dest='loadfile', action='store', help='load project from this file instead of querying a git server, create file with --dumpfile')
    parser.add_argument('--dumpfile', dest='dumpfile', action='store', help='dump project to this file after querying the git server')
    args = parser.parse_args()
    return args