
import requests
import json


# Function

def callData(additionalParams, saveas): 
    url = "https://v3.football.api-sports.io/" + additionalParams

    payload={}
    headers = {
    'x-apisports-key': 'e0792fb991d634c3fc3d00e301b658d4',
    'x-rapidapi-host': 'v3.football.api-sports.io'
    }

    response = requests.request("GET", url, headers=headers, data=payload).json()
    

    with open(saveas +".json", "w") as json_file:
        json.dump(response, json_file)

#Format of the Streamlit report



# Top scorers
#topScorers = callData("players/topscorers?season=2021&league=78", "topscorers")

# Team Statistics
#teamStatistics = callData(,)


