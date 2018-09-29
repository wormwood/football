import pandas as pd 
import os

names=['FixtureID', 'season', 'leagueid', 'fixDate','HomeTeamID', 'FTHG', 'AwayTeamID' , 'FTAG', 
         'HomeELO_prev', 'AwayELO_prev', 'HomeTeamResult', 'AwayTeamResult',
         'HomeTeam', 'AwayTeam', 'FTHG_3', 'FTAG_3', 'FTHG_5', 'FTAG_5']
         
class Fixtures():
    

    def __init__(self, fix_csv, names, refresh, start_date=None, end_date=None):
        if fix_csv is not None:
            self.fix_load(fix_csv, names, refresh, start_date, end_date)
        self.agg_cols=[]
            
        
            
    def fix_load(self, filename, names, refresh, start_date=None, end_date=None):
        if refresh :
            bcp_fixtures = "bcp vwCSV_2 out %s -S localhost -U sa -P Passw0rd -d fixtures_v2 -c -t ','" % filename
            os.system(bcp_fixtures)

        self.df = pd.read_csv(filename, header=None, names=names)
        self.df['FixtureDateAsDate'] = pd.to_datetime(self.df['fixDate'])
        self.df = self.df.sort_values(by='FixtureDateAsDate')
        self.Target_col_name='Target'
        self.df[self.Target_col_name]=self.df.HomeTeamResult.map({'W' : 1.0, 'D': 0.5, 'L':0.0})
        self.df['HTRecord']=self.df.HomeTeamResult.map({'W' : 1.0, 'D': 0.5, 'L':0.0})
        self.df['ATRecord']=self.df.AwayTeamResult.map({'W' : 1.0, 'D': 0.5, 'L':0.0})
        
        if start_date:
            self.df = self.df[self.df.FixtureDateAsDate >= start_date]
        if end_date:
            self.df = self.df[self.df.FixtureDateAsDate <= end_date]
        self.df['ExpectedResult']=1/(10**((self.df.AwayELO_prev - self.df.HomeELO_prev)/400))
        
        return self
    
    def clean(self):
        self.df.dropna(axis=0, how='any', inplace=True)
        return self
    
    def add_agg_col (self, prefix, by_col, agg_col, agg_func, window):
        newcol = prefix + '_'+agg_col+'_'+str(window)
        self.agg_cols.extend([newcol])
        self.df49 = self.df.groupby(by_col).rolling(window).agg({agg_col: agg_func}).reset_index()
        self.df49.rename(index=str, inplace=True, columns={agg_col: newcol})
        self.df = self.df.merge(self.df49[['level_1',newcol]], left_index=True, right_on='level_1')
        self.df.drop(['level_1'], axis=1, inplace=True)
        
#    def calc_diffs(self, prefix, delcols):
#        operand1 = [s for s in f.agg_cols if prefix in s][0]
#        operand2 = [s for s in f.agg_cols if prefix in s][1]
#        self.df[prefix] = self.df[operand1] - self.df[operand2]
#        if delcols:
#            self.df.drop([operand1, operand2], axis=1, inplace=True)
            
    def filter_by_col(self, column, val):
        self.df = self.df[self.df[column]==val]
        return self