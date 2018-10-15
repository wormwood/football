#sqlcmd -S localhost -U sa -P Passw0rd -d fixtures_v2 -Q "exec dbo.PrepStaging"
#bcp staging.footballdata_fixtures  in ./football-data/football_extract.csv -S localhost -U sa -P Passw0rd -d fixtures_v2 -c -t ','
#sqlcmd -S localhost -U sa -P Passw0rd -d fixtures_v2 -Q "exec dbo.LoadFDFixtures"


import pandas as pd
import os
import glob
from sqlalchemy import create_engine
from sqlalchemy.sql import text as sa_text

uid='sa'
pwd='Passw0rd'
server='localhost'
db = 'fixtures_v2'

connstr="mssql://%s:%s@%s/%s?driver=FreeTDS&port=1433& odbc_options='TDS_Version=8.0'" % (uid,pwd,server,db)

engine = create_engine(connstr).connect()
engine.execute(sa_text('''EXEC dbo.PrepStaging''').execution_options(autocommit=True))
df = pd.read_csv('football-data/football_extract.csv')
df.to_sql(name='footballdata_fixtures', schema='staging', con=engine, if_exists='append', index=False)
engine.execute(sa_text('''EXEC dbo.LoadFDFixtures''').execution_options(autocommit=True))

engine.close()



