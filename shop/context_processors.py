from jdatetime import datetime


def today(request):
    return {'today': datetime.now().date()}
