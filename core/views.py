
from django.shortcuts import redirect, render
from django.http import JsonResponse, HttpResponse
import requests
import base64
import pandas as pd

class EPC_API:
    def __init__(self):

        email = 'olumide.moore2817@gmail.com'
        api_key = '51dae8b5fb342c818d4659f3ee600ac383d77403' #Olu's API key
        #You can get your own API key by registering on https://epc.opendatacommunities.org/login

        # Encoding credentials
        encoded_credentials = base64.b64encode(f'{email}:{api_key}'.encode()).decode()

        # API endpoint
        # url = 'https://epc.opendatacommunities.org/api/v1/non-domestic/recommendations/'
        # url = 'https://epc.opendatacommunities.org/api/v1/domestic/recommendations/01cc58bdf7440f9aedd576f9ed5b1fb999ee3611be4665abcd8c3068d176297d'
        self.url = 'https://epc.opendatacommunities.org/api/v1/non-domestic/search'
        # Headers
        self.headers = {
            'Authorization': f'Basic {encoded_credentials}',
            # 'Accept': 'text/csv'
            'Accept': 'application/json'
        }
        self.size = 1000
        self.current_postcode_records = []
    def get_addresses(self, postcode):
        self.current_postcode_records = []
        paginated_url = f"{self.url}?size={self.size}&postcode={postcode}"
            
        # Making the GET request
        response = requests.get(paginated_url, headers=self.headers)
        if response.status_code == 200:
            try:
                data = response.json() 
                # If data is returned, append it to the all_records list
                if data:
                    if 'rows' in data:
                        self.current_postcode_records = pd.DataFrame(data['rows'])
                        return list(map(lambda x: x['address'], data['rows']))
                else:
                    print(f'No data found for postcode: {postcode}')
            except Exception as e:
                print(f"Failed to fetch data.\nError: {e}")
        else:
            print(f'Failed to fetch data: {response.status_code}')
        return []
epc_api=EPC_API()

def home(request):
    return render(request, 'core/index.html')
def getaddresses(request):
    requestGET = request.GET
    postcode = requestGET.get('postcode')
    if postcode:
        addresses=epc_api.get_addresses(postcode)
        return  JsonResponse({'addresses':addresses})
    else:
        return JsonResponse({'error':'No postcode provided'})
    

def step2(request):
    requestGET = request.GET
    address = requestGET.get('address')
    data=epc_api.current_postcode_records.loc[epc_api.current_postcode_records['address']==address]
    # dic=data.iloc[:].to_dict()
    for index, col in data.items():
        print(f"{index}: {col[0]}")
    # print(epc_api.current_postcode_records.loc[epc_api.current_postcode_records['address']==address])
    if address:
        print(address)
    return JsonResponse({'error':'No postcode provided'})
