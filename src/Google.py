## standard library imports
import requests
import logging as log
import datetime
from pprint import pprint

## local library imports
import src.settings as settings

def get_coords(address):
    req_url = 'https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'
    address = address + ' Toronto, Ontario, Canada'

    try:
        response = requests.get(req_url.format(address,
            settings.GOOGLE_LOCATION_TOKEN))
        response_dict = response.json()
        coords=response_dict['results'][0]['geometry']['location']
        if response_dict['status'] == 'OK':
            return coords['lat'],coords['lng']
    except Exception as err:
        log.exception('error retrieving address %s. Error %s' % (address, str(err)))
    return None, None


def get_travel_time(from_address):
    """
    ------
    params
        from_address <string> : "43.6683396,-79.3856119"
    """
    commute_time = None
    try:
        log.info('Getting transit time from %s' % from_address)
        t = datetime.datetime.today()
        tomorrow = t.replace(hour=settings.HOUR_DEPART+5, minute=settings.MINUTE_DEPART,
            second=0, microsecond=0) + datetime.timedelta(days=1)
        epoch = (tomorrow - datetime.datetime(1970,1,1)).total_seconds()
        epoch_str = str(epoch).replace('.0', '')

        if settings.TRAVEL_MODE == 'transit':
            url = ("https://maps.googleapis.com/maps/api/directions/json?origin="
                "{0}&destination={1}&departure_time={2}&mode={3}&transit_mode={4}"
                "&key={5}").format(from_address, settings.WORK_ADDRESS, epoch_str,
                    settings.TRAVEL_MODE, settings.TRANSIT_MODE,
                    settings.GOOGLE_DIRECTIONS_TOKEN)
        else:
            url = ("https://maps.googleapis.com/maps/api/directions/json?origin="
                "{0}&destination={1}&departure_time={2}&mode={3}"
                "&key={4}").format(from_address, settings.WORK_ADDRESS, epoch_str,
                    settings.TRAVEL_MODE, settings.GOOGLE_DIRECTIONS_TOKEN)
        r = requests.get(url)

        if r.status_code == 200:
            d = r.json()
            if d['routes']:
                duration = d['routes'][0]['legs'][0]['duration']
                commute_time = round(duration['value']/60,1)
            else:
                log.warning('No route could be found for address %s' % from_address)
        return commute_time

    except Exception as err:
        log.exception("Error getting transit time for %s Error: %s" %
            (from_address, str(err)))
        return commute_time
