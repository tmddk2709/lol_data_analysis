import pandas as pd
from pandas.io.json import json_normalize
import requests


url = 'https://kr.api.riotgames.com/'


"""
get leagues by tier from riot api https://developer.riotgames.com/apis#league-v4

    api_key(string)  - api key 
    tier(string)     - tier
    division(string) - division
    page(integer)    - recommended page
    n_pages(integer) - recommended page number (0: all pages)
    
"""
def get_leagues(tier, division=None, page=1, n_pages=0):
    
    
    if tier in ['CHALLENGER', 'GRANDMASTER', 'MASTER']:
        req = requests.get(url + 'lol/league/v4/{0}/leagues/by-queue/RANKED_SOLO_5x5?api_key={1}'.format(tier.lowercase(), api_key))
        data = json_normalize(req.json()['entries'])
        data['tier'] = tier
        
    elif tier in ['DIAMOND', 'PLATINUM', 'GOLD', 'SILVER', 'BRONZE', 'IRON']:
        
        if n_pages == 0:
            while(True):
                req = requests.get(url + 'lol/league/v4/entries/RANKED_SOLO_5x5/{0}/{1}?page={2}&api_key={3}'.format(tier, division, page, api_key))


    
    
    