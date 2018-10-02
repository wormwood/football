for f in ./bbc/bbc_results_1_*.csv ; do
	printf "processing : %s\n" "$f"
	sqlcmd -S localhost -U sa -P Passw0rd -d fixtures_v2 -Q "exec dbo.PrepStaging"
	bcp staging.bbc_fixtures  in $f -S localhost -U sa -P Passw0rd -d fixtures_v2 -c -t ',';
	mv -f $f ./archive/$(basename $f);
done
sqlcmd -S localhost -U sa -P Passw0rd -d fixtures_v2 -Q "exec dbo.LoadBBCResults"
sqlcmd -S localhost -U sa -P Passw0rd -d fixtures_v2 -Q "exec dbo.FixtureStats"