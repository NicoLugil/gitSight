import gitlab

import gitsight.util_issuedates
import gitsight.burndown_chart

def main():
    print('hi')

    gl = gitlab.Gitlab.from_config('default', ['/home/niclugil/.python-gitlab.cfg'])

    project = gl.projects.get(19719852)

    issues = project.issues.list()
    #print(f'Found {len(issues)} issues')
    #print(issues[0])

    # create burndown chart
    map=gitsight.util_issuedates.get_issues_created_and_closed_dates(issues)
    xy=gitsight.burndown_chart.create_burndown_list(map)
    xy_bucketized=gitsight.burndown_chart.bucketize_dates(xy,'last')
    gitsight.burndown_chart.create_plot(xy_bucketized)
    print(xy_bucketized)
