import os
import yaml
from mako.template import Template
from .. data import graphic_data_classes
from .. data import data_classes
from . import issues_vs_time
from . import people

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
    plot_cnt=0
    m_page.add_plot(issues_vs_time.plot_one_user(f'LINE_chart_{plot_cnt}',issues_per_user[-1],'Issues over time'),col=plot_cnt%config['columns'])
    plot_cnt += 1
    m_page.add_plot(people.plot_n_issues_per_user_pie(f'PIE_chart_{plot_cnt}', users, issues_per_user),col=plot_cnt%config['columns'])
    m_page.add_js('gs_dashboard_line.js')
    m_page.add_js('gs_dashboard_pie.js')

    create(m_page)
    print('done')

def create(page):
    """ will create html and js with dashboard

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

    mytemplate = Template(filename=os.path.join(os.environ['GITSIGHT_HOME'],'templates/multi_xy_line_chart.js'))
    s_js=mytemplate.render(plots=page.gs_plots.get_plots_of_type(graphic_data_classes.gs_plot_type.LINE).plots)
    with open('gs_dashboard_line.js', 'w') as f:
        f.write(s_js)

    mytemplate = Template(filename=os.path.join(os.environ['GITSIGHT_HOME'],'templates/pie_chart.js'))
    s_js=mytemplate.render(plots=page.gs_plots.get_plots_of_type(graphic_data_classes.gs_plot_type.PIE).plots)
    with open('gs_dashboard_pie.js', 'w') as f:
        f.write(s_js)