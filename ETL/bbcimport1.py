import csv
import urllib.request
from bs4 import BeautifulSoup 
import re
import datetime
import sys, getopt
import argparse

def get_bbc_fix_html(fix_date):
    bbc_url='http://www.bbc.co.uk/sport/football/scores-fixtures/'+fix_date
    with urllib.request.urlopen(bbc_url) as response:
        html = response.read()
        return html


def parse_a_fixture(fixture_div):
    if fixture_div.contents[1].text :
        # its a fixture, not a result
        return (1, 
                fixture_div.span.span.abbr['title'], 
                fixture_div.contents[2].contents[0].abbr['title'],
                fixture_div.contents[1].text,
                'N/A'
               )
    else:
        #its probably a result
        return (2,
                fixture_div.span.span.abbr['title'], # HomeTeam
                fixture_div.contents[2].span.span.abbr['title'], # AwayTeam
                fixture_div.contents[0].contents[1].text, # Home Team Goals

                fixture_div.contents[2].contents[1].text  #Away Team Goals
               )

def write_results(results):

    date_as_string = datetime.datetime.now().strftime('%Y%m%d')
    filename='bbc/bbc_results_1_' + date_as_string + '.csv'
    fix_file = open(filename, 'w')
    print ('writing to ', filename)
    wr = csv.writer(fix_file, dialect='excel')
    wr.writerow(['FixtureDate', 'League','Fix_or_result', 'HomeTeam', 'AwayTeam', 'HTG_or_time', 'ATG'])
    for resultdate in results:
        wr.writerows([resultdate])
    
    fix_file.close()

def do_args():

    parser = argparse.ArgumentParser()

    parser.add_argument('--numdays', help='number of days (forward and back) to scrape')
    args = parser.parse_args()
    return args

args = do_args()

numdays=3

if args.numdays :
    numdays=int(args.numdays)


base = datetime.datetime.today()
fix_dates = [(base - datetime.timedelta(days=x)).strftime('%Y-%m-%d') for x in range(-numdays, numdays)]


all_fixtures=[]
for fix_date in fix_dates:
    print ('getting fixtures for', fix_date)
    html = get_bbc_fix_html(fix_date)
    soup = BeautifulSoup(html, "lxml")
    divs = soup.find_all("h3", {"class" : "sp-c-match-list-heading"})
    for div in divs:
        fixture_divs=div.parent.find_all("div", {"class" : "sp-c-fixture__wrapper"})
        for fd in fixture_divs:
            fix_or_result, HT, AT, HTG_or_time, ATG = parse_a_fixture(fd)
            all_fixtures.append([fix_date, div.text, fix_or_result, HT, AT, HTG_or_time, ATG])

write_results(all_fixtures)
