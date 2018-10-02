import pandas as pd
import sys

def unpivot(filename):
    df = pd.read_csv(filename)
    unpivot=pd.melt(df, id_vars=['Date','HomeTeam','AwayTeam'], value_vars=df.columns[24:].tolist(), 
        value_name='decimal_odds', var_name='bookmaker')
    unpivot['odds_res'] = unpivot.bookmaker.astype(str).str[-1]
    unpivot['bookmaker'] = unpivot.bookmaker.astype(str).str[0:-1]
    return unpivot

infile=sys.argv[1]
outfile = sys.argv[2]

df = unpivot(infile)
df.to_csv(outfile)