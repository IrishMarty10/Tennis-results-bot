competition = jsondata['events'][0]['tournament']['name']
# men's/women's singles/doubles
discipline = jsondata['events'][0]['stage']['id']
# format: bo3 / bo5
format = int(jsondata['events'][0]['totalSets'])

round = jsondata['events'][0]['round']['name']

# "PostEvent" / "MidEvent" / "PreEvent" / "Cancelled"
matchstatus = jsondata['events'][0]['status']

# Player Names
player_1 = jsondata['events'][0]['participants'][0]['players'][0]['name']['fullName']
player_2 = jsondata['events'][0]['participants'][1]['players'][0]['name']['fullName']

# "True" / "False"
player_1_win = jsondata['events'][0]['participants'][0]['matchWon']
player_2_win = jsondata['events'][0]['participants'][1]['matchWon']

# winner
winner = jsondata['events'][0]['matchSummary']['accessible'].split("(")[0]

# loser
accessibleinfo = jsondata['events'][0]['matchSummary']['accessible']
loser = (re.split('[()]|beat', accessibleinfo))[3]

# Set scores
player_1_sets_won = int(jsondata['events'][0]['participants'][0]['totalSetsWon'])
player_2_sets_won = int(jsondata['events'][0]['participants'][1]['totalSetsWon'])
total_sets_played = int(player_1_sets_won + player_2_sets_won)

player_1_set_scores = jsondata['events'][0]['participants'][0]['sets']
player_2_set_scores = jsondata['events'][0]['participants'][1]['sets']

player_1_set_1 = player_1_set_scores[0]['score']
player_1_set_2 = player_1_set_scores[1]['score']
player_1_set_3 = player_1_set_scores[2]['score']

try:
    tiebreak1 = player_1_set_scores[0]['tieBreak']
except KeyError:
    exit
try:
    tiebreak2 = player_1_set_scores[1]['tieBreak']
except KeyError:
    exit
try:
    tiebreak3 = player_1_set_scores[2]['tieBreak']
except KeyError:
    exit

player_2_set_1 = player_2_set_scores[0]['score']
player_2_set_2 = player_2_set_scores[1]['score']
player_2_set_3 = player_2_set_scores[2]['score']

try:
    tiebreak4 = player_2_set_scores[0]['tieBreak']
except KeyError:
    exit
try:
    tiebreak5 = player_2_set_scores[1]['tieBreak']
except KeyError:
    exit
try:
    tiebreak6 = player_2_set_scores[2]['tieBreak']
except KeyError:
    exit

try:
    set1_tiebreak = int(player_1_set_1) - int(player_2_set_1)
except ValueError:
    exit
try:
    set2_tiebreak = int(player_1_set_2) - int(player_2_set_2)
except ValueError:
    exit
try:
    set3_tiebreak = int(player_1_set_3) - int(player_2_set_3)
except ValueError:
    exit
