from typing import List, Dict
import googlemaps

from private import APIKEY
from lib.Hospital import Hospital

gmaps = googlemaps.Client(key=APIKEY)

def processAPIResponse(transfer, response, critical_time, hosp_collection)->List:
    '''Gets Response of API Call and yields a list of dictionaries which can be processed further

    params:
    json_resp: JSON response from API call
    critical_time: time that must be within

    yields: 
    A dictionary of distance, time and hospital
    '''
    validHosps = list()
    row = response['rows'][0]['elements']

    for idx, trip in enumerate(row):
        time = trip['duration']['value']
        distance = trip['distance']['value']
        hosp = hosp_collection[idx]

        #If it is the first hospital visited or within critical timeframe
        if (time < critical_time) or (hosp == transfer.hospital):
            validHosps.append({'hospital':hosp, 'time':time, 'distance':distance})
    return validHosps


def hospitalTransfers(transfer, hospital_collection, critical_time):
    '''Get hospital transfers that are givem transfer

    params:
    transfer: An ambulance transfer
    hospital_collection: Collection of hospitals to check against
    critical_time: the threshold period of time in which a transfer would be valid
    '''
    response = gmaps.distance_matrix(origins=(transfer.pickup_lat, transfer.pickup_lon),
                                     destinations=hospital_collection.getAddresses())
    if response['status'] == "OK":
        valid_trips = processAPIResponse(transfer, response, critical_time, hospital_collection)
        if valid_trips != None:
            transfer.feasible_transfers = valid_trips
    elif response['status'] == "INVALID_REQUEST":
        print(f"The request of {transfer.id} was not able to be completed")


def serialize(obj):
    if isinstance(obj, Hospital):
        serial  = obj.__repr__()
        return serial

    return obj.__dict__