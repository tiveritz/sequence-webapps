from datetime import datetime


API_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
APP_TIME_FORMAT = '%d.%m.%Y %H:%M'
    
def convert_datetime_api_to_app(api_time):
    dt = datetime.strptime(api_time[0:18], API_TIME_FORMAT)
    return dt.strftime(APP_TIME_FORMAT)
