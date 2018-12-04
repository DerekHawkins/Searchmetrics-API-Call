import requests
import json
import pandas as pd
from itertools import chain

### API Credentials ###
API_KEY = ""
API_SECRET = ""

### Payload Items for API Call ###
# To pull data, the Project ID, Search Engine Location, Domain of project, Dates and Limits are needed. For documentation on this,
## please see http://api.searchmetrics.com/v3/documentation/api-calls/service/ProjectOrganicGetListRankingsFilter
pid="1491139"
engine="29"
domain="goarmy.com"
#Dates are in YYYYMMDD format, build payload dates based on Fridays of the month
date=["20180831", "20180824", "20180817", "20180810", "20180803"]
limit="250"
realData = []

### Access Token / API Call ###
data = {
    'grant_type': 'client_credentials'
}

response = requests.post('http://api.searchmetrics.com/v3/token', data=data, auth=(
    API_KEY, API_SECRET)).json()

access_token = response['access_token']

url = ' http://api.searchmetrics.com/v3/'
#Name of the call (see documentations for additional calls) 
url += 'ProjectOrganicGetListRankingsFilter.json'
url += '?project_id=' + pid
url += '&se_id=' + engine
url += '&url=' + domain
url += '&limit=' + limit
url += '&access_token=' + access_token
for datechange in date:
    url += '&date=' + datechange
    sm_call = requests.get(url)
    response_json = sm_call.json()
    realData.append(response_json)

### Loop for acquiring and tabling date, keyword, position, search volume, and tags ###
data = realData
data_list = []
for i in range(5):
    dataVice = data[i]
    for each in range(0, len(dataVice["response"]),1):
        date = {"Date": dataVice["response"][each]["date"]}
        keyword = {"Keyword": dataVice["response"][each]["keyword"]}
        pos = dataVice["response"][each]["pos"]
        item = dict(chain(date.items(), keyword.items(), pos[0].items()))
        data_list.append(item)

### Dataframe formulation and saving ###
df = pd.DataFrame(data_list)
df = df[['Date', 'Keyword', 'cpc', 'position', 'traffic_volume', 'tags']]
df.rename(columns={'cpc': 'CPC', 'position':'Position', 'traffic_volume':'Traffic Volume', 'tags': 'Tags'}, inplace=True)
df.to_csv("")
