from .. import utils

########################################### classes ###########################################

class gs_issue:
    """ 
    A more accessible format of a subset of the issue info that gitlab returns
    """

    def __init__(self,git_issue):
        """ constructor

        Args:
            git_issue: a single issue how it comes out of gitlab

        Constructor will set its fields based on this

        iid: issue iid
        creation_date: date issue was created, type datetime in local time
        closed_date: date issue was closed, type datetime in local time, or None if not yet closed
        """

        self.iid=git_issue.iid
        self.creation_date=utils.from_gitlab_api_date_to_local_datetime_format(git_issue.created_at)
        self.closed_date=None if git_issue.closed_at==None else utils.from_gitlab_api_date_to_local_datetime_format(git_issue.closed_at)


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

########################################### methods ###########################################

def convert_gitlab_issues_to_gs_issues(gitlab_issues):
    """ Converts an array of issues as returned by gitlab to an array of gs_issues

    Args:
        gitlab_issues: array of issues as returned by gitlab

    Returns:
        an array of gs_issues

    """

    gs_issues=[]
    for gitlab_issue in gitlab_issues:
        issue = gs_issue(gitlab_issue)
        gs_issues.append(issue)
    return gs_issues