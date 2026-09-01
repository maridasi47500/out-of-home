
mkdir templates 
python3 scaffold.py user username password email phone country_id:references
python3 scaffold.py city name country_id:references
python3 scaffold.py userhasarrival city_id:references user_id
python3 scaffold.py oohads city_id:references pic:file user_id message
python3 scaffold.py lyricsongs city_id lyrics user_id
python3 scaffold.py country name
