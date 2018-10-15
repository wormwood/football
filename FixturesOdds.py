from Fixtures import Fixtures
import requests
import pandas as pd

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
    
    def add_live_odds(self, bookie_key, leagueid):

        df_odds = self.get_odds(bookie_key, leagueid)
        self.add_odds(df_odds)

    def add_odds(self, df_odds):
        self.df.drop(['HomeOdds', 'DrawOdds', 'AwayOdds'], axis=1, inplace=True)
        self.df = self.df.merge(df_odds, left_on='HomeTeam', right_on='HomeTeam')
        return self


    def get_odds(self, bookie_key, leaugeid):
        
        apiKey='fc3fa79ee130aa6427d2d86743b794fc'
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
        
        first_team = [game['teams'][0] for game in games]
        x =  list(zip(home_teams,odds,first_team))
        
        df1=pd.DataFrame(x)
        df1[['AwayOdds', 'HomeOdds', 'DrawOdds']]=pd.DataFrame(df1[1].values.tolist(), index=df1.index)
        
    # swap Home and Away odds because the api mixes them up if it says the home team is the away team   
        saved_away=df1['AwayOdds']
        swapindex=df1[0]!=df1[2] # if the home team is wrong
        df1.loc[swapindex, 'AwayOdds']=df1['HomeOdds'] 
        df1.loc[swapindex, 'HomeOdds']=saved_away
        
        
        df1=pd.DataFrame(x, columns=['HomeTeam',1,2])
        df1[['AwayOdds', 'HomeOdds', 'DrawOdds']]=pd.DataFrame(df1[1].values.tolist(), index=df1.index)
        
        return df1[['HomeTeam','HomeOdds', 'DrawOdds', 'AwayOdds']]