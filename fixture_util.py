

import pandas as pd 
import pandas.io.sql as psql
import pypyodbc

pd.set_option('display.max_colwidth', 18)
pd.set_option('colheader_justify', 'left')
pd.set_option('display.expand_frame_repr', False)

conn = pypyodbc.connect('DSN=dockersql;DATABASE=fixtures_v2;UID=sa;PWD=Passw0rd')

nextfix = psql.read_sql('EXEC GetUpcomingFixtures 1', conn)
print(nextfix)

conn.close()


