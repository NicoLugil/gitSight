import os
import yaml
from mako.template import Template
from .. data import graphic_data_classes
from .. data import data_classes

def create_page(users,issues_per_user,config):
    """ Creates html page for people

    Args:
        users: gs_users object 
        issues_per_user: dict as returned by get_issues_per_user:
            key can be: None, -1 or user id
            value: gs_issues object with the issues for the user identified by the key
            config: config for this page

    Created files:
        gs_people.js
        people.html

    """

    print('people...', end='')
    m_page = graphic_data_classes.gs_page(title='People statistics',n_columns=config['columns'])
    plot_cnt=0;
    m_page.add_plot(plot_n_issues_per_user_pie(f'PIE_chart_{plot_cnt}', users, issues_per_user),col=plot_cnt%config['columns'])
    plot_cnt += 1
    m_page.add_js('gs_people.js')

    create(m_page)
    print('done')

def plot_n_issues_per_user_pie(name, users, issues_per_user):
    """ returns a single plot (gs_pie_plot) with as parts each user's number of open issues

    Args:
        users: gs_users object 
        issues_per_user: dict as returned by get_issues_per_user:
            key can be: None, -1 or user id
            value: gs_issues object with the issues for the user identified by the key

    Returns:
        gs_pie_plot object
    """

    # array containing 2 element arrays: [username, number of open issues]
    parts=[]
    for user_id, issues_of_user in issues_per_user.items():
        open_issues=data_classes.filter_open_issues(issues_of_user)
        #print(user_id)
        if open_issues.get_number_of_issues()==0:
            continue
        if user_id==-1:
            continue
        if user_id==None:
            parts.append(['Unassigned',open_issues.get_number_of_issues()])
            #print(['Unassigned',open_issues.get_number_of_issues()])
            continue
        parts.append([users.get_user_by_id(user_id).name,open_issues.get_number_of_issues()])
        #print([users.get_user_by_id(user_id).name,open_issues.get_number_of_issues()])
    # sorted
    parts=sorted(parts,key=lambda part: part[1], reverse=True)
    #print(parts)

    # collapse everything under 1% of total into other
    total=0.0;
    other=0;
    index_to_start_deletion=-1
    for part in parts:
        total += part[1]
    #print(f"total={total}")
    #print(f'total={total}')
    for idx, part in enumerate(parts):
        #print(f'{idx}: {part[0]} {part[1]/total}')
        if part[1]/total < 0.01:
            other += part[1]
            if index_to_start_deletion==-1:
                index_to_start_deletion=idx
    #print(f'starting deletion at {parts[index_to_start_deletion]}')
    if index_to_start_deletion != -1:
        parts[index_to_start_deletion:]=[]
    if other>0:
        parts.append(['Others',other])
    #print(parts)

    # plot
    plot = graphic_data_classes.gs_pie_plot(name,title='Open issues per user')
    for part in parts:
       plot.add_part(part[0],part[1])

    return plot

def create(page):
    """ will create html and js

    Args:
        page: gs_page object

    Returns:
        nothing yet - will just dump html and js as output
    """

    ##################
    ###### html ######
    ##################

    mytemplate = Template(filename=os.path.join(os.environ['GITSIGHT_HOME'],'templates/main.html'))
    s_html=mytemplate.render(page=page)
    with open('people.html', 'w') as f:                
        f.write(s_html)

    ##################
    ######  js  ######
    ##################

    mytemplate = Template(filename=os.path.join(os.environ['GITSIGHT_HOME'],'templates/pie_chart.js'))
    s_js=mytemplate.render(plots=page.gs_plots.get_plots_of_type(graphic_data_classes.gs_plot_type.PIE).plots)
    with open('gs_people.js', 'w') as f:
        f.write(s_js)

