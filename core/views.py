
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
        # self.url = 'https://epc.opendatacommunities.org/api/v1/non-domestic/search'
        # self.url = 'https://epc.opendatacommunities.org/api/v1/display/search'
        self.urls={'EPC':'https://epc.opendatacommunities.org/api/v1/non-domestic/search','DEC':'https://epc.opendatacommunities.org/api/v1/display/search'}
        # Headers
        self.headers = {
            'Authorization': f'Basic {encoded_credentials}',
            # 'Accept': 'text/csv'
            'Accept': 'application/json'
        }
        self.size = 1000
        self.current_postcode_records = {'EPC':pd.DataFrame(),'DEC':pd.DataFrame()}
    def get_data(self, postcode):
        """
        Retrieves data for a given postcode.
        Arguments:  postcode (str): The postcode for which to retrieve addresses.
        Returns:  list: A pandas Dataframe of data (both found in EPC and DEC) retrieved for the given postcode.
        Example:
            >>> obj = EPC_API()
            >>> obj.get_data('SE12 2DG)
        """
        self.current_postcode_records = {'EPC':pd.DataFrame(),'DEC':pd.DataFrame()}
        for type, url in self.urls.items():
            # if type=='EPC': continue
            paginated_url = f"{url}?size={self.size}&postcode={postcode}"
            # Making the GET request
            response = requests.get(paginated_url, headers=self.headers)
            if response.status_code == 200:
                try:
                    if response.content != b'':
                        data = response.json() 
                        # If data is returned, append it to the all_records list
                        if data:
                            if 'rows' in data:
                                self.current_postcode_records[type] = pd.DataFrame(data['rows'])
                                # return list(map(lambda x: x['address'], data['rows']))
                        else:
                            print(f'No data found for postcode: {postcode}')
                except Exception as e:
                    print(f"Failed to fetch data.\nError: {e}")
            else:
                print(f'Failed to fetch data: {response.status_code}')
        return
    def get_addresses(self):
        epc=self.current_postcode_records['EPC']
        dec=self.current_postcode_records['DEC']
        if not epc.empty and not dec.empty:
            addresses= pd.concat([epc['address'],dec['address']],ignore_index=True).drop_duplicates().to_list()
        elif not epc.empty:
            addresses=epc['address'].drop_duplicates().to_list()
        elif not dec.empty:
            addresses=dec['address'].drop_duplicates().to_list()
        else:
            addresses=[]
        return addresses

epc_api=EPC_API()
def home(request):
    return render(request, 'core/index.html')
def getaddresses(request):
    requestGET = request.GET
    postcode = requestGET.get('postcode')
    if postcode:
        epc_api.get_data(postcode)
        addresses=epc_api.get_addresses()
        return  JsonResponse({'addresses':addresses})
    else:
        return JsonResponse({'error':'No postcode provided'})
    

def step2(request):
    print(epc_api.current_postcode_records)
    requestGET = request.GET
    address = requestGET.get('address')
    dec=epc_api.current_postcode_records['DEC']
    epc=epc_api.current_postcode_records['EPC']
    if not dec.empty and not dec.loc[dec['address']==address].empty:
        found_data=dec.loc[dec['address']==address]
        found_in='DEC'
    elif not epc.empty and not epc.loc[epc['address']==address].empty:
        found_data=epc.loc[epc['address']==address]
        found_in='EPC'
    else:
        return JsonResponse({'error':'No data found'})
    latest_data=found_data.loc[found_data['lodgement-datetime'].idxmax()]
    print(latest_data)
    return JsonResponse({'data':latest_data.to_dict(),'found_in':found_in})


    # if not epc_api.current_postcode_records['DEC'].empty and not epc:
    #     dec=epc_api.current_postcode_records['DEC']
    #     data=dec.loc[dec['address']==address]
    #     if not data.empty:
    #         dic=data.iloc[:].to_dict()
    #         return JsonResponse({'data':dic})
    # if not epc_api.current_postcode_records['EPC'].empty:
    #     epc=epc_api.current_postcode_records['EPC']
    #     data=epc.loc[epc['address']==address]
    #     if not data.empty:
    #         dic=data.iloc[:].to_dict()
    #         return JsonResponse({'data':dic})
                                            
    # # print(epc_api.current_postcode_records)
    # # print(address)
    # # if address:
    # #     data=epc_api.current_postcode_records.loc[epc_api.current_postcode_records['address']==address]
    # #     print(data)
    # #     # dic=data.iloc[:].to_dict()
    # #     # for index, col in data.items():
    # #     #     print(f"{index}: {col[0]}")
    # #     # # print(epc_api.current_postcode_records.loc[epc_api.current_postcode_records['address']==address])
    # #     # if address:
    # #     #     print(address)
    # print(address)
    # return JsonResponse({'error':'No postcode provided'})
