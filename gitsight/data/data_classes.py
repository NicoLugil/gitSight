from .. import utils

########################################### classes ###########################################

class gs_issue:
    """ 
    A more accessible format of a subset of the issue info that gitlab returns
    """

    def __init__(self,git_issue,users):
        """ constructor

        Args:
            git_issue: a single issue how it comes out of gitlab
            users: collection of users (gs_users object)

        Constructor will set its fields based on this

        iid: issue iid
        creation_date: date issue was created, type datetime in local time
        closed_date: date issue was closed, type datetime in local time, or None if not yet closed
        assignee: a gs_user object, or None if the issue has no assignee
        """

        self.iid=git_issue.iid
        self.creation_date=utils.from_gitlab_api_date_to_local_datetime_format(git_issue.created_at)
        self.closed_date=None if git_issue.closed_at==None else utils.from_gitlab_api_date_to_local_datetime_format(git_issue.closed_at)
        self.assignee=None if git_issue.assignee==None else users.get_user_by_id(git_issue.assignee['id'])


class gs_issues:
    """
    Collection of issues (gs_issue)
    """

    def __init__(self):
        self.issues=[]

    def add_issue(self,issue):
        self.issues.append(issue)

    def get_number_of_issues(self):
        return len(self.issues)

    def filter(filter):
        """ 
        returns a new gs_issues object, with only the issues passing the filter

        Args:
            filter: gs_filter object

        """
        filtered_issues = gs_issues()
        for i in self.issues():
            if filter.filter(i) is not None:
                filtered_issues.append(i)
            else:
                print('filtered')


class gs_user:
    """
    Our small database of a single user's info
    """

    def __init__(self,git_user):
        """ constructor

        Args:
            git_user: a single user how it comes out of gitlab
        """

        self.id=git_user.id
        self.name=git_user.name
        self.username=git_user.username

class gs_users:
    """
    Collection of all users
    """

    def __init__(self):
        self.users=[]
        self.user_dict={}   # key = user id, value - user

    def add_user(self,user):
        """ add a user 

        Args:
            user: gs_user object
        """
        self.users.append(user)
        self.user_dict[user.id]=user

    def get_user_by_id(self,u_id):
        """ return user matching the given id"""
        return self.user_dict[u_id]

    def get_number_of_users(self):
        return len(self.users)


class xy:
    """ 
    A class that bundles x, y and label
    """

    def __init__(self, label='no-label', x=None, y=None):
        self.label=label
        self.x = x if x is not None else []
        self.y = y if y is not None else []

    def append(self,x,y):
        """ appends x and y to the internal array """
        self.x.append(x)
        self.y.append(y)

    def get_as_pair(self):
        """ returns x and y as a single array of 2-deep arrays holding x and y"""

        pair=[]
        for idx,x in enumerate(self.x):
            e=[x,self.y[idx]]
            pair.append(e)
        return pair
    
    def print(self):
        print(f"xy object labelled {self.label}:")
        for idx, x in enumerate(self.x):
            print(f"{idx}   {x} {self.y[idx]}") 

class gs_filter:
    """
    A class to represent a filter which can be used to filter gs_issues

    Each member of the class is used as filter member. Issues matching all the filter mebers are kept.
    To not filter by a member: member should be '*'

    """

    def __init__(self, assignee_id='*'):
        """ constructor, allows setting filter

        Args:
            assignee_id: assignee to filter by. '*' passes all. Must be a user id or None (for issues that have no assigneee)

        """

        self.assignee_id=assignee_id

    def filter(gs_issue):
        """ Apllies the filter to a signel issue

        Args:
            gs_issue: gs_issue object that is being checked if it passes the filter

        Returns:
            if it passes the filter: the given gs_issue, if not: None

        """
        if self.assignee == '*':
            return gs_issue
        if self.assignee_id == None:
            # we want to keep issues without assignee
            if gs_issue.assignee == None:
                return gs_issue
        if gs_issue.assignee == None:
            # issue has no assignee
            # if filter was also None, the above would already have returned -> return None
            return None
        if self.assignee_id == gs_issue.assignee.id:
            return gs_issue
        return None


########################################### methods ###########################################

def convert_gitlab_issues_to_gs_issues(gitlab_issues, users):
    """ Converts an array of issues as returned by gitlab to a gs_issues object

    Args:
        gitlab_issues: array of issues as returned by gitlab
        users: collection of users (gs_users object)

    Returns:
        gs_issues object

    """
    issues = gs_issues()
    for gitlab_issue in gitlab_issues:
        issue = gs_issue(gitlab_issue, users)
        issues.add_issue(issue)
    return issues

def convert_gitlab_users_to_gs_users(gitlab_users):
    """ Converts an array of users as returned by gitlab to a gs_users object

    Args:
        gitlab_users: array of users as returned by gitlab

    Returns:
        gs_users object

    """

    users = gs_users()
    for gitlab_user in gitlab_users:
        user = gs_user(gitlab_user)
        users.add_user(user)
    return users 

def get_number_of_open_issues_per_user(users, issues):
    """ return for each of the users how many open issues he has """