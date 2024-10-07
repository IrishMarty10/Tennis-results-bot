import requests
from datetime import datetime, timedelta, date
import json
import re

today = date.today()

# Today minus 1 month
earliest_valid_date = (date.today() - timedelta(days=30)).strftime('%Y-%m-%d')
# Today 
end_date = (date.today()).strftime('%Y-%m-%d')
# Tomorrow
latest_valid_date = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
# Today
start_date = (date.today()).strftime('%Y-%m-%d')

url = "https://web-cdn.api.bbci.co.uk/wc-poll-data/container/tennis-scores-schedule"

query_dict = {"earliestValidDate":earliest_valid_date,"endDate":end_date,"latestValidDate":latest_valid_date,"startDate":start_date}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
    "Accept": "application/json",
    "Accept-Language": "en-GB,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Referer": "https://www.bbc.co.uk/",
    "Origin": "https://www.bbc.co.uk",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "DNT": "1",
    "Sec-GPC": "1",
    "If-None-Match": "9276f8e24a275a562e0034f4929d537c7d7e60a1",
    "Priority": "u=4",
    "TE": "trailers"
}

response = requests.request("GET", url, headers=headers, params=query_dict)
jsondata = response.json()

for match in jsondata['events']:
    matchstatus = match['status']
    if matchstatus == "PostEvent":
        discipline = match['stage']['id']
        competition = match['tournament']['name']
        round = match['round']['name']
        winner = match['matchSummary']['accessible'].split("(")[0]
        accessibleinfo = match['matchSummary']['accessible']
        loser = (re.split('[()]|beat', accessibleinfo))[3]
        player_1_sets_won = int(match['participants'][0]['totalSetsWon'])
        player_2_sets_won = int(match['participants'][1]['totalSetsWon'])
        total_sets_played = int(player_1_sets_won + player_2_sets_won)
        player_1_win = match['participants'][0]['matchWon']
        player_2_win = match['participants'][1]['matchWon']
        player_1_set_scores = match['participants'][0]['sets']
        try:
            player_1_set_1 = player_1_set_scores[0]['score']
        except IndexError:
            exit
        try:
            player_1_set_2 = player_1_set_scores[1]['score']
        except IndexError:
            exit
        try:
            player_1_set_3 = player_1_set_scores[2]['score']
        except IndexError:
            exit
        try:
            tiebreak1 = player_1_set_scores[0]['tieBreak']
        except KeyError or IndexError:
            exit
        try:
            tiebreak2 = player_1_set_scores[1]['tieBreak']
        except KeyError or IndexError:
            exit
        try:
            tiebreak3 = player_1_set_scores[2]['tieBreak']
        except KeyError or IndexError:
            exit
        player_2_set_scores = match['participants'][1]['sets']
        try:
            player_2_set_1 = player_2_set_scores[0]['score']
        except IndexError:
            exit
        try:
            player_2_set_2 = player_2_set_scores[1]['score']
        except IndexError:
            exit
        try:
            player_2_set_3 = player_2_set_scores[2]['score']
        except IndexError:
            exit
        try:
            tiebreak4 = player_2_set_scores[0]['tieBreak']
        except KeyError or IndexError:
            exit
        try:
            tiebreak5 = player_2_set_scores[1]['tieBreak']
        except KeyError or IndexError:
            exit
        try:
            tiebreak6 = player_2_set_scores[2]['tieBreak']
        except KeyError or IndexError:
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

    # Player retirement
        # First set retirement
        # Second set retirement
        # Third set retirement

    # Two set match
        if total_sets_played == 2:
        # No tiebreaks
            # Player_1 wins both sets with no tiebreaks
            if player_1_win and matchstatus == "PostEvent" and (discipline == "mens-singles" or discipline == "womens-singles") and (set1_tiebreak < -1 or set1_tiebreak > 1) and (set2_tiebreak < -1 or set2_tiebreak > 1):
                print(competition, " ", round, " ", '|', " ", winner, 'd.', loser, player_1_set_1, "-", player_2_set_1, " ", player_1_set_2, "-", player_2_set_2, sep = '')
            # Player_2 wins both sets with no tiebreaks
            elif player_2_win and matchstatus == "PostEvent" and (discipline == "mens-singles" or discipline == "womens-singles") and (set1_tiebreak < -1 or set1_tiebreak > 1) and (set2_tiebreak < -1 or set2_tiebreak > 1):
                print(competition, " ", round, " ", '|', " ", winner, 'd.', loser, player_2_set_1, "-", player_1_set_1, " ", player_2_set_2, "-", player_1_set_2, sep = '')

        # First set tiebreak only
            # Player_1 wins first set tiebreak and wins match
            elif player_1_win and matchstatus == "PostEvent" and (discipline == "mens-singles" or discipline == "womens-singles") and set1_tiebreak == 1 and (set2_tiebreak > 1 or set2_tiebreak < -1):
                try:
                    print(competition, " ", round, " ", '|', " ", winner, 'd.', loser, player_1_set_1, "-", player_2_set_1, "(", tiebreak4, ")", " ", player_1_set_2, "-", player_2_set_2, " ", sep = '')
                except NameError:
                    exit
            # Player_2 wins first set tiebreak and wins match
            elif player_2_win and matchstatus == "PostEvent" and (discipline == "mens-singles" or discipline == "womens-singles") and set1_tiebreak == -1 and (set2_tiebreak > 1 or set2_tiebreak < -1):
                try:
                    print(competition, " ", round, " ", '|', " ", winner, 'd.', loser, player_2_set_1, "-", player_1_set_1, "(", tiebreak1, ")", " ", player_2_set_2, "-", player_1_set_2, sep = '')
                except NameError:
                    exit
        # Second set tiebreak only
            # Player_1 wins second set tiebreak and wins match
            elif player_1_win and matchstatus == "PostEvent" and (discipline == "mens-singles" or discipline == "womens-singles") and set2_tiebreak == 1 and (set1_tiebreak < -1 or set1_tiebreak > 1):
                try:
                    print(competition, " ", round, " ", '|', " ", winner, 'd.', loser, player_1_set_1, "-", player_2_set_1, " ", player_1_set_2, "-", player_2_set_2, "(", tiebreak5, ")", sep = '')
                except NameError:
                    exit
            # Player_2 wins second set tiebreak and wins match
            elif player_2_win and matchstatus == "PostEvent" and (discipline == "mens-singles" or discipline == "womens-singles") and set2_tiebreak == -1 and (set1_tiebreak < -1 or set1_tiebreak > 1):
                try:
                    print(competition, " ", round, " ", '|', " ", winner, 'd.', loser, player_2_set_1, "-", player_1_set_1, " ", player_2_set_2, "-", player_1_set_2, "(", tiebreak2, ")", sep = '')
                except NameError:
                    exit
        # First and second set tiebreak
            # Player_1 wins first and second set tiebreak
            elif player_1_win and matchstatus == "PostEvent" and (discipline == "mens-singles" or discipline == "womens-singles") and set1_tiebreak == 1 and set2_tiebreak == 1:
                try:
                    print(competition, " ", round, " ", '|', " ", winner, 'd.', loser, player_1_set_1, "-", player_2_set_1, "(", tiebreak4, ")", " ", player_1_set_2, "-", player_2_set_2, "(", tiebreak5, ")", sep = '')
                except NameError:
                    exit
            # Player_2 wins first and second set tiebreak
            elif player_2_win and matchstatus == "PostEvent" and (discipline == "mens-singles" or discipline == "womens-singles") and set1_tiebreak == -1 and set2_tiebreak == -1:
                try:
                    print(competition, " ", round, " ", '|', " ", winner, 'd.', loser, player_2_set_1, "-", player_1_set_1, "(", tiebreak1, ")", " ", player_2_set_2, "-", player_1_set_2, "(", tiebreak2, ")", sep = '')
                except NameError:
                    exit

        # # First and second set tiebreak
        #     # Player_1 loses first set tiebreak, wins second set tiebreak, and wins third non-tiebreak set
        #     elif player_1_win and matchstatus == "PostEvent" and (discipline == "mens-singles" or discipline == "womens-singles") and set1_tiebreak == -1 and set2_tiebreak == 1 and (set3_tiebreak < -1 or set3_tiebreak > 1):
        #         try:
        #             print(competition, " ", round, " ", '|', " ", winner, 'd.', loser, player_1_set_1, "-", player_2_set_1, "(", tiebreak1, ")", " ", player_1_set_2, "-", player_2_set_2, "(", tiebreak5, ")", " ", player_1_set_3, "-", player_2_set_3, sep = '')
        #         except NameError:
        #             exit
        #     # Player_2 loses first set tiebreak, wins second set tiebreak, and wins third non-tiebreak set
        #     elif player_2_win and matchstatus == "PostEvent" and (discipline == "mens-singles" or discipline == "womens-singles") and set1_tiebreak == -1:
                try:
                    print(competition, " ", round, " ", '|', " ", winner, 'd.', loser, player_2_set_1, "-", player_1_set_1, "(", tiebreak4, ")", " ", player_2_set_2, "-", player_1_set_2, "(", tiebreak2, ")", " ", player_2_set_3, "-", player_1_set_3, sep = '')
                except NameError:
                    exit


    # Three set match    
        elif total_sets_played == 3:
        # No tiebreaks
            # Player_1 wins
            if player_1_win and matchstatus == "PostEvent" and (discipline == "mens-singles" or discipline == "womens-singles") and (set1_tiebreak > 1 or set1_tiebreak < -1) and (set2_tiebreak > 1 or set2_tiebreak < -1) and (set3_tiebreak > 1 or set3_tiebreak < -1):
                print(competition, " ", round, " ", '|', " ", winner, 'd.', loser, player_1_set_1, "-", player_2_set_1, " ", player_1_set_2, "-", player_2_set_2, " ", player_1_set_3, "-", player_2_set_3, sep = '')
            # Player_2 wins
            elif player_1_win and matchstatus == "PostEvent" and (discipline == "mens-singles" or discipline == "womens-singles") and (set1_tiebreak > 1 or set1_tiebreak < -1) and (set2_tiebreak > 1 or set2_tiebreak < -1) and (set3_tiebreak > 1 or set3_tiebreak < -1):
                print(competition, " ", round, " ", '|', " ", winner, 'd.', loser, player_2_set_1, "-", player_1_set_1, " ", player_2_set_2, "-", player_1_set_2, " ", player_2_set_3, "-", player_1_set_3, sep = '')
        # First set tiebreak only
            # Player_1 wins first set tiebreak and wins match
            elif player_1_win and matchstatus == "PostEvent" and (discipline == "mens-singles" or discipline == "womens-singles") and set1_tiebreak == 1 and (set2_tiebreak > 1 or set2_tiebreak < -1) and (set3_tiebreak > 1 or set3_tiebreak < -1):
                try:
                    print(competition, " ", round, " ", '|', " ", winner, 'd.', loser, player_1_set_1, "-", player_2_set_1, "(", tiebreak4, ")", " ", player_1_set_2, "-", player_2_set_2, " ", player_1_set_3, "-", player_2_set_3, sep = '')
                except NameError:
                    exit
            # Player_1 loses first set tiebreak and wins match
            elif player_1_win and matchstatus == "PostEvent" and (discipline == "mens-singles" or discipline == "womens-singles") and set1_tiebreak == -1 and (set2_tiebreak > 1 or set2_tiebreak < -1) and (set3_tiebreak > 1 or set3_tiebreak < -1):
                try:
                    print(competition, " ", round, " ", '|', " ", winner, 'd.', loser, player_1_set_1, "-", player_2_set_1, "(", tiebreak1, ")", " ", player_1_set_2, "-", player_2_set_2, " ", player_1_set_3, "-", player_2_set_3, sep = '')
                except NameError:
                    exit
            # Player_2 wins first set tiebreak and wins match
            elif player_2_win and matchstatus == "PostEvent" and (discipline == "mens-singles" or discipline == "womens-singles") and set1_tiebreak == -1 and (set2_tiebreak > 1 or set2_tiebreak < -1) and (set3_tiebreak > 1 or set3_tiebreak < -1):
                try:
                    print(competition, " ", round, " ", '|', " ", winner, 'd.', loser, player_2_set_1, "-", player_1_set_1, "(", tiebreak4, ")", " ", player_2_set_2, "-", player_1_set_2, " ", player_2_set_3, "-", player_1_set_3, sep = '')
                except NameError:
                    exit
            # Player_2 loses first set tiebreak and wins match
            elif player_2_win and matchstatus == "PostEvent" and (discipline == "mens-singles" or discipline == "womens-singles") and set1_tiebreak == 1 and (set2_tiebreak > 1 or set2_tiebreak < -1) and (set3_tiebreak > 1 or set3_tiebreak < -1):
                try:
                    print(competition, " ", round, " ", '|', " ", winner, 'd.', loser, player_2_set_1, "-", player_1_set_1, "(", tiebreak4, ")", " ", player_2_set_2, "-", player_1_set_2, " ", player_2_set_3, "-", player_1_set_3, sep = '')
                except NameError:
                    exit
        # Second set tiebreak only
            # Player_1 wins second set tiebreak and wins match
            elif player_1_win and matchstatus == "PostEvent" and (discipline == "mens-singles" or discipline == "womens-singles") and set2_tiebreak == 1 and (set1_tiebreak < -1 or set1_tiebreak > 1) and (set3_tiebreak < -1 or set3_tiebreak > 1):
                try:
                    print(competition, " ", round, " ", '|', " ", winner, 'd.', loser, player_1_set_1, "-", player_2_set_1, " ", player_1_set_2, "-", player_2_set_2, "(", tiebreak5, ")", " ", player_1_set_3, "-", player_2_set_3, sep = '')
                except NameError:
                    exit
            # Player_1 loses second set tiebreak and wins match
            elif player_1_win and matchstatus == "PostEvent" and (discipline == "mens-singles" or discipline == "womens-singles") and set2_tiebreak == -1 and (set1_tiebreak < -1 or set1_tiebreak > 1) and (set3_tiebreak < -1 or set3_tiebreak > 1):
                try:
                    print(competition, " ", round, " ", '|', " ", winner, 'd.', loser, player_1_set_1, "-", player_2_set_1, " ", player_1_set_2, "-", player_2_set_2, "(", tiebreak2, ")", " ", player_1_set_3, "-", player_2_set_3, sep = '')
                except NameError:
                    exit
            # Player_2 wins second set tiebreak and wins match
            elif player_2_win and matchstatus == "PostEvent" and (discipline == "mens-singles" or discipline == "womens-singles") and set2_tiebreak == -1 and (set1_tiebreak < -1 or set1_tiebreak > 1) and (set3_tiebreak < -1 or set3_tiebreak > 1):
                try:
                    print(competition, " ", round, " ", '|', " ", winner, 'd.', loser, player_2_set_1, "-", player_1_set_1, " ", player_2_set_2, "-", player_1_set_2, "(", tiebreak2, ")", " ", player_2_set_3, "-", player_1_set_3, sep = '')
                except NameError:
                    exit
            # Player_2 loses second set tiebreak and wins match
            elif player_2_win and matchstatus == "PostEvent" and (discipline == "mens-singles" or discipline == "womens-singles") and set2_tiebreak == 1 and (set1_tiebreak < -1 or set1_tiebreak > 1) and (set3_tiebreak < -1 or set3_tiebreak > 1):
                try:
                    print(competition, " ", round, " ", '|', " ", winner, 'd.', loser, player_2_set_1, "-", player_1_set_1, " ", player_2_set_2, "-", player_1_set_2, "(", tiebreak5, ")", " ", player_2_set_3, "-", player_1_set_3, sep = '')
                except NameError:
                    exit
        # Third set tiebreak only
            # Player_1 wins third set tiebreak and wins match
            elif player_1_win and matchstatus == "PostEvent" and (discipline == "mens-singles" or discipline == "womens-singles") and set3_tiebreak == 1 and (set1_tiebreak < -1 or set1_tiebreak > 1) and (set2_tiebreak < -1 or set2_tiebreak > 1):
                try:
                    print(competition, " ", round, " ", '|', " ", winner, 'd.', loser, player_1_set_1, "-", player_2_set_1, " ", player_1_set_2, "-", player_2_set_2, " ", player_1_set_3, "-", player_2_set_3, "(", tiebreak6, ")", sep = '')
                except NameError:
                    exit
            # Player_2 wins third set tiebreak and wins match
            elif player_2_win and matchstatus == "PostEvent" and (discipline == "mens-singles" or discipline == "womens-singles") and set3_tiebreak == -1 and (set1_tiebreak < -1 or set1_tiebreak > 1) and (set2_tiebreak < -1 or set2_tiebreak > 1):
                try:
                    print(competition, " ", round, " ", '|', " ", winner, 'd.', loser, player_2_set_1, "-", player_1_set_1, " ", player_2_set_2, "-", player_1_set_2, " ", player_2_set_3, "-", player_1_set_3, "(", tiebreak3, ")", sep = '')
                except NameError:
                    exit
        # First and second set tiebreak
            # Player_1 wins first set tiebreak, Player_2 wins second set tiebreak, Player_1 wins match
            elif player_1_win and matchstatus == "PostEvent" and (discipline == "mens-singles" or discipline == "womens-singles") and set1_tiebreak == 1 and set2_tiebreak == -1 and (set3_tiebreak > 1 or set3_tiebreak < -1):
                try:
                    print(competition, " ", round, " ", '|', " ", winner, 'd.', loser, player_1_set_1, "-", player_2_set_1, "(", tiebreak4, ")", " ", player_1_set_2, "-", player_2_set_2, "(", tiebreak2, ")", " ", player_1_set_3, "-", player_2_set_3, sep = '')
                except NameError:
                    exit
            # Player_1 wins first set tiebreak, Player_2 wins second set tiebreak, Player_2 wins match
            elif player_2_win and matchstatus == "PostEvent" and (discipline == "mens-singles" or discipline == "womens-singles") and set1_tiebreak == 1 and set2_tiebreak == -1 and (set3_tiebreak > 1 or set3_tiebreak < -1):
                try:
                    print(competition, " ", round, " ", '|', " ", winner, 'd.', loser, player_2_set_1, "-", player_1_set_1, "(", tiebreak4, ")", " ", player_2_set_2, "-", player_1_set_2, "(", tiebreak2, ")", " ", player_2_set_3, "-", player_1_set_3, sep = '')
                except NameError:
                    exit
            # Player_2 wins first set tiebreak, Player_1 wins second set tiebreak, Player_2 wins match
            elif player_2_win and matchstatus == "PostEvent" and (discipline == "mens-singles" or discipline == "womens-singles") and set1_tiebreak == -1 and set2_tiebreak == 1 and (set3_tiebreak > 1 or set3_tiebreak < -1):
                try:
                    print(competition, " ", round, " ", '|', " ", winner, 'd.', loser, player_2_set_1, "-", player_1_set_1, "(", tiebreak1, ")", " ", player_2_set_2, "-", player_1_set_2, "(", tiebreak5, ")", " ", player_2_set_3, "-", player_1_set_3, sep = '')
                except NameError:
                    exit
            # Player_2 wins first set tiebreak, Player_1 wins second set tiebreak, Player_1 wins match
            elif player_1_win and matchstatus == "PostEvent" and (discipline == "mens-singles" or discipline == "womens-singles") and set1_tiebreak == -1 and set2_tiebreak == 1 and (set3_tiebreak > 1 or set3_tiebreak < -1):
                try:
                    print(competition, " ", round, " ", '|', " ", winner, 'd.', loser, player_1_set_1, "-", player_2_set_1, "(", tiebreak1, ")", " ", player_1_set_2, "-", player_2_set_2, "(", tiebreak5, ")", " ", player_1_set_3, "-", player_2_set_3, sep = '')
                except NameError:
                    exit
        # First and third set tiebreak
            # Player_1 wins first set tiebreak, Player_1 wins third set tiebreak and wins match
            elif player_1_win and matchstatus == "PostEvent" and (discipline == "mens-singles" or discipline == "womens-singles") and set1_tiebreak == 1 and set3_tiebreak == 1 and (set2_tiebreak > 1 or set2_tiebreak < -1):
                try:
                    print(competition, " ", round, " ", '|', " ", winner, 'd.', loser, player_1_set_1, "-", player_2_set_1, "(", tiebreak4, ")", " ", player_1_set_2, "-", player_2_set_2, " ", player_1_set_3, "-", player_2_set_3, "(", tiebreak6, ")", sep = '')
                except NameError:
                    exit
            # Player_1 loses first set tiebreak, Player_1 wins second set and third set tiebreak, and wins match
            elif player_1_win and matchstatus == "PostEvent" and (discipline == "mens-singles" or discipline == "womens-singles") and set1_tiebreak == -1 and set3_tiebreak == 1 and (set2_tiebreak > 1 or set2_tiebreak < -1):
                try:
                    print(competition, " ", round, " ", '|', " ", winner, 'd.', loser, player_1_set_1, "-", player_2_set_1, "(", tiebreak1, ")", " ", player_1_set_2, "-", player_2_set_2, " ", player_1_set_3, "-", player_2_set_3, "(", tiebreak6, ")", sep = '')
                except NameError:
                    exit
            # Player_2 wins first set tiebreak, Player_2 wins third set tiebreak and wins match
            elif player_2_win and matchstatus == "PostEvent" and (discipline == "mens-singles" or discipline == "womens-singles") and set1_tiebreak == -1 and set3_tiebreak == -1 and (set2_tiebreak > 1 or set2_tiebreak < -1):
                try:
                    print(competition, " ", round, " ", '|', " ", winner, 'd.', loser, player_2_set_1, "-", player_1_set_1, "(", tiebreak1, ")", " ", player_2_set_2, "-", player_1_set_2, " ", player_2_set_3, "-", player_1_set_3, "(", tiebreak3, ")", sep = '')
                except NameError:
                    exit
            # Player_2 loses first set tiebreak, Player_2 wins second set and third set tiebreak, and wins match
            elif player_2_win and matchstatus == "PostEvent" and (discipline == "mens-singles" or discipline == "womens-singles") and set1_tiebreak == 1 and set3_tiebreak == -1 and (set2_tiebreak > 1 or set2_tiebreak < -1):
                try:
                    print(competition, " ", round, " ", '|', " ", winner, 'd.', loser, player_2_set_1, "-", player_1_set_1, "(", tiebreak4, ")", " ", player_2_set_2, "-", player_1_set_2, " ", player_2_set_3, "-", player_1_set_3, "(", tiebreak3, ")", sep = '')
                except NameError:
                    exit
        # Second and third set tiebreak
            # Player_1 wins second and third set tiebreak, and wins match
            elif player_1_win and matchstatus == "PostEvent" and (discipline == "mens-singles" or discipline == "womens-singles") and set2_tiebreak == 1 and set3_tiebreak == 1 and (set1_tiebreak > 1 or set1_tiebreak < -1):
                try:
                    print(competition, " ", round, " ", '|', " ", winner, 'd.', loser, player_1_set_1, "-", player_2_set_1, " ", player_1_set_2, "-", player_2_set_2, "(", tiebreak5, ")", " ", player_1_set_3, "-", player_2_set_3, "(", tiebreak6, ")", sep = '')
                except NameError:
                    exit
            # Player_1 wins first set, loses second set tiebreak, wins third set tiebreak, and wins match
            elif player_1_win and matchstatus == "PostEvent" and (discipline == "mens-singles" or discipline == "womens-singles") and set2_tiebreak == -1 and set3_tiebreak == 1 and (set1_tiebreak > 1 or set1_tiebreak < -1):
                try:
                    print(competition, " ", round, " ", '|', " ", winner, 'd.', loser, player_1_set_1, "-", player_2_set_1, " ", player_1_set_2, "-", player_2_set_2, "(", tiebreak2, ")", " ", player_1_set_3, "-", player_2_set_3, "(", tiebreak6, ")", sep = '')
                except NameError:
                    exit
            # Player_2 wins second and third set tiebreak, and wins match
            elif player_2_win and matchstatus == "PostEvent" and (discipline == "mens-singles" or discipline == "womens-singles") and set2_tiebreak == -1 and set3_tiebreak == -1 and (set1_tiebreak > 1 or set1_tiebreak < -1):
                try:
                    print(competition, " ", round, " ", '|', " ", winner, 'd.', loser, player_2_set_1, "-", player_1_set_1, " ", player_2_set_2, "-", player_1_set_2, "(", tiebreak2, ")", " ", player_2_set_3, "-", player_1_set_3, "(", tiebreak3, ")", sep = '')
                except NameError:
                    exit
            # Player_2 wins first set, loses second set tiebreak, and wins match
            elif player_2_win and matchstatus == "PostEvent" and (discipline == "mens-singles" or discipline == "womens-singles") and set2_tiebreak == 1 and set3_tiebreak == -1 and (set1_tiebreak > 1 or set1_tiebreak < -1):
                try:
                    print(competition, " ", round, " ", '|', " ", winner, 'd.', loser, player_2_set_1, "-", player_1_set_1, " ", player_2_set_2, "-", player_1_set_2, "(", tiebreak5, ")", " ", player_2_set_3, "-", player_1_set_3, "(", tiebreak3, ")", sep = '')
                except NameError:
                    exit
        # First, Second and Third set tiebreak
            # Player_1 wins first set tiebreak, Player_2 wins second set tiebreak, Player_1 wins third set tiebreak and match
            elif player_1_win and matchstatus == "PostEvent" and (discipline == "mens-singles" or discipline == "womens-singles") and set1_tiebreak == 1 and set2_tiebreak == -1 and set3_tiebreak == 1:
                try:
                    print(competition, " ", round, " ", '|', " ", winner, 'd.', loser, player_1_set_1, "-", player_2_set_1, "(", tiebreak4, ")", " ", player_1_set_2, "-", player_2_set_2, "(", tiebreak2, ")", " ", player_1_set_3, "-", player_2_set_3, "(", tiebreak6, ")", sep = '')
                except NameError:
                    exit
            # Player_1 wins first set tiebreak, Player_2 wins second set tiebreak, Player_2 wins third set tiebreak and match
            elif player_2_win and matchstatus == "PostEvent" and (discipline == "mens-singles" or discipline == "womens-singles") and set1_tiebreak == 1 and set2_tiebreak == -1 and set3_tiebreak == -1:
                try:
                    print(competition, " ", round, " ", '|', " ", winner, 'd.', loser, player_2_set_1, "-", player_1_set_1, "(", tiebreak4, ")", " ", player_2_set_2, "-", player_1_set_2, "(", tiebreak2, ")", " ", player_2_set_3, "-", player_1_set_3, "(", tiebreak3, ")", sep = '')
                except NameError:
                    exit
            # Player_2 wins first set tiebreak, Player_1 wins second set tiebreak, Player_1 wins third set tiebreak and match
            elif player_1_win and matchstatus == "PostEvent" and (discipline == "mens-singles" or discipline == "womens-singles") and set1_tiebreak == -1 and set2_tiebreak == 1 and set3_tiebreak == -1:
                try:
                    print(competition, " ", round, " ", '|', " ", winner, 'd.', loser, player_1_set_1, "-", player_2_set_1, "(", tiebreak1, ")", " ", player_1_set_2, "-", player_2_set_2, "(", tiebreak5, ")", " ", player_1_set_3, "-", player_2_set_3, "(", tiebreak6, ")", sep = '')
                except NameError:
                    exit
            # Player_2 wins first set tiebreak, Player_1 wins second set tiebreak, Player_2 wins third set tiebreak and match
            elif player_2_win and matchstatus == "PostEvent" and (discipline == "mens-singles" or discipline == "womens-singles") and set1_tiebreak == -1 and set2_tiebreak == 1 and set3_tiebreak == -1:
                try:
                    print(competition, " ", round, " ", '|', " ", winner, 'd.', loser, player_2_set_1, "-", player_1_set_1, "(", tiebreak1, ")", " ", player_2_set_2, "-", player_1_set_2, "(", tiebreak5, ")", " ", player_2_set_3, "-", player_1_set_3, "(", tiebreak3, ")", sep = '')
                except NameError:
                    exit
    else:
        exit

