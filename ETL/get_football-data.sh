
: > football_extract.csv

for year in 1516 1617 1718 1819; do 
   for div in E0 E1 E2 E3; do
      wget -O $div$year.csv http://www.football-data.co.uk/mmz4281/$year/$div.csv 1> NUL 2> NUL ; 
      mv -f $div$year.csv ./football-data/$div$year.csv
   done
done

for f in ./football-data/E*.csv ; do
  cut -d ',' -f1-6 "$f" >> ./football-data/football_extract.csv; 
  mv -f $f ./archive/$(basename $f);
done

sed -i -e '1d' football_extract.csv
