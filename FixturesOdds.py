from Fixtures import Fixtures

class FixturesOdds(Fixtures):
    
    def __init__(self):
        self.names=['FixtureID', 'season', 'leagueid', 'fixDate','HomeTeamID', 'FTHG', 'AwayTeamID' , 'FTAG', 
         'HomeELO_prev', 'AwayELO_prev', 'HomeTeamResult', 'AwayTeamResult',
         'HomeTeam', 'AwayTeam', 'FTHG_3', 'FTAG_3', 'FTHG_5', 'FTAG_5', 'HomeOdds', 'DrawOdds', 'AwayOdds']

        self.agg_cols=[]
    
    def X(self):
        return self.df[['ExpectedResult', 'FTG_3', 'FTG_5', 'HomeOdds', 'DrawOdds', 'AwayOdds']].values
    
    def add_odds(self, df_odds):
        self.df.drop(['HomeOdds', 'DrawOdds', 'AwayOdds'], axis=1, inplace=True)
        self.df = self.df.merge(df_odds, left_on='HomeTeam', right_on='HomeTeam')
        return self