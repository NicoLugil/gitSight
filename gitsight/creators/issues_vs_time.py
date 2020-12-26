import os
import yaml
from mako.template import Template
from .. data import graphic_data_classes
from .. data import data_classes

def create_page(users,issues_per_user):
    """ Creates html page for issues vs time

    Args:
        issues_per_user: dict as returned by get_issues_per_user:
            key can be: None, -1 or user id
            value: gs_issues object with the issues for the user identified by the key

    Created files:
        gs_issues_vs_time.js
        issues_vs_time.html

    """

    m_page = graphic_data_classes.gs_page(title='Evolution of issues in time')
    m_page.add_plot(plot_one_user(issues_per_user[-1],'Project'))
    m_page.add_plot(plot_one_user(issues_per_user[None],'Unassigned'))

    # the other ones: sort from most to least open issues
    sorted_ipu = dict(sorted(issues_per_user.items(), key=lambda item: item[1].get_number_of_issues(), reverse=True))
    for user_id,user_issues in sorted_ipu.items():

        if user_id==None or user_id==-1:
            continue
        m_page.add_plot(plot_one_user(user_issues,users.get_user_by_id(user_id).name))
    create(m_page)

def plot_one_user(issues,title):
    """ returns a single plot (gs_plot) for the given issues. 

    Args:
        issues for this user (gs_issues)
        title: title to use


    Returns:
        gs_plot object
    """

    plot = graphic_data_classes.gs_plot(x_type='timeseries',x_count=10,title=title,default_type='line')

    xy_remaining=bucketize_dates(create_open_issues_vs_time_list(issues.issues),'last')
    plot.add_xy_line(xy_remaining,type_override='area')

    xy_opened,xy_closed=create_opened_and_closed_issues_list(issues.issues)
    xy_opened_bucketized=bucketize_dates(xy_opened,'last')
    plot.add_xy_line(xy_opened_bucketized)
    xy_closed_bucketized=bucketize_dates(xy_closed,'last')
    plot.add_xy_line(xy_closed_bucketized)

    return plot

def create_open_issues_vs_time_list(issues):
    """Will create an xy object list with #open issues vs time

    Args:
        issues: object of type gs_issues

    Returns:
        xy object with x=date/time, y=#open issues at that date/time
        the xy entries will be sorted in 'incrementing time'
    """
    
    my_delta_dict={}   # dict: key: all dates when something changed, value: delta of open issues at that date
    for i in issues:
        if i.creation_date in my_delta_dict:
            my_delta_dict[i.creation_date]+=1
        else:
            my_delta_dict[i.creation_date]=1
        if i.closed_date:
            if i.closed_date in my_delta_dict:
                my_delta_dict[i.closed_date]+=-1
            else:
                my_delta_dict[i.closed_date]=-1
    # list of sorted dates
    sorted_dates=sorted(my_delta_dict.keys())
    # build abolute number of open issues, corresponding to the dates
    m_xy = data_classes.xy(label='remaining')
    acc=0;
    for d in sorted_dates:
        acc=acc+my_delta_dict[d]
        m_xy.append(d,acc)
    return m_xy

def create_opened_and_closed_issues_list(issues):
    """Will create 2 xy objects: with the number of opened and closed issues

    In contrast to create_open_issues_vs_time_list, this will return 2 monotonic lists
    Opened will start at 0 and every time an issue is opened it increments, closing does not matter
    Closed will start at 0 and every time an issue is closed it increments

    Args:
        issues: object of type gs_issues

    Returns:
        xy_opened: xy object with x=date/time, y=# ever opened issues at that date/time
        xy_closed: xy object with x=date/time, y=# ever closed issues at that date/time
        the lists will be sorted in 'incrementing time'
    """
  
    my_delta_dict_opened={}   # dict: key: all dates when something changed, value: delta of opened issues at that date
    my_delta_dict_closed={}   # dict: key: all dates when something changed, value: delta of closed issues at that date
    for i in issues:
        if i.creation_date in my_delta_dict_opened:
            my_delta_dict_opened[i.creation_date]+=1
        else:
            my_delta_dict_opened[i.creation_date]=1
        if i.closed_date:
            if i.closed_date in my_delta_dict_closed:
                my_delta_dict_closed[i.closed_date]+=1
            else:
                my_delta_dict_closed[i.closed_date]=1
    # list of sorted dates
    sorted_dates_opened=sorted(my_delta_dict_opened.keys())
    sorted_dates_closed=sorted(my_delta_dict_closed.keys())
    # build abolute number of opened issues, corresponding to the dates
    xy_opened = data_classes.xy(label='opened')
    xy_closed = data_classes.xy(label='closed')
    acc=0
    for d in sorted_dates_opened:
        acc=acc+my_delta_dict_opened[d]
        xy_opened.append(d, acc)
    acc=0
    for d in sorted_dates_closed:
        acc=acc+my_delta_dict_closed[d]
        xy_closed.append(d, acc)
    #print(r)
    return xy_opened, xy_closed

def bucketize_dates(xy, bucket_mode=None):
    """Allows reducing 'close together dates'

    This function gets an xy object as from create_open_issues_vs_time_list
    or create_opened_and_closed_issues_list
    and allows reducing the set if multiple x values are 'on the same day'.
    In this way the returned list will have at maximum one entry for a particular day
    (unless bucket_mode=None)
    The pairs do not have to be in time order
    The given xy object will be altered and returned
    
    Args:
        xy: xy object
            x is a datetime object
            y is a number representing the number of open issues at the date/time of y

        bucket_mode: option to 'collapse' multiple x data points to a single one
            None: do nothing, output = input
            'last': if multiple from the same day: keep the one with the latest time.

    Returns:
        a new version of xy with reduced number of 'x'-es, based on the bucket_mode
    """

    assert bucket_mode in (None,'last'), f'Invalid bucket_mode {bucket_mode}'

    #xy.print()

    new_list_x=[]
    new_list_y=[]
    handled_days=[]
    if not bucket_mode:
        pass
    else:
        # we will do a reduction
        if bucket_mode=='last':
            # this is probably not pythonic :-)
            # and probably not very fast - probably best to first sort
            xy_pairs=xy.get_as_pair()
            for idx,xy_pair in enumerate(xy_pairs):
                # print(f'handled days are {handled_days}')
                if xy_pair[0].date() in handled_days:
                    # we must already have handled all items in the list on this day
                    pass
                    # print(f'already handled {pair[0].strftime("%m/%d/%Y, %H:%M:%S")}')
                else:
                    # a new date
                    # print(f'not yet handled {pair[0].strftime("%m/%d/%Y, %H:%M:%S")}')
                    keep=xy_pair
                    # print(f'   keeping {keep[0].strftime("%m/%d/%Y, %H:%M:%S")}')
                    handled_days.append(keep[0].date())
                    # search the one we want to keep
                    for pair2 in xy_pairs[idx : None]:
                        if keep[0].date()==pair2[0].date():
                            if keep[0].time()<pair2[0].time():
                                keep=pair2
                                # print(f'   keeping {keep[0].strftime("%m/%d/%Y, %H:%M:%S")}')
                    new_list_x.append(keep[0])
                    new_list_y.append(keep[1])
            xy.x=new_list_x
            xy.y=new_list_y
    # print('\n')
    # for idx,pair in enumerate(new_list):
    #     print(f'{idx}: {pair[0].strftime("%m/%d/%Y, %H:%M:%S")}')
    # print('\n')

    #xy.print()
    return xy

def create(page):
    """ will create html with issues vs time plots

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
    with open('dashboard.html', 'w') as f:                 # for now this is our only page --> call it dashboard.html
        f.write(s_html)

    ##################
    ######  js  ######
    ##################

    mytemplate = Template(filename=os.path.join(os.environ['GITSIGHT_HOME'],'templates/multi_xy_line_chart.js'))
    #s_js=mytemplate.render(lines=lines, columns=x+xo+xc+y+yo+yc, x_axis=x_axis, chart=chart)
    #print(yaml.dump(page))
    s_js=mytemplate.render(plots=page.plots)
    with open('gs_issues_vs_time.js', 'w') as f:
        f.write(s_js)

