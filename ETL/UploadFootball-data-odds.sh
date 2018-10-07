sqlcmd -S localhost -U sa -P Passw0rd -d fixtures_v2 -Q "TRUNCATE TABLE staging.footballdata_odds"

for f in ./odds/E*.csv_odds ; do
    bcp staging.footballdata_odds  in $f -S localhost -U sa -P Passw0rd -d fixtures_v2 -c -t ','
    mv -f $f ./archive/$(basename $f);
done

sqlcmd -S localhost -U sa -P Passw0rd -d fixtures_v2 -Q "exec dbo.LoadFootballDataOdds"
