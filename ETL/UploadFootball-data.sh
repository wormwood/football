sqlcmd -S localhost -U sa -P Passw0rd -d fixtures_v2 -Q "exec dbo.PrepStaging"
bcp staging.footballdata_fixtures  in ./football-data/football_extract.csv -S localhost -U sa -P Passw0rd -d fixtures_v2 -c -t ','
sqlcmd -S localhost -U sa -P Passw0rd -d fixtures_v2 -Q "exec dbo.LoadFDFixtures"

