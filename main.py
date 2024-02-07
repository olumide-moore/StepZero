#To run this code, you need to install 'requests' library
import requests
import base64


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



page = 1
limit = 100  # Adjust based on what the API supports
has_more_data = True

# List to collect all records
all_records = []
post_code='SE11 5JH'
post_code='B4 7UJ'
while has_more_data:
    # Update the API endpoint with pagination query parameters

    # paginated_url = f"{url}?page={page}&limit={limit}&postcode={post_code}&address={'VOX STUDIOS WEST, Vox Studios, 1-45 Durham Street'}"
    paginated_url = f"{url}?page={page}&limit={limit}&postcode={post_code}"
    
    # Making the GET request
    response = requests.get(paginated_url, headers=headers)  # Ensure 'headers' is defined as before
    
    if response.status_code == 200:
        try:
            data = response.json()  # Assuming the response is in JSON format
            # with open(f'data{page}.csv', 'w') as file:
            #     file.write(response.text)
            
            # If data is returned, append it to the all_records list
            if data:  # Assuming 'data' is a list of records
                # print(list(data.keys())
                # print(data)
                print(list(map(lambda x: x['address'], data['rows'])))
                break
                all_records.extend(data)
                page += 1  # Go to the next page
            else:
                # No more data, exit the loop
                has_more_data = False
        except Exception as e:
            print(f"Failed to process data on page {page}: {e}")
            break
    else:
        print(f"Failed to fetch data on page {page}: {response.status_code}")
        break