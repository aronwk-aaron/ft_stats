from bs4 import BeautifulSoup
import urllib.request
import csv
import pandas as pd
from os import remove

pocket_lists = [None,None,None,None,None,None]

try:
    fp = open('sites.txt')

    for cnt, line in enumerate(fp):
        print(line)
        page = urllib.request.urlopen(line)
        html = page.read()
        soup = BeautifulSoup(html, features='html.parser')
        table = soup.select_one('table.leaderboard')
        #  SO UGLY
#         no_head = table.replace(
#         '<table class="leaderboard">\n\
# <thead><tr>\n\
# <td>Rank</td><td>Agent</td><td>Score</td>\n\
# </tr></thead>\n\
# <tbody>\n\
# ','')
#         no_head_and_foot = no_head.replace('\n</tbody></table>', '')
#         print(no_head_and_foot)
#         pocket_lists[cnt] = no_head_and_foot
        pocket_lists[cnt] = table

finally:
    fp.close()
with open("glyphs.csv", "w") as f:
    wr = csv.writer(f)
    wr.writerow(['rank', 'name', 'glyph points'])
    wr.writerows([[td.text.encode("utf-8") for td in row.find_all("td")] for row in pocket_lists[0].select("tr + tr")])
with open("walks.csv", "w") as f:
    wr = csv.writer(f)
    wr.writerow(['rank', 'name', 'walking distance'])
    wr.writerows([[td.text.encode("utf-8") for td in row.find_all("td")] for row in pocket_lists[1].select("tr + tr")])
with open("artifacts.csv", "w") as f:
    wr = csv.writer(f)
    wr.writerow(['rank', 'name', 'artifacts collected'])
    wr.writerows([[td.text.encode("utf-8") for td in row.find_all("td")] for row in pocket_lists[2].select("tr + tr")])
with open("hacks.csv", "w") as f:
    wr = csv.writer(f)
    wr.writerow(['rank', 'name', 'hacks'])
    wr.writerows([[td.text.encode("utf-8") for td in row.find_all("td")] for row in pocket_lists[3].select("tr + tr")])
with open("mods.csv", "w") as f:
    wr = csv.writer(f)
    wr.writerow(['rank', 'name', 'mods deployed'])
    wr.writerows([[td.text.encode("utf-8") for td in row.find_all("td")] for row in pocket_lists[4].select("tr + tr")])
with open("deploys.csv", "w") as f:
    wr = csv.writer(f)
    wr.writerow(['rank', 'name', 'resos deployed'])
    wr.writerows([[td.text.encode("utf-8") for td in row.find_all("td")] for row in pocket_lists[5].select("tr + tr")])

g = pd.read_csv('glyphs.csv').drop(['rank'], axis=1)
w = pd.read_csv('walks.csv').drop(['rank'], axis=1)
a = pd.read_csv('artifacts.csv').drop(['rank'], axis=1)
h = pd.read_csv('hacks.csv').drop(['rank'], axis=1)
m = pd.read_csv('mods.csv').drop(['rank'], axis=1)
d = pd.read_csv('deploys.csv').drop(['rank'], axis=1)

merged = pd.merge(g, w, on='name')
merged = pd.merge(merged, a, on='name')
merged = pd.merge(merged, h, on='name')
merged = pd.merge(merged, m, on='name')
merged = pd.merge(merged, d, on='name')

merged['name'] = merged['name'].map(lambda x: x.lstrip('b\'').rstrip('\''))
merged['glyph points'] = merged['glyph points'].map(lambda x: x.lstrip('b\'').rstrip('\''))
merged['walking distance'] = merged['walking distance'].map(lambda x: x.lstrip('b\'').rstrip('\''))
merged['artifacts collected'] = merged['artifacts collected'].map(lambda x: x.lstrip('b\'').rstrip('\''))
merged['hacks'] = merged['hacks'].map(lambda x: x.lstrip('b\'').rstrip('\''))
merged['mods deployed'] = merged['mods deployed'].map(lambda x: x.lstrip('b\'').rstrip('\''))
merged['resos deployed'] = merged['resos deployed'].map(lambda x: x.lstrip('b\'').rstrip('\''))

merged.to_csv('final.csv', index = None, header=True)

remove('glyphs.csv')
remove('walks.csv')
remove('artifacts.csv')
remove('hacks.csv')
remove('mods.csv')
remove('deploys.csv')
