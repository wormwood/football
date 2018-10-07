
for year in 1819; do 
   for div in E0 E1 E2 E3; do
      wget -O $div$year.csv http://www.football-data.co.uk/mmz4281/$year/$div.csv 1> NUL 2> NUL ; 
      mv -f $div$year.csv ./odds/$div$year.csv
   done
done

for f in ./odds/E*.csv ; do
	python3 unpivot_odds.py $f odds/$(basename $f)_odds
    rm $f
done
