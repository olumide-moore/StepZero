#To run this code, you need to install 'requests' library
import requests
import base64
import pandas as pd

email = 'olumide.moore2817@gmail.com'
api_key = '51dae8b5fb342c818d4659f3ee600ac383d77403' #Olu's API key
#You can get your own API key by registering on https://epc.opendatacommunities.org/login

# Encoding credentials
encoded_credentials = base64.b64encode(f'{email}:{api_key}'.encode()).decode()

# API endpoint
# url = 'https://epc.opendatacommunities.org/api/v1/non-domestic/recommendations/'
# url = 'https://epc.opendatacommunities.org/api/v1/domestic/recommendations/01cc58bdf7440f9aedd576f9ed5b1fb999ee3611be4665abcd8c3068d176297d'
url = 'https://epc.opendatacommunities.org/api/v1/non-domestic/search'

# Headers
headers = {
    'Authorization': f'Basic {encoded_credentials}',
    # 'Accept': 'text/csv'
    'Accept': 'application/json'
}

# # Making the GET request
# response = requests.get(url, headers=headers,)
# # Checking if the request was successful
# if response.status_code == 200:
#     #Extracting the data to a csv file
#      with open('data4.csv', 'w') as file:
#         file.write(response.text)
# else:
#     print(f'Failed to fetch data: {response.status_code}')



# page = 1
# limit = 100  # Adjust based on what the API supports
# has_more_data = True

# # List to collect all records
# all_records = []
# post_code='SE11 5JH'
# post_code='B4 7UJ'
# while has_more_data:
#     # Update the API endpoint with pagination query parameters

#     # paginated_url = f"{url}?page={page}&limit={limit}&postcode={post_code}&address={'VOX STUDIOS WEST, Vox Studios, 1-45 Durham Street'}"
#     paginated_url = f"{url}?page={page}&limit={limit}&postcode={post_code}"
    
#     # Making the GET request
#     response = requests.get(paginated_url, headers=headers)  # Ensure 'headers' is defined as before
    
#     if response.status_code == 200:
#         try:
#             data = response.json()  # Assuming the response is in JSON format
#             # with open(f'data{page}.csv', 'w') as file:
#             #     file.write(response.text)
            
#             # If data is returned, append it to the all_records list
#             if data:  # Assuming 'data' is a list of records
#                 # print(list(data.keys())
#                 # print(data)
#                 print(list(map(lambda x: x['address'], data['rows'])))
#                 break
#                 all_records.extend(data)
#                 page += 1  # Go to the next page
#             else:
#                 # No more data, exit the loop
#                 has_more_data = False
#         except Exception as e:
#             print(f"Failed to process data on page {page}: {e}")
#             break
#     else:
#         print(f"Failed to fetch data on page {page}: {response.status_code}")
#         break

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
        return []
    
epc_api=EPC_API()
# epc_api.get_data('SE11 5JH')
epc_api.get_data('LE2 4FU')

epc_api.current_postcode_records
epc=epc_api.current_postcode_records['EPC']
dec=epc_api.current_postcode_records['DEC']
if not epc.empty and not dec.empty:
    addresses= pd.concat([epc['address'],dec['address']],ignore_index=True).drop_duplicates().to_list()
elif not epc.empty:
    addresses=epc['address'].drop_duplicates().to_list()
elif not dec.empty:
    addresses=dec['address'].drop_duplicates().to_list()
else:
    addresses=[]
print(addresses)

    
# df=epc_api.current_postcode_records
# print(df.columns)
# print(df[['address','address1','address2','address3','uprn','posttown','building-reference-number' ]])
# # addresses=df['address']
# # print(df)
# # print(df)
# # # print(df[addresses.isin(addresses[addresses.duplicated()])])
# # print(df[df['address']=='Brookside School, Severn Road']['lodgement-datetime'])
# # 0      OX20 1RW
# # 1       SS6 9BZ
# # 2       SS9 5SJ
# # 3       SS9 1SP
# # 4       B42 1NU
# #          ...
# # 995     LE2 4FU
# # 996    CF37 2DB
# # 997     M41 6AP
# # 998     GU9 8LU
# # 999    LS22 5BS