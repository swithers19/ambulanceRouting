from typing import Optional, List
import csv

specialist_spinal = ['Royal North Shore', 'Prince of Wales']


class Hospital():
    '''Class containing information pertaining to hospital

    attributes:
    name: Name of hospital
    address: Address of hospital
    type: Type of hospital
    '''
    def __init__(self, name: str, address: str, hosp_type):
        self.name = name
        self.address = address
        self.type = hosp_type

    def toJson(self):
        return self.name + "Hospital"

    def __eq__(self, other: 'Hospital'):
        return (self.name == other.name
                and self.address == other.address
                and self.type == other.type)

    def __str__(self):
        return f"{self.name} Hospital is of type {self.type} at {self.address}" 

    def __repr__(self):
        return f"{self.name} Hospital"

    def isType(self, type:str)->bool:
        return type == self.type


class HospitalCollection():
    '''Collection of Hospitals which acts as a utlity class

    attributes:
    _items: A list of Hospitals 
    '''
    def __init__(self, hospital_collection: Optional['HospitalCollection'] = None):
        if hospital_collection != None:
            self._items = hospital_collection._items
        else:
            self._items = list()

    def __len__():
        return len(self._items)

    def __getitem__(self, position):
        return self._items[position]

    def add(self, hosp):
        self._items.append(hosp)

    def getAddresses(self):
        return [hosp.address for hosp in self._items]

    def removeHospital(self, hosp:'hospital')->'HospitalCollection':
        '''Remove a hospital froma collection'''
        new_collection = HospitalCollection(self)
        new_collection._items.remove(hosp)
        return new_collection

    def getByType(self, hosp_type)->'HospitalCollection':
        '''Get hospitals of a particular type'''
        type_collection = HospitalCollection()
        for hosp in self._items:
            if hosp.type == hosp_type:
                type_collection.add(hosp)
        return type_collection

    def getByName(self, hosp_name)->'Hospital':
        '''Return a hospital in a collection by name'''
        for hosp in self._items:
            if hosp.name == hosp_name:
                return hosp
        return None


    @staticmethod
    def hospitalScraper(csv_data):
        '''Scrape through csv and get all hospitals and load into HospitalCollection
        
        params:
        csv_data: CSV file to scrape

        returns:
        hosp_collection: A Collection of all the hospitals processed in the csv
        '''
        hosp_collection = HospitalCollection()

        with open(csv_data, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            hospital_names = set()
            for row in reader:
                #Clean up hospital names
                hosp_name = row['destination_name'].replace(' Hosp', '')
                #Only add new hospitals to collection
                if hosp_name not in hospital_names:
                    new_hosp = Hospital(name = hosp_name, 
                                        address = row['first_hosp_address'], 
                                        hosp_type = getHospitalType(hosp_name))
                    hosp_collection.add(new_hosp)
                    hospital_names.add(hosp_name)
            
        return hosp_collection


def getHospitalType(hosp_name:str):
    if hosp_name in specialist_spinal:
        return 'spinal'
    else:
        return 'trauma'
