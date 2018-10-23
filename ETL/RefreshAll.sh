echo "getting fixtures from football data"
./get_football-data.sh
echo "loading fixtures from football data"
./UploadFootball-data.sh
echo "getting fixtures from football api"
./football-data-api.py
echo "loading fixtures from football api"
./UploadFootball-api.py
echo "getting odds from football data"
./get_odds.sh
echo "loading odds from football data"
./UploadFootball-data-odds.sh
echo "Uploading ELOs"
./DoAllELOs.sh