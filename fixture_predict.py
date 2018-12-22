from FixturesOdds import FixturesOdds
import FootballClf
import argparse
import requests
import pandas as pd


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


outfile=None
if args.outfile:
    outfile = args.outfile


fix_pred=FixturesOdds()
fix_pred.fix_load('vwCSV_3','vwCSV_3.csv', refresh) # no reresh
fix_pred.do_calcs()

fix_pred.add_live_odds('skybet', int(leagueid),predictday)
fix_pred.clean_predict()

fix_pred.filter_by_col('FixtureDateAsDate', predictday).filter_by_col('leagueid', int(leagueid))
X=fix_pred.X()

c=FootballClf.FootballClf()
clf=c.load_by_name('betting clf_2.2')
pd.set_option('display.max_colwidth', 18)
pd.set_option('colheader_justify', 'left')
pd.set_option('display.expand_frame_repr', False)

fix_pred.df['prediction']=clf.predict(X)
fix_pred.df.sort_values('HomeTeam', inplace=True)

print(fix_pred.df[['FixtureDateAsDate','HomeTeam', 'AwayTeam', 'prediction', 'HomeOdds', 'DrawOdds', 'AwayOdds']])

if outfile is not None:
    with open(outfile, 'a') as f:
        fix_pred.df[['FixtureDateAsDate','HomeTeam', 'AwayTeam', 'prediction', 'HomeOdds', 'DrawOdds', 'AwayOdds']].to_csv(f, header=False)

