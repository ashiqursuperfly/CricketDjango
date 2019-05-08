import csv
from datetime import datetime
import json
import pathlib
from bs4 import BeautifulSoup
import urllib3

import requests

# api-endpoint
URL = "https://www.cricbuzz.com/match-api/livematches.json"
URL_FOR_SCORECARD = "https://www.cricbuzz.com/api/html/cricket-scorecard/"


def create_directory_if_not_exist(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def check_if_match_completed(match_data):
    state = match_data.get("state")
    if state == "mom":
        return True
    else:
        return False


def init_players_to_csv(data_dict, file_name):
    path_name = "api_data/"
    create_directory_if_not_exist(path_name)
    f = csv.writer(open(path_name + file_name + ".csv", "w", newline=''))
    # Write CSV Header, If you dont need that, remove this line
    f.writerow(["player_id", "full_name", "nationality", "bat_style", "bowl_style", "speciality"])
    for match_id, match in data_dict.get('matches').items():
        if not check_if_match_completed(match):
            continue
        squad_data = list(dict(match.get("team1")).get("squad")) + list(dict(match.get("team1")).get("squad_bench"))
        squad_1 = list()
        for s in squad_data:
            squad_1.insert(0, str(s))
        for x in dict(match).get('players'):
            category = match.get("series").get("category")
            if category == 'International':
                category = str(match.get("team1").get("name")) if str(x.get("id")) in squad_1 else str(
                    match.get("team2").get("name"))
            else:
                category = ""

            f.writerow([x.get("id"), x.get("f_name"),
                        category, x.get("bat_style"),
                        x.get("bowl_style"), x.get("speciality")])


def init_teams_to_csv(data_dict, file_name):
    path_name = "api_data/"
    create_directory_if_not_exist(path_name)
    f = csv.writer(open(path_name + file_name + ".csv", "w", newline=''))
    f.writerow(["team_id", "team_name", "league"])
    for key, match in data_dict.get('matches').items():
        if not check_if_match_completed(match):
            continue

        league = str(dict(dict(match).get('series')).get('category'))
        if league == 'League':
            league = str(dict(dict(match).get('series')).get('name'))

        f.writerow([str(dict(dict(match).get('team1')).get('id')) + "",
                    str(dict(dict(match).get('team1')).get('name')) + "",
                    league + ""])

        f.writerow([str(dict(dict(match).get('team2')).get('id')) + "",
                    str(dict(dict(match).get('team2')).get('name')) + "",
                    league + ""])


def init_players_plays_for_teams_to_csv(data_dict, file_name):
    path_name = "api_data/"
    create_directory_if_not_exist(path_name)
    f = csv.writer(open(path_name + file_name + ".csv", "w", newline=''))
    f.writerow(["team_id", "player_id"])
    for key, match in data_dict.get('matches').items():
        if not check_if_match_completed(match):
            continue
        squad_1 = list(dict(match.get("team1")).get("squad")) + list(dict(match.get("team1")).get("squad_bench"))
        for p_id in squad_1:
            f.writerow([dict(dict(match).get('team1')).get('id'), p_id])

        squad_2 = list(dict(match.get("team2")).get("squad")) + list(dict(match.get("team2")).get("squad_bench"))
        for p_id in squad_2:
            f.writerow([dict(dict(match).get('team2')).get('id'), p_id])


def init_umpires_to_csv(data_dict, file_name):
    path_name = "api_data/"
    create_directory_if_not_exist(path_name)
    f = csv.writer(open(path_name + file_name + ".csv", "w", newline=''))

    # Write CSV Header, If you dont need that, remove this line
    f.writerow(["umpire_id", "full_name", "nationality"])

    for match_id, match in data_dict.get('matches').items():

        if not check_if_match_completed(match):
            continue
        # print(match_id)
        for k, x in dict(match).get('official').items():
            f.writerow([x.get("id"), x.get("name"), x.get("country")])


def init_umpires_conducts_matches_to_csv(data_dict, file_name):
    path_name = "api_data/"
    create_directory_if_not_exist(path_name)
    f = csv.writer(open(path_name + file_name + ".csv", "w", newline=''))

    # Write CSV Header, If you dont need that, remove this line
    f.writerow(["match_id", "umpire_id", "umpiring_role"])

    for match_id, match in data_dict.get('matches').items():
        if not check_if_match_completed(match):
            continue
        print(match_id)
        for k, x in dict(match).get('official').items():
            f.writerow([match_id, x.get("id"), k])


def init_series_to_csv(data_dict, file_name):
    path_name = "api_data/"
    create_directory_if_not_exist(path_name)

    series_writer = csv.writer(open(path_name + file_name + ".csv", "w", newline=""))

    path_name_2 = "api_data/"
    create_directory_if_not_exist(path_name_2)

    team_series_relation_writer = csv.writer(
        open(path_name_2 + "teams_plays_in_" + file_name + ".csv", "w", newline=""))

    # Write CSV Header, If you dont need that, remove this line
    series_writer.writerow(["series_id", "series_name", "mots", "winner"])
    team_series_relation_writer.writerow(["team_id", "series_id"])

    for match_key, match_value in data_dict.get('matches').items():
        if not check_if_match_completed(match_value):
            continue
        series_value = match_value.get('series')
        mots = match_value.get("mos")
        if mots == None:
            mots = ''
        else : mots = match_value.get("mos")[0]
        # print(str(mots) + 'man of the series')
        series_writer.writerow(
            [series_value.get('id'), series_value.get('name'), mots, match_value.get('winning_team_id')])
        team_series_relation_writer.writerow([match_value.get('team1').get('id'), series_value.get('id')])
        team_series_relation_writer.writerow([match_value.get('team2').get('id'), series_value.get('id')])


def init_match_to_csv(data_dict, file_name):
    path_name = "api_data/"
    create_directory_if_not_exist(path_name)

    match_writer = csv.writer(open(path_name + file_name + ".csv", "w", newline=""))

    # Write CSV Header, If you dont need that, remove this line
    match_writer.writerow(["match_id", "match_type", "team1Id", "team2Id", "captain_1",
                           "captain_2", "score_1", "score_2", "score 3", "score 4", "venue",
                           "stadium_name", "date", "winner", "motm", "series_id"])

    for match_key, match_value in data_dict.get('matches').items():

        if not check_if_match_completed(match_value):
            continue

        print(match_key)
        squad_data = list(dict(match_value.get("team1")).get("squad")) + list(
            dict(match_value.get("team1")).get("squad_bench"))

        squad_1 = list()
        for s in squad_data:
            squad_1.insert(0, str(s))

        match_id = match_key
        match_type = match_value.get("type")
        unix_time = int(match_value.get("start_time"))
        date = datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d')
        captain1 = ""
        captain2 = ""
        stadium_name = match_value.get("venue").get("name")
        venue = match_value.get("venue").get("location")
        team1 = match_value.get("team1").get("id")
        team2 = match_value.get("team2").get("id")
        (score1, score2, score3, score4) = init_match_performance_data_wtests(match_key, team1, team2, match_type)
        winning_team = match_value.get("winning_team_id")
        motm = list(match_value.get("mom"))[0]
        series_id = match_value.get("series").get("id")
        for x in match_value.get("players"):
            if x.get("role") == "(c)" or x.get("role") == "(c & wk)":
                if x.get("id") in squad_1:
                    captain1 = x.get("id")
                else:
                    captain2 = x.get("id")

        match_writer.writerow(
            [match_id, match_type, team1, team2, captain1, captain2, score1, score2, score3, score4, venue,
             stadium_name, date, winning_team, motm,
             series_id])


def init_all_match_data(json_data):
    init_match_to_csv(dict(json_data), "match")
    init_players_to_csv(dict(json_data), "players")
    init_teams_to_csv(dict(json_data), "teams")
    init_players_plays_for_teams_to_csv(dict(json_data), "player_plays_for_teams")
    init_umpires_to_csv(dict(json_data), "umpires")
    init_umpires_conducts_matches_to_csv(dict(json_data), "umpire_conducts_match")
    init_series_to_csv(dict(json_data), "series")



class PlayerPerformanceModel:
    def __init__(self, name, player_id):
        self.name = name
        self.player_id = player_id
        self.runs_scored = 0
        self.balls_batted = 0
        self.fours_scored = 0
        self.sixes_scored = 0
        self.overs_bowled = 0
        self.maidens = 0
        self.runs_conceded = 0
        self.wickets_taken = 0
        self.no_balls = 0
        self.wides = 0
        self.final_out_condition = "Did not bat"


def create_player_performance_model(player_link_internal):
    splittedArray = str(player_link_internal).split('/')

    return PlayerPerformanceModel(splittedArray[3], splittedArray[2])


def create_players_dictionary(team_batting_data_soup):
    team_dict = dict()

    for link in team_batting_data_soup.find_all('a'):
        player_model = create_player_performance_model(link.get('href'))
        # print(link.get('href'))
        team_dict[player_model.player_id] = player_model
    return team_dict


# Note that parser does not work for test matches. Nor will it ever work. I am done with this  :)
def init_match_performance_data(match_id, team1_id, team2_id):
    full_url = URL_FOR_SCORECARD + str(match_id)
    # print(full_url)

    path_name = "api_data/match_performance_data/"
    create_directory_if_not_exist(path_name)

    match_performance_writer = csv.writer(open(path_name + str(match_id) + ".csv", "w", newline=""))

    match_performance_writer.writerow(
        ["match_id", "team_id", "player_id", "runs_scored", "balls_batted", "fours_scored", "sixes_scored",
         "overs_bowled", "maidens",
         "runs_conceded", "wickets_taken", "no_balls", "wides", "final_out_condition"])

    http = urllib3.PoolManager()
    response = http.request('GET', full_url)
    soup = BeautifulSoup(response.data, features="html.parser")

    innings1Tag = soup.findAll('div', {"id": 'innings_1'})[0]
    innings2Tag = soup.findAll('div', {"id": 'innings_2'})[0]

    # cb-col cb-col-100 cb-ltst-wgt-hdr  -> cb-col cb-col-100 cb-scrd-itms <space ase ekta btw

    team1_batting_data = innings1Tag.findAll('div', {"class": "cb-col cb-col-100 cb-ltst-wgt-hdr"})[0]
    team2_bowling_data = innings1Tag.findAll('div', {"class": "cb-col cb-col-100 cb-ltst-wgt-hdr"})[1]

    team2_batting_data = innings2Tag.findAll('div', {"class": "cb-col cb-col-100 cb-ltst-wgt-hdr"})[0]
    team1_bowling_data = innings2Tag.findAll('div', {"class": "cb-col cb-col-100 cb-ltst-wgt-hdr"})[1]

    team1dictionary = create_players_dictionary(team1_batting_data)
    team2dictionary = create_players_dictionary(team2_batting_data)

    # print(len(team1dictionary))

    # print(team1_batting_data.prettify())

    # class="cb-col cb-col-100 cb-scrd-itms"

    team1_batting_data_array = team1_batting_data.findAll('div', {"class": "cb-col cb-col-100 cb-scrd-itms"})
    team2_batting_data_array = team2_batting_data.findAll('div', {"class": "cb-col cb-col-100 cb-scrd-itms"})
    team1_bowling_data_array = team1_bowling_data.findAll('div', {"class": "cb-col cb-col-100 cb-scrd-itms"})
    team2_bowling_data_array = team2_bowling_data.findAll('div', {"class": "cb-col cb-col-100 cb-scrd-itms"})

    # print(team1_batting_data_array[0].prettify())

    # children = team1_batting_data_array[0].contents
    # print(children[5])

    total_runs_team1 = 0
    total_runs_team2 = 0

    for playerdata in team1_batting_data_array:

        all_text = playerdata.get_text()
        if "Extras" in all_text or "Did not Bat" in all_text:
            continue
        if "Total" in all_text:
            total_runs_team1 = int(playerdata.contents[3].string)
            # print(total_runs_team1)
            continue

        playerdatacontents = playerdata.contents
        temp_model = create_player_performance_model(playerdatacontents[1].a.get('href'))
        player_model = team1dictionary.get(temp_model.player_id)

        player_model.final_out_condition = playerdatacontents[3].span.string
        player_model.runs_scored = int(playerdatacontents[5].string)
        player_model.balls_batted = int(playerdatacontents[7].string)
        player_model.fours_scored = int(playerdatacontents[9].string)
        player_model.sixes_scored = int(playerdatacontents[11].string)

    for playerdata in team2_batting_data_array:

        all_text = playerdata.get_text()
        if "Extras" in all_text or "Did not Bat" in all_text:
            continue
        if "Total" in all_text:
            total_runs_team2 = int(playerdata.contents[3].string)
            # print(total_runs_team1)
            continue

        playerdatacontents = playerdata.contents
        temp_model = create_player_performance_model(playerdatacontents[1].a.get('href'))
        player_model = team2dictionary.get(temp_model.player_id)

        player_model.final_out_condition = playerdatacontents[3].span.string
        player_model.runs_scored = int(playerdatacontents[5].string)
        player_model.balls_batted = int(playerdatacontents[7].string)
        player_model.fours_scored = int(playerdatacontents[9].string)
        player_model.sixes_scored = int(playerdatacontents[11].string)

    for playerdata in team2_bowling_data_array:
        playerdatacontents = playerdata.contents
        temp_model = create_player_performance_model(playerdatacontents[1].a.get('href'))
        player_model = team2dictionary.get(temp_model.player_id)

        player_model.overs_bowled = float(playerdatacontents[3].string)
        player_model.maidens = int(playerdatacontents[5].string)
        player_model.runs_conceded = int(playerdatacontents[7].string)
        player_model.wickets_taken = int(playerdatacontents[9].string)
        player_model.no_balls = int(playerdatacontents[11].string)
        player_model.wides = int(playerdatacontents[13].string)

    for playerdata in team1_bowling_data_array:
        playerdatacontents = playerdata.contents
        temp_model = create_player_performance_model(playerdatacontents[1].a.get('href'))
        player_model = team1dictionary.get(temp_model.player_id)
        player_model.overs_bowled = float(playerdatacontents[3].string)
        player_model.maidens = int(playerdatacontents[5].string)
        player_model.runs_conceded = int(playerdatacontents[7].string)
        player_model.wickets_taken = int(playerdatacontents[9].string)
        player_model.no_balls = int(playerdatacontents[11].string)
        player_model.wides = int(playerdatacontents[13].string)

    # match_performance_writer.writerow(
    #         ["player_id", "runs_scored", "balls_batted", "fours_scored", "sixes_scored", "overs_bowled", "maidens",
    #          "runs_conceded", "wickets_taken", "no_balls", "wides", "final_out_condition"])

    for player_model in team1dictionary.values():
        match_performance_writer.writerow(
            [match_id, team1_id, player_model.player_id, player_model.runs_scored, player_model.balls_batted,
             player_model.fours_scored, player_model.sixes_scored, player_model.overs_bowled, player_model.maidens,
             player_model.runs_conceded, player_model.wickets_taken, player_model.no_balls, player_model.wides,
             player_model.final_out_condition])

    for player_model in team2dictionary.values():
        match_performance_writer.writerow(
            [match_id, team2_id, player_model.player_id, player_model.runs_scored, player_model.balls_batted,
             player_model.fours_scored, player_model.sixes_scored,
             player_model.overs_bowled, player_model.maidens, player_model.runs_conceded,
             player_model.wickets_taken, player_model.no_balls, player_model.wides,
             player_model.final_out_condition])

    return total_runs_team1, total_runs_team2


def init_match_performance_data_wtests(match_id, team1_id, team2_id, match_type):
    full_url = URL_FOR_SCORECARD + str(match_id)
    print(full_url)

    path_name = "api_data/match_performance_data/"
    create_directory_if_not_exist(path_name)

    match_performance_writer = csv.writer(open(path_name + str(match_id) + ".csv", "w", newline=""))

    match_performance_writer.writerow(
        ["match_id", "innings_no", "team_id", "player_id", "runs_scored", "balls_batted", "fours_scored",
         "sixes_scored",
         "overs_bowled", "maidens",
         "runs_conceded", "wickets_taken", "no_balls", "wides", "final_out_condition"])

    http = urllib3.PoolManager()
    response = http.request('GET', full_url)
    soup = BeautifulSoup(response.data, features="html.parser")

    innings1Tag = soup.findAll('div', {"id": 'innings_1'})[0]
    innings2Tag = soup.findAll('div', {"id": 'innings_2'})[0]

    # cb-col cb-col-100 cb-ltst-wgt-hdr  -> cb-col cb-col-100 cb-scrd-itms <space ase ekta btw

    team1_inn1_batting_data = innings1Tag.findAll('div', {"class": "cb-col cb-col-100 cb-ltst-wgt-hdr"})[0]
    team2_inn1_bowling_data = innings1Tag.findAll('div', {"class": "cb-col cb-col-100 cb-ltst-wgt-hdr"})[1]

    team2_inn2_batting_data = innings2Tag.findAll('div', {"class": "cb-col cb-col-100 cb-ltst-wgt-hdr"})[0]
    team1_inn2_bowling_data = innings2Tag.findAll('div', {"class": "cb-col cb-col-100 cb-ltst-wgt-hdr"})[1]

    team1_inn12_dictionary = create_players_dictionary(team1_inn1_batting_data)
    team2_inn12_dictionary = create_players_dictionary(team2_inn2_batting_data)

    # print(len(team1dictionary))

    # print(team1_batting_data.prettify())

    # class="cb-col cb-col-100 cb-scrd-itms"

    team1_inn1_batting_data_array = team1_inn1_batting_data.findAll('div', {"class": "cb-col cb-col-100 cb-scrd-itms"})
    team2_inn1_bowling_data_array = team2_inn1_bowling_data.findAll('div', {"class": "cb-col cb-col-100 cb-scrd-itms"})
    team2_inn2_batting_data_array = team2_inn2_batting_data.findAll('div', {"class": "cb-col cb-col-100 cb-scrd-itms"})
    team1_inn2_bowling_data_array = team1_inn2_bowling_data.findAll('div', {"class": "cb-col cb-col-100 cb-scrd-itms"})

    no_inn_4 = False
    if match_type == 'TEST':
        innings3Tag = soup.findAll('div', {"id": 'innings_3'})[0]
        team1_inn3_batting_data = innings3Tag.findAll('div', {"class": "cb-col cb-col-100 cb-ltst-wgt-hdr"})[0]
        team2_inn3_bowling_data = innings3Tag.findAll('div', {"class": "cb-col cb-col-100 cb-ltst-wgt-hdr"})[1]
        team1_inn34_dictionary = create_players_dictionary(team1_inn3_batting_data)
        team1_inn3_batting_data_array = team1_inn3_batting_data.findAll('div',
                                                                        {"class": "cb-col cb-col-100 cb-scrd-itms"})
        team2_inn3_bowling_data_array = team2_inn3_bowling_data.findAll('div',
                                                                      {"class": "cb-col cb-col-100 cb-scrd-itms"})
        try:
            innings4Tag = soup.findAll('div', {"id": 'innings_4'})[0]

            team2_inn4_batting_data = innings4Tag.findAll('div', {"class": "cb-col cb-col-100 cb-ltst-wgt-hdr"})[0]
            team1_inn4_bowling_data = innings4Tag.findAll('div', {"class": "cb-col cb-col-100 cb-ltst-wgt-hdr"})[1]
            team2_inn34_dictionary = create_players_dictionary(team2_inn4_batting_data)
            team2_inn4_batting_data_array = team2_inn4_batting_data.findAll('div',
                                                                        {"class": "cb-col cb-col-100 cb-scrd-itms"})
            team1_inn4_bowling_data_array = team1_inn4_bowling_data.findAll('div',
                                                                        {"class": "cb-col cb-col-100 cb-scrd-itms"})
        except IndexError:
            print('might not have innings 4')
            team2_inn34_dictionary = create_players_dictionary(team2_inn3_bowling_data)
            no_inn_4 = True

    # print(team1_batting_data_array[0].prettify())

    # children = team1_batting_data_array[0].contents
    # print(children[5])

    total_runs_inn1_team1 = 0
    total_runs_inn2_team2 = 0
    total_runs_inn3_team1 = 0
    total_runs_inn4_team2 = 0

    for playerdata in team1_inn1_batting_data_array:

        all_text = playerdata.get_text()
        if "Extras" in all_text or "Did not Bat" in all_text:
            continue
        if "Total" in all_text:
            total_runs_inn1_team1 = int(playerdata.contents[3].string)
            # print(total_runs_inn1_team1)
            continue

        playerdatacontents = playerdata.contents
        temp_model = create_player_performance_model(playerdatacontents[1].a.get('href'))
        player_model = team1_inn12_dictionary.get(temp_model.player_id)

        player_model.final_out_condition = playerdatacontents[3].span.string
        player_model.runs_scored = int(playerdatacontents[5].string)
        player_model.balls_batted = int(playerdatacontents[7].string)
        player_model.fours_scored = int(playerdatacontents[9].string)
        player_model.sixes_scored = int(playerdatacontents[11].string)
    for playerdata in team2_inn2_batting_data_array:

        all_text = playerdata.get_text()
        if "Extras" in all_text or "Did not Bat" in all_text:
            continue
        if "Total" in all_text:
            total_runs_inn2_team2 = int(playerdata.contents[3].string)
            # print(total_runs_inn1_team1)
            continue

        playerdatacontents = playerdata.contents
        temp_model = create_player_performance_model(playerdatacontents[1].a.get('href'))
        player_model = team2_inn12_dictionary.get(temp_model.player_id)

        player_model.final_out_condition = playerdatacontents[3].span.string
        player_model.runs_scored = int(playerdatacontents[5].string)
        player_model.balls_batted = int(playerdatacontents[7].string)
        player_model.fours_scored = int(playerdatacontents[9].string)
        player_model.sixes_scored = int(playerdatacontents[11].string)
    for playerdata in team2_inn1_bowling_data_array:
        playerdatacontents = playerdata.contents
        temp_model = create_player_performance_model(playerdatacontents[1].a.get('href'))
        player_model = team2_inn12_dictionary.get(temp_model.player_id)

        player_model.overs_bowled = float(playerdatacontents[3].string)
        player_model.maidens = int(playerdatacontents[5].string)
        player_model.runs_conceded = int(playerdatacontents[7].string)
        player_model.wickets_taken = int(playerdatacontents[9].string)
        player_model.no_balls = int(playerdatacontents[11].string)
        player_model.wides = int(playerdatacontents[13].string)
    for playerdata in team1_inn2_bowling_data_array:
        playerdatacontents = playerdata.contents
        temp_model = create_player_performance_model(playerdatacontents[1].a.get('href'))
        player_model = team1_inn12_dictionary.get(temp_model.player_id)
        player_model.overs_bowled = float(playerdatacontents[3].string)
        player_model.maidens = int(playerdatacontents[5].string)
        player_model.runs_conceded = int(playerdatacontents[7].string)
        player_model.wickets_taken = int(playerdatacontents[9].string)
        player_model.no_balls = int(playerdatacontents[11].string)
        player_model.wides = int(playerdatacontents[13].string)

    if match_type == 'TEST':
        for playerdata in team1_inn3_batting_data_array:

            all_text = playerdata.get_text()
            if "Extras" in all_text or "Did not Bat" in all_text:
                continue
            if "Total" in all_text:
                total_runs_inn3_team1 = int(playerdata.contents[3].string)
                # print(total_runs_inn3_team1)
                continue

            playerdatacontents = playerdata.contents
            temp_model = create_player_performance_model(playerdatacontents[1].a.get('href'))
            player_model = team1_inn34_dictionary.get(temp_model.player_id)

            player_model.final_out_condition = playerdatacontents[3].span.string
            player_model.runs_scored = int(playerdatacontents[5].string)
            player_model.balls_batted = int(playerdatacontents[7].string)
            player_model.fours_scored = int(playerdatacontents[9].string)
            player_model.sixes_scored = int(playerdatacontents[11].string)

        if not no_inn_4:
            for playerdata in team2_inn4_batting_data_array:
                all_text = playerdata.get_text()
                if "Extras" in all_text or "Did not Bat" in all_text:
                    continue
                if "Total" in all_text:
                    total_runs_inn4_team2 = int(playerdata.contents[3].string)
                    # print(total_runs_inn4_team2)
                    continue

                playerdatacontents = playerdata.contents
                temp_model = create_player_performance_model(playerdatacontents[1].a.get('href'))
                player_model = team2_inn34_dictionary.get(temp_model.player_id)

                player_model.final_out_condition = playerdatacontents[3].span.string
                player_model.runs_scored = int(playerdatacontents[5].string)
                player_model.balls_batted = int(playerdatacontents[7].string)
                player_model.fours_scored = int(playerdatacontents[9].string)
                player_model.sixes_scored = int(playerdatacontents[11].string)

        for playerdata in team2_inn3_bowling_data_array:
            playerdatacontents = playerdata.contents
            temp_model = create_player_performance_model(playerdatacontents[1].a.get('href'))
            player_model = team2_inn34_dictionary.get(temp_model.player_id)
            player_model.overs_bowled = float(playerdatacontents[3].string)
            player_model.maidens = int(playerdatacontents[5].string)
            player_model.runs_conceded = int(playerdatacontents[7].string)
            player_model.wickets_taken = int(playerdatacontents[9].string)
            player_model.no_balls = int(playerdatacontents[11].string)
            player_model.wides = int(playerdatacontents[13].string)
        if not no_inn_4:
            for playerdata in team1_inn4_bowling_data_array:
                playerdatacontents = playerdata.contents
                temp_model = create_player_performance_model(playerdatacontents[1].a.get('href'))
                player_model = team1_inn34_dictionary.get(temp_model.player_id)
                player_model.overs_bowled = float(playerdatacontents[3].string)
                player_model.maidens = int(playerdatacontents[5].string)
                player_model.runs_conceded = int(playerdatacontents[7].string)
                player_model.wickets_taken = int(playerdatacontents[9].string)
                player_model.no_balls = int(playerdatacontents[11].string)
                player_model.wides = int(playerdatacontents[13].string)

    # match_performance_writer.writerow(
    #         ["player_id", "runs_scored", "balls_batted", "fours_scored", "sixes_scored", "overs_bowled", "maidens",
    #          "runs_conceded", "wickets_taken", "no_balls", "wides", "final_out_condition"])

    for player_model in team1_inn12_dictionary.values():
        match_performance_writer.writerow(
            [match_id, "1", team1_id, player_model.player_id, player_model.runs_scored, player_model.balls_batted,
             player_model.fours_scored, player_model.sixes_scored, player_model.overs_bowled, player_model.maidens,
             player_model.runs_conceded, player_model.wickets_taken, player_model.no_balls, player_model.wides,
             player_model.final_out_condition])

    for player_model in team2_inn12_dictionary.values():
        match_performance_writer.writerow(
            [match_id, "2", team2_id, player_model.player_id, player_model.runs_scored, player_model.balls_batted,
             player_model.fours_scored, player_model.sixes_scored,
             player_model.overs_bowled, player_model.maidens, player_model.runs_conceded,
             player_model.wickets_taken, player_model.no_balls, player_model.wides,
             player_model.final_out_condition])

    if match_type == 'TEST':
        for player_model in team1_inn34_dictionary.values():
            match_performance_writer.writerow(
                [match_id, "3", team1_id, player_model.player_id, player_model.runs_scored, player_model.balls_batted,
                 player_model.fours_scored, player_model.sixes_scored, player_model.overs_bowled, player_model.maidens,
                 player_model.runs_conceded, player_model.wickets_taken, player_model.no_balls, player_model.wides,
                 player_model.final_out_condition])
        if not no_inn_4:
            for player_model in team2_inn34_dictionary.values():
                match_performance_writer.writerow(
                    [match_id, "4", team2_id, player_model.player_id, player_model.runs_scored, player_model.balls_batted,
                    player_model.fours_scored, player_model.sixes_scored,
                    player_model.overs_bowled, player_model.maidens, player_model.runs_conceded,
                    player_model.wickets_taken, player_model.no_balls, player_model.wides,
                    player_model.final_out_condition])

    return total_runs_inn1_team1, total_runs_inn2_team2, total_runs_inn3_team1, total_runs_inn4_team2


# sending get request and saving the response as response object
r = requests.get(url=URL)

# extracting data in json format
data = r.json()

init_all_match_data(data)
