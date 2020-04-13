from private import APIKEY, API_ENDPOINT
from lib.Ambulance import TransferCollection
from lib.Hospital import Hospital, HospitalCollection
from lib.utils import hospitalTransfers, serialize

import requests
import googlemaps
import json


file_csv = 'Ambulance GIS and hospital address data sample.csv'

hosp_collection = HospitalCollection.hospitalScraper(file_csv)

transfer_collection = TransferCollection.csvParser(file_csv, hosp_collection)
transfer_collection.getHospitalsWithin(3600, hosp_collection)

json_ready_data = transfer_collection.generateJSONData()
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(json_ready_data, f, ensure_ascii=False, indent=4, default=serialize)
