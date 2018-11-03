from Fixtures import Fixtures
import requests
import pandas as pd
from datetime import datetime

def swap (row):
    if row[0]!= row[2]:
        return[row[0], row[1],row[2],row[3],row['AwayOdds'], row['DrawOdds'], row['HomeOdds']]
    else:
        return[row[0], row[1],row[2],row[3],row['HomeOdds'], row['DrawOdds'], row['AwayOdds']]

def format_commence_time(commence_time):
    return datetime.utcfromtimestamp(int(commence_time)).strftime('%Y-%m-%d')

class FixturesOdds(Fixtures):
    
    def __init__(self):
        self.names=['FixtureID', 'season', 'leagueid', 'fixDate','HomeTeamID', 'FTHG', 'AwayTeamID' , 'FTAG', 
         'HomeELO_prev', 'AwayELO_prev', 'HomeTeamResult', 'AwayTeamResult',
         'HomeTeam', 'AwayTeam', 'FTHG_3', 'FTAG_3', 'FTHG_5', 'FTAG_5', 'HomeOdds', 'DrawOdds', 'AwayOdds']

        self.predict_cols=['ExpectedResult', 'FTG_3', 'FTG_5', 'HomeOdds', 'DrawOdds', 'AwayOdds']

    def clean_predict(self):
        self.df.dropna(axis=0, how='any', inplace=True, subset=self.predict_cols)
        return self

    def X(self):
        return self.df[self.predict_cols].values
    
    def add_live_odds(self, bookie_key, leagueid,predictday):

        df_odds = self.get_odds(bookie_key, leagueid)
        df_odds=df_odds[df_odds.fixdate==predictday]
        self.add_odds(df_odds)

    def add_odds(self, df_odds):
        self.df.drop(['HomeOdds', 'DrawOdds', 'AwayOdds'], axis=1, inplace=True)
        self.df = self.df.merge(df_odds, left_on=['HomeTeam'], right_on=['HomeTeam'])
        return self



    def get_odds(self, bookie_key, leaugeid):
        apiKey='fc3fa79ee130aa6427d2d86743b794fc'
        apiKey = 'edddec034215860d93d49887ede78024'
        sports = {1 : 'soccer_epl', 2: 'soccer_efl_champ'}
        sport = sports[leaugeid]
        url = "https://api.the-odds-api.com/v3/odds/?sport=%s&region=uk&apiKey=%s" % (sport,apiKey)

        #url="https://api.the-odds-api.com/v3/odds/?sport=soccer_epl&region=uk&apiKey=fc3fa79ee130aa6427d2d86743b794fc"
        r = requests.get(url=url)
        json=r.json()
        games = json['data']

        home_teams = [game['home_team'] for game in games]
        sites = [game['sites'] for game in games]
        odds=[s['odds']['h2h'] for site in sites for s in site if s['site_key']==bookie_key]
        dates=[format_commence_time(game['commence_time']) for game in games]

        first_team = [game['teams'][0] for game in games]
        x =  list(zip(home_teams,odds,first_team,dates))
        
        df1=pd.DataFrame(x)

        df1[['HomeOdds', 'AwayOdds', 'DrawOdds']]=pd.DataFrame(df1[1].values.tolist(), index=df1.index)
        df1=df1[[0,1,2,3,'HomeOdds', 'DrawOdds', 'AwayOdds']].apply(swap,1)
        df1.replace({'Bournemouth' : 'AFC Bournemouth'}, inplace=True)
        df1.replace({'Brighton and Hove Albion' : 'Brighton & Hove Albion'}, inplace=True)
        df1.rename(columns={0:'HomeTeam',3:'fixdate'}, inplace=True)
        return df1[['HomeTeam','fixdate', 'HomeOdds', 'DrawOdds', 'AwayOdds']]

