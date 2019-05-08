from django.db import connection, ProgrammingError
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
import os

from cric_db_app.forms import ContactForm

match_performance_procedure = "DO $$  <<first_block>>  DECLARE r VARCHAR(100);" \
                              " BEGIN CREATE TEMP TABLE tmp_table ON COMMIT DROP AS SELECT * FROM match_performance_data WITH NO DATA;" \
                              " copy tmp_table FROM 'E:/Pycharm Workspace/EspnCricinfo/api_data/match_performance_data/##.csv' DELIMITER ',' CSV HEADER;" \
                              " INSERT INTO match_performance_data SELECT DISTINCT ON (match_id,innings_no,player_id) * FROM tmp_table ON CONFLICT DO NOTHING;" \
                              " COMMIT;END first_block $$;"


def sql_select(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    results_list = []
    try:
        results = cursor.fetchall()
    except ProgrammingError as e:
        # print(e)
        return []

    i = 0
    for row in results:
        dict = {}
        field = 0
        while True:
            try:
                dict[cursor.description[field][0]] = str(results[i][field])
                field = field + 1
            except IndexError as e:
                break
        i = i + 1
        results_list.append(dict)
    return results_list


def index(request):
    run_update_schedules()

    if request.method == 'POST':
        sql_string = request.POST.get('sql_string')
        print(sql_string)
        result_list = sql_select(sql_string)
        return render(request, "cric_db_app/query.html", {'results': result_list})

    return render(request, 'cric_db_app/index.html')


def get_player(request, player_id):
    result_list = sql_select('SELECT * FROM players WHERE player_id =' + str(player_id))
    # print(result_list)
    context = {'results': result_list}
    return render(request, 'cric_db_app/query.html', context)


def get_scorecard(request, match_id):
    result_list = sql_select(
        'SELECT full_name as "Player",team_name as "Team" ,innings_no as "Innings",runs_scored,balls_batted,fours_scored,'
        'sixes_scored,overs_bowled,'
        'maidens,runs_conceded,wickets_taken,no_balls,wides,final_out_condition'
        ' FROM players,teams,match_performance_data WHERE players.player_id = match_performance_data.player_id'
        ' AND teams.team_id = match_performance_data.team_id AND match_id =' + str(match_id) + 'order by innings_no asc'
    )
    # print(result_list)
    context = {'results': result_list}
    return render(request, 'cric_db_app/query.html', context)


def get_all_matches(request):
    result_list = sql_select('SELECT * FROM match')
    # print(result_list)
    context = {'results': result_list}
    return render(request, 'cric_db_app/query.html', context)


def get_all_players(request):
    result_list = sql_select('SELECT * FROM players')
    # print(result_list)
    context = {'results': result_list}
    return render(request, 'cric_db_app/query.html', context)


def any_sql(request, sql_string):
    print(sql_string)
    result_list = sql_select(sql_string)
    # print(result_list)
    context = {'results': result_list}
    return render(request, 'cric_db_app/query.html', context)


def get_series(request, series_id):
    result_list = sql_select('SELECT * FROM SERIES WHERE SERIES_ID = ' + str(series_id))
    context = {'results': result_list}
    return render(request, 'cric_db_app/query.html', context)


def home(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            pass  # does nothing, just trigger the validation
    else:
        form = ContactForm()
    print(form.data)
    return render(request, 'cric_db_app/index.html', {'form': form})


def run_update_schedules():
    os.system('python backup_scripts.py')

    sql_select('call init_all_match_data()')

    results = sql_select("SELECT DISTINCT match_id FROM match"
                         " EXCEPT"
                         " SELECT DISTINCT match_id FROM match_performance_data order by match_id;")

    for i in results:
        print('item :', i)
        procedure_to_update_match_performance = match_performance_procedure.replace('##', dict(i).get("match_id"))
        sql_select(procedure_to_update_match_performance)
        print('procedure ran :', procedure_to_update_match_performance)

    results.append({'Summary:': 'ALL DATA UP TO DATE! ' + str(results.__len__()) + ' rows updated'})
    print('All DATA UP TO DATE ! ', results.__len__(), 'rows updated')
    return results


def update_all_data(request):
    results = run_update_schedules()
    return render(request, 'cric_db_app/query.html', {'results': results})
