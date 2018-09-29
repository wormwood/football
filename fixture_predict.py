import Fixtures
import FootballClf
import argparse


def do_args():

    parser = argparse.ArgumentParser()

    parser.add_argument('--predictday', help='day to use to predict results (YYYY-MM-DD)')
    parser.add_argument('--infile', help='csv to use for predictions')
    parser.add_argument('--league', help='integer representing the league for predictions')

    args=  parser.parse_args()
    return args

args = do_args()

if args.infile:
    csvfile=args.infile

if args.predictday:
    predictday = args.predictday

if args.league:
    leagueid=args.league

fix_pred = Fixtures.Fixtures(csvfile, Fixtures.names,False)

fix_pred.df['FTG_3']=fix_pred.df.FTHG_3 - fix_pred.df.FTAG_3
fix_pred.df['FTG_5']=fix_pred.df.FTHG_5 - fix_pred.df.FTAG_5
fix_pred.filter_by_col('FixtureDateAsDate', predictday).filter_by_col('leagueid', int(leagueid))

X=fix_pred.df[['ExpectedResult', 'FTG_3', 'FTG_5']]

c=FootballClf.FootballClf()

clf=c.load_by_name('small clf')

fix_pred.df['prediction']=clf.predict(X)
print(fix_pred.df[['HomeTeam', 'AwayTeam', 'prediction']])

