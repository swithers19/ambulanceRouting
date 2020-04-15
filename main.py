from private import APIKEY, API_ENDPOINT
from lib.Ambulance import TransferCollection
from lib.Hospital import Hospital, HospitalCollection, getHospitalType
from lib.utils import hospitalTransfers, serialize, writeCSV

import requests
import googlemaps
import json
import csv


file_csv = 'Ambulance GIS and hospital address data sample.csv'

hosp_collection = HospitalCollection.hospitalScraper(file_csv)

transfer_collection = TransferCollection.csvParser(file_csv, hosp_collection)
transfer_collection.getHospitalsWithin(200000, hosp_collection)

csv_trans = transfer_collection.generateCSVData()
# json_ready_data = transfer_collection.generateJSONData()

# with open('data.json', 'w', encoding='utf-8') as f:
#     json.dump(json_ready_data, f, ensure_ascii=False, indent=4, default=serialize)

writeCSV("Hosp Transfers.csv", csv_trans)
# writeCSV("Trauma Hospitals.csv", csv_trauma)
# writeCSV("Spinal Hospitals.csv", csv_spinal)



