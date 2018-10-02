import csv
import urllib.request
import datetime


import json
from dateutil import parser

def get_matches(competition_id):
    # my api token
    headers={'X-Auth-Token': 'eaa1239b82654c72bd9d2541b8a042fc'}

    req = urllib.request.Request('http://api.football-data.org/v2/competitions/' + competition_id + '/matches', headers=headers)
    r = urllib.request.urlopen(req).read()

    #parse json into an array of matches
    matches=json.loads(r.decode('utf-8'))
    return matches


def write_results(results):

    date_as_string = datetime.datetime.now().strftime('%Y%m%d%s')
    filename='bbc/bbc_results_1_' + date_as_string + '.csv'
    fix_file = open(filename, 'w')
    print ('writing to ', filename)
    wr = csv.writer(fix_file, dialect='excel')
    wr.writerow(['FixtureDate', 'League','Fix_or_result', 'HomeTeam', 'AwayTeam', 'HTG_or_time', 'ATG'])
    for resultdate in results:
        wr.writerows([resultdate])
    
    fix_file.close()

all_fixtures=[]

for competition in ['2021', '2016'] :
    matches = get_matches(competition)
    for m in matches['matches']:
        matchtime = parser.parse(m['utcDate']).strftime("%H:%M")
        matchdate = parser.parse(m['utcDate']).strftime("%Y-%m-%d")
        if m['score']['fullTime']['homeTeam'] is not None:
            all_fixtures.append ([matchdate,matches['competition']['name'], '2', m['homeTeam']['name'], m['awayTeam']['name'], 
            m['score']['fullTime']['homeTeam'], m['score']['fullTime']['awayTeam']])
        else:
            all_fixtures.append ([matchdate,matches['competition']['name'], '1', m['homeTeam']['name'], m['awayTeam']['name'], 
            matchtime, 'N/A'])

#send fixtures to csv file in the same format as v2 of the bbc scraper
write_results(all_fixtures)