from private import APIKEY, API_ENDPOINT
import requests
import urllib

file_csv = 'Ambulance GIS and hospital address data sample.csv'

lat_origin = -34.790257
lon_origin = 150.56216

lat_dest = 	-34.868135
lon_dest = 150.595159

parameters = {
    'origins':f'{lat_origin},{lon_origin}',
    'destinations':f'{lat_dest},{lon_dest}',
    'key':APIKEY
}

response = requests.get(API_ENDPOINT, params = parameters)

print(response.status_code)
print(response.json())