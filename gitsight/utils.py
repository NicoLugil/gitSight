import dateutil.parser
import datetime
import pickle
import yaml

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

def dump_project_to_yaml(project, issues_per_user, active_users, filename):
    """ Serialize what we loaded (and transformed a little) from the git server to yaml file

    Args:
        project: output from gl.projects.get
        issues_per_user: output from gitsight.data.data_classes.get_issues_per_user
        filename: file to dump project in - 
    """

    d = {}
    d['project']=project
    d['active_users']=active_users
    d['issues_per_user']=issues_per_user

    print(f'Dumping git project in {filename}')
    with open(filename, 'w') as m_file:
        yaml.dump(d, m_file)


def dump_project_to_file(project, issues_per_user, active_users, filename):
    """ Serialize what we loaded (and transformed a little) from the git server - load with load_project_from_file

    Args:
        project: output from gl.projects.get
        issues_per_user: output from gitsight.data.data_classes.get_issues_per_user
        filename: file to dump project in 
    """

    d = {}
    d['project']=project
    d['active_users']=active_users
    d['issues_per_user']=issues_per_user

    print(f'Dumping git project in {filename}')
    with open(filename, 'wb') as m_file:
        pickle.dump(d, m_file)

def load_project_from_file(filename):
    """ Deserialize project, issues_per_user, users from a file (created by dump_project_to_file)

    Args:
        filename: file to load project from

    Returns:
        project, issues_per_user: see dump_project_to_file
    """

    print(f'Loading git project from {filename}')
    with open(filename, 'rb') as m_file:
        d= pickle.load(m_file)    

    project=d['project']
    active_users=d['active_users']
    issues_per_user=d['issues_per_user']

    return project, issues_per_user, active_users