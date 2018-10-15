#sqlcmd -S localhost -U sa -P Passw0rd -d fixtures_v2 -Q "TRUNCATE TABLE staging.footballdata_odds"

#for f in ./odds/E*.csv_odds ; do
#    bcp staging.footballdata_odds  in $f -S localhost -U sa -P Passw0rd -d fixtures_v2 -c -t ','
#    mv -f $f ./archive/$(basename $f);
#done

#sqlcmd -S localhost -U sa -P Passw0rd -d fixtures_v2 -Q "exec dbo.LoadFootballDataOdds"

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

files = glob.glob('./odds/E*.csv_odds')
for file in files:
    print ('processing...', file)
    
    df = pd.read_csv(file)
    df.to_sql(name='footballdata_odds', schema='staging', con=engine, if_exists='append', index=False)
    # move file to archive folder
    os.rename(file, os.path.join('archive',os.path.basename(file)))

engine.execute(sa_text('''EXEC dbo.LoadBBCResults''').execution_options(autocommit=True))
engine.close()



