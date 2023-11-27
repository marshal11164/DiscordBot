import requests
from basededatos import *


class LolSettings:
    def __init__(self, summoner, tag):
        self.summoner = summoner
        self.tag = tag
        self.headers = {'X-Riot-Token': 'RGAPI-2e3ea10a-703d-4a47-ae9d-87abceaf197d'}

    def start(self):
        url = f'https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{self.summoner}/{self.tag}'
        response = requests.get(url, headers=self.headers)
        response_body = response.json()
        uid = response_body['puuid']
        url2 = f'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{uid}'
        response2 = requests.get(url2,headers=self.headers)
        return response2.json()

class Lol(LolSettings):
    def __init__(self, summoner, tag):
        super().__init__(summoner, tag)
    
    def rank(self):
        summoner = self.start()
        summoner_id = summoner['id']
        name = summoner['name']
        url = f'https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}'
        response = requests.get(url, headers=self.headers)
        dato = response.json()
        self.mysql(dato)
    
    def mysql(self, dato):
        self.conn = connexion()
        self.cursor = self.conn.cursor()

        summoner_ids = [x['summonerId'] for x in dato if x.get('queueType') == 'RANKED_SOLO_5x5']
        if summoner_ids:
            
            placeholders = ', '.join(['%s'] * len(summoner_ids))
        
            # Consultar los summonerids que ya están en la base de datos
            query_check = f"SELECT summonerid FROM rankeds WHERE summonerid IN ({placeholders})"
            self.cursor.execute(query_check, summoner_ids)
            existing_ids = set(row[0] for row in self.cursor.fetchall())
            print('ya existe')
            
        else:
            for x in dato:
                if x.get('queueType') == 'RANKED_SOLO_5x5' and x['summonerId'] not in existing_ids:
                    summonerid = x['summonerId']
                    summonername = x['summonerName']
                    liga = x['tier']
                    division = x['rank']
                    leaguepoints = x['leaguePoints']
                    wins = x['wins']
                    losses = x['losses']
                    query_insert = (
                        "INSERT INTO rankeds "
                        "(summonerid, summonername, liga, division, leaguepoints, wins, losses) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    )
                    values = (summonerid, summonername, liga, division, leaguepoints, wins, losses)
                    self.cursor.execute(query_insert, values)
                    self.conn.commit()

        self.cursor.close()
        self.conn.close()
        
