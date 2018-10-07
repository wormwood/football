
for year in 1819; do 
   for div in E0 E1 E2 E3; do
      wget -O $div$year.csv http://www.football-data.co.uk/mmz4281/$year/$div.csv 1> NUL 2> NUL ; 
      mv -f $div$year.csv ./football-data/$div$year.csv
   done
done

for f in ./football-data/E*.csv ; do
	python3 unpivot_odds.py $f football-data/$(basename $f)_odds
done