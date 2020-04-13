from typing import List, Optional, Set, Dict
import csv

from lib.Hospital import HospitalCollection
from lib.utils import hospitalTransfers


class Transfer():
    '''A class containing the information pertaining to an ambulance transfer

    params:
    id: unique transfer ID
    pickup_lat: 
    pickup_lon:
    first_hosp_address:
    '''
    def __init__(self, ppn: int, lat: float, lon: float, hospital):
        self.id = ppn
        self.pickup_lat = lat
        self.pickup_lon = lon
        self.hospital = hospital
        
        self.feasible_transfers = list()

    def __len__():
        return len(self.feasible_transfers)
        
    def __str__(self):
        return f"Transfer {self.id} of ({self.pickup_lat}, {self.pickup_lon}) was delivered to {self.hospital.name} Hospital"
        
    def getFirstHospitalData(self):
        for trans in self.feasible_transfers:
            if trans['hospital'] == self.hospital:
                return trans
    
    def getHospitalsOfDataType(self, hosp_type):
        return [trans for trans in self.feasible_transfers if 
                (trans['hospital'].type == hosp_type) and not(trans['hospital'] == self.hospital)]




class TransferCollection():
    '''A collection of ambulance transfers
    
    attributes:
    _items: Contains a set of transfers which can be organised and manipulated

    '''
    def __init__(self, trans_collection:Optional[Set[Transfer]] = None):
        if trans_collection != None:
            self._items = trans_collection
        else:
            self._items = set()

    def add(self, transfer: Transfer):
        self._items.add(transfer)


    def getHospitalsWithin(self, time, hospital_collection):
        '''Get hospitals that are accessible with a given time frame

        params:
        time: time threshold to be used
        hospital_collection: A set of hospitals to be checked
        '''
        for trans in self._items:
            hospitalTransfers(trans, hospital_collection, time)


    def generateJSONData(self):
        '''Create a dictionary ready for JSON encoding
        '''
        transfers_formatted = list()
        for transfer in self._items:
            transfer_dict = {
                'ppn': transfer.id,
                'pickup_lat': transfer.pickup_lat,
                'pickup_long': transfer.pickup_lon,
                'Calculated Transfers': {
                    'First Hospital': transfer.getFirstHospitalData(),
                    'Trauma Hospitals': transfer.getHospitalsOfDataType('trauma'),
                    'Spinal Specialist Hospitals': transfer.getHospitalsOfDataType('spinal')
                }
            }
            transfers_formatted.append(transfer_dict)
        return {'Ambulance Transfers':transfers_formatted}

    @staticmethod
    def csvParser(csv_filename:str, hospital_collection:'HospitalCollection'):
        '''Cycles through a csv and generates collection of Transfers

        params:
        csv_filename: Filename of csv to read
        '''
        csv_transfer = TransferCollection()

        with open(csv_filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                first_hosp_name = row['destination_name'].replace(' Hosp', '')
                hospital = hospital_collection.getByName(first_hosp_name)
                trans = Transfer(row['ppn'],row['pickup_latitude'], 
                                row['pickup_longitude'], hospital)
                csv_transfer.add(trans)
            return csv_transfer


