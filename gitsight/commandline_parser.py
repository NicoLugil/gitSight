import argparse

def get_commandline_args():
    parser = argparse.ArgumentParser(description='Create different kind of charts from a gitlab project', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c','--config', dest='config', action='store', default='gitsight.yaml', help='gitsight yaml config file to use')
    args = parser.parse_args()
    return args