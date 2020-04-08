--Find the teams that are playing in a specific series:

Select team_name
from teams
where team_id in (
    select team_id from teams_plays_in_series where series_id = (
        select series_id from series where lower(series_name) like lower('Bangladesh Premier League 2019'))
                   );



--Get All Teams that play in a specific league:

Select team_id, team_name
FROM teams
WHERE LOWER(league) like lower('international');

--get Team rankings for a speciifc format

select team_name, points
from teams, team_ranking
where teams.team_id = team_ranking.team_id and lower(match_format) like lower('test')
order by points;

--get Player ranking for speicifc format and criteria
select full_name, points
from players, player_ranking
where players.player_id = player_ranking.player_id and lower(match_format) like lower('test')
and lower(criteria) like lower('batting')
order by points;

--Find umpires that conducted a specific match

select  full_name, umpiring_role
from players, umpires_conducts_match
where players.player_id = umpires_conducts_match.player_id and match_id = 1000;

--Find coaches of a specific team
select full_name
from players
where player_id in (select coach_id from coaches where team_id = 11);


--Find performance of a specific player in a certain match

Select *
From match_performance_data
where match_id = 22248 and player_id in (select player_id from players where full_name ilike 'Stafanie Taylor');


--Find Winner of a Series

SELECT series_name, winner
from series
where series_id = 2772;






--Find career batting data of a specific playerID for specific match format
select player_id,
       (select sum(runs_scored)
        from match_performance_data
        where match_performance_data.player_id = 9088
          and (select match_type from match where this_match.match_id = match.match_id) ilike 'ODI') as total_runs,
       (select count(final_out_condition)
        from match_performance_data
        where player_id = 9088
          and final_out_condition ilike 'not out'
          and (select match_type from match where this_match.match_id = match.match_id) ilike 'ODI')             as not_outs,
       (select max(runs_scored)
        from match_performance_data
        where player_id = 9088
          and (select match_type from match where this_match.match_id = match.match_id) ilike 'ODI')             as high_score,
       (select sum(match_performance_data.balls_batted)
        from match_performance_data
        where match_performance_data.player_id = 9088
          and (select match_type from match where this_match.match_id = match.match_id) ilike 'ODI') as balls_faced,
       (select count(*)
        from match_performance_data
        where match_performance_data.player_id = 9088
          and (select match_type from match where this_match.match_id = match.match_id) ilike 'ODI') as innings,
        (select (sum(runs_scored) :: float / sum(balls_batted) :: float) * 100.0
        from match_performance_data
        where match_performance_data.player_id = 9088
          and (select match_type from match where this_match.match_id = match.match_id) ilike 'ODI')
                                  as strike_rate,
      (select avg(match_performance_data.runs_scored)
        from match_performance_data
        where match_performance_data.player_id = 9088
          and (select match_type from match where this_match.match_id = match.match_id) ilike 'ODI')                                                                             as average_runs,
       (select sum(match_performance_data.fours_scored)
        from match_performance_data
        where match_performance_data.player_id = 9088
          and (select match_type from match where this_match.match_id = match.match_id) ilike 'ODI')                                                                           as fours_scored,
       (select sum(sixes_scored)
        from match_performance_data
        where match_performance_data.player_id = 9088
          and (select match_type from match where this_match.match_id = match.match_id) ilike 'ODI')                                                                             as sixes_scored,
       (select coalesce(count(runs_scored), 0)
        from match_performance_data as centurydata
        where centurydata.player_id = 9088
          and centurydata.runs_scored >= 100
          and (select match_type from match where this_match.match_id = match.match_id) ilike 'ODI') as centuries,
       (select coalesce(count(runs_scored), 0)
        from match_performance_data as centurydata2
        where centurydata2.player_id = 9088
          and centurydata2.runs_scored >= 50)                                                        as half_centuries
from match_performance_data as this_match
where player_id = 9089
  and (select match_type from match where match.match_id = this_match.match_id) ilike 'ODI';


  --find career bowling data for specific matchid for specific match_format
  select  player_id,
       (select count(*)
        from match_performance_data
        where match_performance_data.player_id = 9089
          and (select match_type from match where this_match.match_id = match.match_id) ilike 'ODI') as
    matches,
  (select count(*)
        from match_performance_data
        where match_performance_data.player_id = 9089 and match_performance_data.overs_bowled > 0
          and (select match_type from match where this_match.match_id = match.match_id) ilike 'ODI') as
    innings,
       (select sum(match_performance_data.overs_bowled) * 6
        from match_performance_data
        where match_performance_data.player_id = 9089
          and (select match_type from match where this_match.match_id = match.match_id) ilike 'ODI') as balls,
       (select sum(match_performance_data.runs_conceded)
        from match_performance_data
        where player_id = 9089
          and (select match_type from match where this_match.match_id = match.match_id) ilike 'ODI') as runs_conceded,
       (select sum(match_performance_data.wickets_taken)
        from match_performance_data
        where player_id = 9089
          and (select match_type from match where this_match.match_id = match.match_id) ilike 'ODI') as wickets,
       (select sum(match_performance_data.overs_bowled)::float * 6.0 / sum(match_performance_data.wickets_taken)::float
        from match_performance_data
        where match_performance_data.player_id = 9089
          and (select match_type from match where this_match.match_id = match.match_id) ilike 'ODI') as strike_rate,
       (select sum(match_performance_data.runs_conceded)::float / sum(match_performance_data.wickets_taken)::float
        from match_performance_data
        where match_performance_data.player_id = 9089
          and (select match_type from match where this_match.match_id = match.match_id) ilike 'ODI') as bowling_average,

       (select sum(match_performance_data.runs_conceded )::float / sum(match_performance_data.overs_bowled)::float
        from match_performance_data
        where match_performance_data.player_id = 9089
          and (select match_type from match where this_match.match_id = match.match_id) ilike 'ODI') as economy,
       (select sum(match_performance_data.wickets_taken)
        from match_performance_data
        where match_performance_data.player_id = 9089 and match_performance_data.wickets_taken = 4
          and (select match_type from match where this_match.match_id = match.match_id) ilike 'ODI') as four_wickets_taken,
       (select sum(match_performance_data.wickets_taken)
        from match_performance_data
        where match_performance_data.player_id = 9089 and match_performance_data.wickets_taken > 4 and match_performance_data.wickets_taken < 10
          and (select match_type from match where this_match.match_id = match.match_id) ilike 'ODI') as five_wickets_taken,
        (select sum(match_performance_data.wickets_taken)
        from match_performance_data
        where match_performance_data.player_id = 9089 and match_performance_data.wickets_taken = 10
          and (select match_type from match where this_match.match_id = match.match_id) ilike 'ODI') as ten_wickets_taken

from match_performance_data as this_match
where player_id = 9089
  and (select match_type from match where match.match_id = this_match.match_id) ilike 'ODI';



--Get player rankings of a given player
select *
from player_ranking
where player_id = (select player_id from players where full_name ilike '%Shoaib Malik%')


--find player to win highest number of MOTS for a given year
select count(mots), (select full_name from players where player_id = mots)
from series
group by mots
order by  count(mots) desc
limit 1;


-- Get current scoreboard (summary)
select (select team_name from teams where matchtable2.team_id = teams.team_id), sum(runs_scored) as runs, sum(balls_batted)::float / 6.00 as overs,
       (select sum(wickets_taken) from match_performance_data where matchtable2.team_id != match_performance_data.team_id ) as wickets
from match_performance_data as matchtable2
where match_id = 22248
group by  team_id;
