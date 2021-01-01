import os
import yaml
from mako.template import Template
from .. data import graphic_data_classes
from .. data import data_classes
from . import issues_vs_time

def create_page(users,issues_per_user,config):
    """ Creates html page for dashboard

    Args:
        issues_per_user: dict as returned by get_issues_per_user:
            key can be: None, -1 or user id
            value: gs_issues object with the issues for the user identified by the key
            config: config for this page
            

    Created files:
        gs_dashboard.js
        dashboard.html

    """

    print('dashboard...', end='')
    m_page = graphic_data_classes.gs_page(title='Dashboard',n_columns=config['columns'])
    m_page.add_plot(issues_vs_time.plot_one_user(issues_per_user[-1],'Project'),col=0)
    m_page.add_js('gs_time.js')

    create(m_page)
    print('done')

def create(page):
    """ will create html with dashboard

    Args:
        page: gs_page object

    Returns:
        nothing yet - will just dump html as output
    """

    ##################
    ###### html ######
    ##################

    mytemplate = Template(filename=os.path.join(os.environ['GITSIGHT_HOME'],'templates/main.html'))
    s_html=mytemplate.render(page=page)
    with open('dashboard.html', 'w') as f:                
        f.write(s_html)

    ##################
    ######  js  ######
    ##################

    # mytemplate = Template(filename=os.path.join(os.environ['GITSIGHT_HOME'],'templates/multi_xy_line_chart.js'))
    # #s_js=mytemplate.render(lines=lines, columns=x+xo+xc+y+yo+yc, x_axis=x_axis, chart=chart)
    # #print(yaml.dump(page))
    # s_js=mytemplate.render(plots=page.plots)
    # with open('gs_dashboard_time.js', 'w') as f:
    #     f.write(s_js)

