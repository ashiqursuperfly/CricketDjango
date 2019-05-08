from django.urls import path

from . import views

app_name = 'cric_db_app'  # this app's name-space,
# app_name allows it to distinguish it's urls from same name urls of other app's in the same project
urlpatterns = [
    # ex: /cric_db_app/
    path('', views.index, name='index'),
    path('player/<int:player_id>', views.get_player, name='get_player'),
    path('scorecard/<int:match_id>', views.get_scorecard, name='get_scorecard'),
    path('allmatch/', views.get_all_matches, name='get_allmatch'),
    path('allplayers/', views.get_all_players, name='get_allplayers'),
    path('sql_select/<sql_string>', views.any_sql, name='any_sql'),
    path('series/<int:series_id>', views.get_series, name='get_series'),
    path('update', views.update_all_data, name='update_all'),
    # ex: /polls/5/
    # path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    # path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    # path('<int:question_id>/vote/', views.vote, name='vote'),
    # path('doshit/<randomstring>/', views.doshit, name='doshit'),

]
