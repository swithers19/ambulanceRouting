from typing import List, Optional, Set, Dict
import csv, operator

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
        self.def_hospital = None
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

    def getHospitalByAttr(self, key, value):
        return [trans for trans in self.feasible_transfers if 
                (getattr(trans['hospital'], key) == value) and not(trans['hospital'] == self.hospital)]

    def getMinByDistance(self, key, value):
        trips = self.getHospitalByAttr(key, value)
        if trips:
            return min(trips, key=lambda x:x['distance'])

        

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

        returns: dictionary of each transfer and associated feasible lists
        '''
        transfers_formatted = list()
        items_sorted = sorted(self._items, key=lambda x: int(x.id))
        for transfer in items_sorted:
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


    def generateCSVData(self):
        trans = list()
        items_sorted = sorted(self._items, key=lambda x: int(x.id))

        for transfer in items_sorted:
            first_hosp_data = transfer.getFirstHospitalData()
            min_dist_trauma = transfer.getMinByDistance('type', 'trauma')
            min_dist_spinal = transfer.getMinByDistance('type', 'spinal')
            first_hosp_dict = self.__createDict("First", first_hosp_data)
            trauma_hosp_dict = self.__createDict("Trauma", min_dist_trauma, True)
            spinal_hosp_dict = self.__createDict("Spinal", min_dist_spinal, True)
            print(spinal_hosp_dict)
            transfer_dict = {
                'ppn': transfer.id,
                'pickup_lat': transfer.pickup_lat,
                'pickup_long': transfer.pickup_lon,
                'First Hospital': transfer.hospital,
                'Final Hospital': None,
                'Time to First Hospital': first_hosp_data['time'], 
                'Distance to First Hospital': first_hosp_data['distance'],
                'Time to Nearest Trauma Hospital': min_dist_trauma['time'],
                'Distance to Nearest Trauma Hospital': min_dist_trauma['distance'],
                'Time to Nearest Spinal Hospital': min_dist_spinal['time'],
                'Distance to Nearest Spinal Hospital': min_dist_spinal['distance'],
            }
            trans.append(transfer_dict)
        return trans

    def __createDict(self, hosp_criteria, trip, set_hosp=False):
        hosp_list = list()
        holding_dict = {
            f"Time to {hosp_criteria} Hospital": trip['time']/60,
            f"Distance to {hosp_criteria} Hospital": trip['distance']/1000
        }
        if set_hosp:
              holding_dict[f"Nearest {hosp_criteria} Hospital"] = trip['hospital']

        return holding_dict


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
                                row['pickup_longitude'], hospital, )
                csv_transfer.add(trans)
            return csv_transfer
