import os

def create_open_issues_list(iid_dates_map):
    """Will create a list with open issues numbers

    Args:
        iid_dates_map: A dict mapping the issue's iid to a pair of 
        datetime objects. Index 0 is the creation date, index 1 the closed date. 
        If not yet closed, index1 must be None

    Returns:
        a list with an array of size 2:
        index0 is a datetime object
        index1 is a number representing the number of open issues at the date/time
               of index0
        the list will be sorted in 'incrementing time'
    """

    
    my_delta_dict={}   # dict: key: all dates when something changed, value: delta of open issues at that date
    for k,v in iid_dates_map.items():
        if v[0] in my_delta_dict:
            my_delta_dict[v[0]]+=1
        else:
            my_delta_dict[v[0]]=1
        if v[1]:
            if v[1] in my_delta_dict:
                my_delta_dict[v[1]]+=-1
            else:
                my_delta_dict[v[1]]=-1
    # list of sorted dates
    sorted_dates=sorted(my_delta_dict.keys())
    # build abolute number of open issues, corresponding to the dates
    r=[]
    acc=0;
    for d in sorted_dates:
        acc=acc+my_delta_dict[d]
        pair=[d, acc]
        r.append(pair)
    #print(r)
    return r

def create_opened_and_closed_issues_list(iid_dates_map):
    """Will create a list with the number of opened and closed issues

    In contrast to create_open_issues_list, this will return 2 monotonic lists
    Opened will start at 0 and every time an issue is opened it increments, closing does not matter
    Closed will start at 0 and every time an issue is closed it increments

    Args:
        iid_dates_map: A dict mapping the issue's iid to a pair of 
        datetime objects. Index 0 is the creation date, index 1 the closed date. 
        If not yet closed, index1 must be None

    Returns:
        ro:
            a list with an array of size 2:
            - index0 is a datetime object
            - index1 is a number representing the number of opened issues at the date/time
               of index0
        rc:
            a list with an array of size 2:
            - index0 is a datetime object
            - index1 is a number representing the number of closed issues at the date/time
               of index0
        the lists will be sorted in 'incrementing time'
    """
  
    my_delta_dict_opened={}   # dict: key: all dates when something changed, value: delta of opened issues at that date
    my_delta_dict_closed={}   # dict: key: all dates when something changed, value: delta of closed issues at that date
    for k,v in iid_dates_map.items():
        if v[0] in my_delta_dict_opened:
            my_delta_dict_opened[v[0]]+=1
        else:
            my_delta_dict_opened[v[0]]=1
        if v[1]:
            if v[1] in my_delta_dict_closed:
                my_delta_dict_closed[v[1]]+=1
            else:
                my_delta_dict_closed[v[1]]=1
    # list of sorted dates
    sorted_dates_opened=sorted(my_delta_dict_opened.keys())
    sorted_dates_closed=sorted(my_delta_dict_closed.keys())
    # build abolute number of opened issues, corresponding to the dates
    ro=[]
    acc=0
    for d in sorted_dates_opened:
        acc=acc+my_delta_dict_opened[d]
        pair=[d, acc]
        ro.append(pair)
    rc=[]
    acc=0
    for d in sorted_dates_closed:
        acc=acc+my_delta_dict_closed[d]
        pair=[d, acc]
        rc.append(pair)
    #print(r)
    return ro, rc

def bucketize_dates(xy, bucket_mode=None):
    """Allows reducing 'close together dates'

    This function gets a list of xy pairs as from create_open_issues_list
    and allows reducing the set if multiple x values are 'on the same day'.
    In this way the returned list will have at maximum one entry for a particular day
    (unless bucket_mode=None)
    The pairs do not have to be in time order
    Always a new list is created.
    
    Args:
        xy: a list containing arrays of size 2: 
            index0 is a datetime object
            index1 is a number representing the number of open issues at the date/time of index0

        bucket_mode: option to 'collapse' multiple x data points to a single one
            None: do nothing, output = input
            'last': if multiple from the same day: keep the one with the latest time.

    Returns:
        a new version of xy with reduced number of 'x'-es, based on the bucket_mode
    """

    assert bucket_mode in (None,'last'), f'Invalid bucket_mode {bucket_mode}'
    # print('\n')
    # for idx,pair in enumerate(xy):
    #     print(f'{idx}: {pair[0].strftime("%m/%d/%Y, %H:%M:%S")}')
    # print('\n')
    new_list=[]
    handled_days=[]
    if not bucket_mode:
        new_list=xy.copy()
    else:
        # we will do a reduction
        if bucket_mode=='last':
            # this is probably not pythonic :-)
            # and probably not very fast
            for idx,pair in enumerate(xy):
                # print(f'handled days are {handled_days}')
                if pair[0].date() in handled_days:
                    # we must already have handled all items in the list on this day
                    pass
                    # print(f'already handled {pair[0].strftime("%m/%d/%Y, %H:%M:%S")}')
                else:
                    # a new date
                    # print(f'not yet handled {pair[0].strftime("%m/%d/%Y, %H:%M:%S")}')
                    keep=pair
                    # print(f'   keeping {keep[0].strftime("%m/%d/%Y, %H:%M:%S")}')
                    handled_days.append(keep[0].date())
                    # search the one we want to keep
                    for pair2 in xy[idx : None]:
                        if keep[0].date()==pair2[0].date():
                            if keep[0].time()<pair2[0].time():
                                keep=pair2
                                # print(f'   keeping {keep[0].strftime("%m/%d/%Y, %H:%M:%S")}')
                    new_list.append(keep)
    # print('\n')
    # for idx,pair in enumerate(new_list):
    #     print(f'{idx}: {pair[0].strftime("%m/%d/%Y, %H:%M:%S")}')
    # print('\n')
    return new_list

def create_plot(xy,xy_opened,xy_closed):
    """ will create html with open issues chart

    Args:
        xy: a list containing arrays of size 2: 
            index0 is a datetime object
            index1 is a number representing the number of open issues at the date/time of index0

    Returns:
        nothing yet - will just dump html as output
    """

    print(xy)
    print('------------')
    print(xy_opened)


    ##################
    ###### html ######
    ##################
    with open(os.path.join(os.environ['GITSIGHT_HOME'],'templates/main.html'), 'r') as f:
        s_html=f.read()

    content=f"""    
    <div class="w3-row w3-padding-64">
        <div class="w3-container">
          <h1 class="w3-text-black">Number of open issues</h1>
          <p> Project</p>
          <div id="chart0" class="w3-margin"></div>
        </div>
        <div class="w3-container">
          <p> Top 10 members</p>
          
        </div>
    </div>
"""
    s_html=s_html.replace('--gs_replace_me--',content)

    with open('open_issues.html', 'w') as f:
        f.write(s_html)

    ##################
    ######  js  ######
    ##################
    with open(os.path.join(os.environ['GITSIGHT_HOME'],'templates/multi_xy_line_chart.js'), 'r') as f:
        s_js=f.read()

    xs='\'remaining\': \'x\',\n'
    xs+='            \'opened\': \'xo\',\n'
    xs+='            \'closed\': \'xc\''
    s_js=s_js.replace('--gs_replace_me_xs--',xs)


    x='[\'x\',\n             '
    y='            [\'remaining\',\n              '
    for idx, pair in enumerate(xy):
        nl=f''
        if idx+1 != len(xy):
            nl +=','
        if ((idx+1) % 10 == 0):
            nl += ' \\\n            '
        x+=(pair[0].date().strftime('\'%Y-%m-%d\'')+nl)
        y+=(str(pair[1])+nl)
    x+='],\n'
    y+='],\n'
    #
    xo='            [\'xo\',\n             '
    yo='            [\'opened\',\n              '
    for idx, pair in enumerate(xy_opened):
        nl=f''
        if idx+1 != len(xy_opened):
            nl +=','
        if ((idx+1) % 10 == 0):
            nl += ' \\\n            '
        xo+=(pair[0].date().strftime('\'%Y-%m-%d\'')+nl)
        yo+=(str(pair[1])+nl)
    xo+='],\n'
    yo+='],\n'
    #
    xc='            [\'xc\',\n             '
    yc='            [\'closed\',\n              '
    for idx, pair in enumerate(xy_closed):
        nl=f''
        if idx+1 != len(xy_closed):
            nl +=','
        if ((idx+1) % 10 == 0):
            nl += ' \\\n            '
        xc+=(pair[0].date().strftime('\'%Y-%m-%d\'')+nl)
        yc+=(str(pair[1])+nl)
    xc+='],\n'
    yc+=']'
    #
    s_js=s_js.replace('--gs_replace_me_columns--',x+xo+xc+y+yo+yc)

    x_axis="""
            type: 'timeseries',
            tick: {format: '%Y-%m-%d', count: 10}
"""
    s_js=s_js.replace('--gs_replace_me_x_axis--',x_axis)

    chart='chart0'
    s_js=s_js.replace('--gs_replace_me_bindto--',chart)

    with open('gs_open_issues.js', 'w') as f:
        f.write(s_js)

