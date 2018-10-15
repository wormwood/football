#for f in ./bbc/bbc_results_1_*.csv ; do
#	printf "processing : %s\n" "$f"
#	sqlcmd -S localhost -U sa -P Passw0rd -d fixtures_v2 -Q "exec dbo.PrepStaging"
#	bcp staging.bbc_fixtures  in $f -S localhost -U sa -P Passw0rd -d fixtures_v2 -c -t ',';
#	mv -f $f ./archive/$(basename $f);
#done
#sqlcmd -S localhost -U sa -P Passw0rd -d fixtures_v2 -Q "exec dbo.LoadBBCResults"
#sqlcmd -S localhost -U sa -P Passw0rd -d fixtures_v2 -Q "exec dbo.FixtureStats"


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

files = glob.glob('bbc/bbc*.csv')
for file in files:
    print ('processing...', file)
    df = pd.read_csv(file)
    df.to_sql(name='bbc_fixtures', schema='staging', con=engine, if_exists='append', index=False)

engine.execute(sa_text('''EXEC dbo.LoadBBCResults''').execution_options(autocommit=True))
engine.close()



