## standard library imports
import requests
import logging as log
import datetime

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


def get_transit_time(from_address):
    """
    ------
    params
        from_address <string> : "43.6683396,-79.3856119"
    """
    transit_time = None
    try:
        log.info('Getting transit time from %s' % from_address)
        t = datetime.datetime.today()
        tomorrow = t.replace(hour=settings.HOUR_DEPART+5, minute=settings.MINUTE_DEPART,
            second=0, microsecond=0) + datetime.timedelta(days=1)
        epoch = (tomorrow - datetime.datetime(1970,1,1)).total_seconds()
        epoch_str = str(epoch).replace('.0', '')

        url = ("https://maps.googleapis.com/maps/api/directions/json?origin="
            "{0}&destination={1}&departure_time={2}&mode={3}"
            "&key={4}").format(from_address, settings.WORK_ADDRESS, epoch_str,
                settings.TRAVEL_MODE, settings.GOOGLE_DIRECTIONS_TOKEN)
        r = requests.get(url)

        if r.status_code == 200:
            d = r.json()
            if d['routes']:
                duration = d['routes'][0]['legs'][0]['duration']
                transit_time = duration['value']/60
            else:
                log.warning('No route could be found for address %s' % from_address)
        return transit_time

    except Exception as err:
        log.exception("Error getting transit time for %s Error: %s" %
            (from_address, str(err)))
        return transit_time
