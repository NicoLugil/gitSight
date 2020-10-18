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
