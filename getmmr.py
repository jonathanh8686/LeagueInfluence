import requests
import json

def get_mmr(usr):
    URL = "https://na.whatismymmr.com/api/v1/summoner?name=" + usr
    print("Making request to get MMR")
    r = requests.get(URL)

    resp = r.json()
    if("error" in resp):
        return "ERROR"

    return(resp["ranked"]["avg"])

