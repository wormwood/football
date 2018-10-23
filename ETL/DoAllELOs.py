#sqlcmd -S localhost -U sa -P Passw0rd -d fixtures_v2 -Q "exec dbo.DoAllELOs 64"


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
engine.execute(sa_text('''EXEC dbo.DoAllELOs 64''').execution_options(autocommit=True))


engine.close()



