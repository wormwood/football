from FixturesOdds import FixturesOdds
import FootballClf
import argparse
import requests
import pandas as pd


def get_odds(bookie_key):
    
    url="https://api.the-odds-api.com/v3/odds/?sport=soccer_epl&region=uk&apiKey=fc3fa79ee130aa6427d2d86743b794fc"
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


def do_args():

    parser = argparse.ArgumentParser()

    parser.add_argument('--predictday', help='day to use to predict results (YYYY-MM-DD)', required=True)
    parser.add_argument('--infile', help='csv to use for predictions')
    parser.add_argument('--outfile', help='csv to use for writing results of predictions')
    parser.add_argument('--league', help='integer representing the league for predictions', type=int)
    parser.add_argument('--refresh', help='If true, refresh the csv from the database', choices=['y', 'Y', 'n', 'N'], default='Y')

    args=  parser.parse_args()
    return args

args = do_args()

if args.infile:
    csvfile=args.infile

if args.predictday:
    predictday = args.predictday

if args.league:
    leagueid=args.league

refresh = args.refresh.upper()=='Y'


#if args.outfile:cmd
outfile = args.outfile


fix_pred=FixturesOdds()
fix_pred.fix_load('vwCSV_3','vwCSV_3.csv', False) # no reresh
fix_pred.do_calcs()

fix_pred.add_live_odds('skybet', int(leagueid))
#x =get_odds('skybet')
#fix_pred.add_odds(x)
fix_pred.clean_predict()

fix_pred.filter_by_col('FixtureDateAsDate', predictday).filter_by_col('leagueid', int(leagueid))
X=fix_pred.X()

c=FootballClf.FootballClf()
clf=c.load_by_name('betting clf')

fix_pred.df['prediction']=clf.predict(X)
print(fix_pred.df[['FixtureDateAsDate','HomeTeam', 'AwayTeam', 'prediction']])

if outfile is not None:
    with open(outfile, 'a') as f:
        fix_pred.df[['FixtureDateAsDate','HomeTeam', 'AwayTeam', 'prediction']].to_csv(f, header=False)
