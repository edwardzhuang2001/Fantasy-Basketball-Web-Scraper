import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime

url = 'https://hashtagbasketball.com/fantasy-basketball-projections'
response = requests.get(url)

bad_data = ['R#', 'ADP', 'PLAYER', 'POS', 'TEAM', 'GP', 'MPG', 'FG%', 'FT%', '3PM', 'PTS', 'TREB', 'AST', 'STL', 'BLK', 'TO', 'TOTAL']

soup = BeautifulSoup(response.content, 'html.parser')
raw_data_html = soup.find('table', class_='table--statistics').find_all('td')
raw_data_text = [raw_data_html[i].get_text().strip() for i in range(len(raw_data_html)) if raw_data_html[i].get_text().strip() not in bad_data]
data = [raw_data_text[i:i+17] for i in range(0, len(raw_data_text), 17)]

percentage_stat_pattern = r'([\d.]+)\n+\(([\d.]+)/([\d.]+)\)'

ranks = [data[i][0] for i in range(len(data))]
adps = [data[i][1] for i in range(len(data))]
players = [data[i][2] for i in range(len(data))]
fgm = [float(re.search(percentage_stat_pattern, data[i][7]).group(2)) for i in range(len(data))]
fga = [float(re.search(percentage_stat_pattern, data[i][7]).group(3)) for i in range(len(data))]
fgp = [float(re.search(percentage_stat_pattern, data[i][7]).group(1)) for i in range(len(data))]
ftm = [float(re.search(percentage_stat_pattern, data[i][8]).group(2)) for i in range(len(data))]
fta = [float(re.search(percentage_stat_pattern, data[i][8]).group(3)) for i in range(len(data))]
ftp = [float(re.search(percentage_stat_pattern, data[i][8]).group(1)) for i in range(len(data))]
_3pm = [data[i][9] for i in range(len(data))]
pts = [data[i][10] for i in range(len(data))]
reb = [data[i][11] for i in range(len(data))]
ast = [data[i][12] for i in range(len(data))]
stl = [data[i][13] for i in range(len(data))]
blk = [data[i][14] for i in range(len(data))]
to = [data[i][15] for i in range(len(data))]

data_dict = {
    'Rank': ranks,
    'ADP': adps,
    'Player': players,
    'FGM': fgm,
    'FGA': fga,
    'FG%': fgp,
    'FTM': ftm,
    'FTA': fta,
    'FT%': ftp,
    '3PM': _3pm,
    'PTS': pts,
    'REB': reb,
    'AST': ast,
    'STL': stl,
    'BLK': blk,
    'TO': to
}

df = pd.DataFrame(data_dict)

date = datetime.now().strftime('%Y-%m-%d')
output_path = f'sheets/fantasy_basketball_projections_{date}.csv'

df.to_csv(output_path, index=False)

print('Done!')