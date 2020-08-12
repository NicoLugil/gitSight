import dateutil.parser
import datetime

def from_gitlab_api_date_to_local_datetime_format(date):
    """ Transforms the API returned date string to a datetime object

    The API returns dates of as '2020-08-12T08:46:52.794Z'
    This function will transform it to a datetime object
    and convert it to the local timezone

    Args:
        date: string in the ISO 8061 format ('2020-08-12T08:46:52.794Z')

    Returns:
        datetime object by converting the provided date, including
        changing to the local timezone
    """

    t=dateutil.parser.isoparse(date)
    t_local=t.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)
    #print(t_local)
    return t_local

def get_issues_created_and_closed_dates(issues):
    """Returns the created and closed dates for a list of issues

    Given a list of issues, a dict will be created with as key the 
    iid, and as value an array of size 2: created and closed date
    if not yet closed, the closed date will be None

    Args:
        issues: a list of issues returned by the gitlab API

    Returns:
        A dict mapping the issue's iid to a pair of datetime objects.
        Index 0 is the creation date, index 1 the closed date. If not yet 
        closed, None will be returned.
        The dates will be in the local timezone
    """

    m={}
    for i in issues:
        creation_date=from_gitlab_api_date_to_local_datetime_format(i.created_at)
        closed_date=None if i.closed_at==None else from_gitlab_api_date_to_local_datetime_format(i.closed_at)
        m[i.iid]=[creation_date,closed_date]
    return m    
