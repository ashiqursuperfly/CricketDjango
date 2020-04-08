create table teams
(
	team_id integer not null
		constraint teams_pkey
			primary key,
	team_name varchar(100) not null,
	league varchar(100) not null
);

alter table teams owner to postgres;

create table players
(
	player_id integer not null
		constraint players_pkey
			primary key,
	full_name varchar(100) not null,
	nationality varchar(50),
	batting_style varchar(100),
	bowling_style varchar(100),
	speciality varchar(100)
);

alter table players owner to postgres;

create table player_plays_for_teams
(
	team_id integer not null
		constraint player_plays_for_teams_team_id_fkey
			references teams,
	player_id integer not null
		constraint player_plays_for_teams_player_id_fkey
			references players,
	constraint player_plays_for_teams_pkey
		primary key (team_id, player_id)
);

alter table player_plays_for_teams owner to postgres;

create table series
(
	series_id integer not null
		constraint series_pkey
			primary key,
	series_name varchar(100) not null,
	mots integer
		constraint series_mots_fkey
			references players,
	winner integer
		constraint series_winner_fkey
			references teams
);

alter table series owner to postgres;

create table teams_plays_in_series
(
	team_id integer not null
		constraint teams_plays_in_series_team_id_fkey
			references teams,
	series_id integer not null
		constraint teams_plays_in_series_series_id_fkey
			references series,
	constraint teams_plays_in_series_pkey
		primary key (team_id, series_id)
);

alter table teams_plays_in_series owner to postgres;

create table player_ranking
(
	player_id integer not null
		constraint player_ranking_player_id_fkey
			references players,
	match_format varchar(50) not null,
	criteria varchar(50) not null,
	points integer not null
);

alter table player_ranking owner to postgres;

create table team_ranking
(
	team_id integer not null
		constraint team_ranking_team_id_fkey
			references teams,
	match_format varchar(50) not null,
	points integer not null
);

alter table team_ranking owner to postgres;

create table umpires
(
	player_id integer
		constraint umpires_player_id_key
			unique
		constraint umpires_player_id_fkey
			references players,
	odis_umpired integer default 0,
	tests_umpired integer default 0,
	t20s_umpired integer default 0
);

alter table umpires owner to postgres;

create table coaches
(
	player_id integer
		constraint coaches_player_id_fkey
			references players,
	coaching_role varchar(100),
	team_id integer
		constraint coaches_team_id_fkey
			references teams
);

alter table coaches owner to postgres;

create table match
(
	match_id integer not null
		constraint match_pkey
			primary key,
	match_type varchar(50) not null,
	team1_id integer not null,
	team2_id integer not null,
	captain1 integer not null
		constraint match_captain1_fkey
			references players,
	captain2 integer not null
		constraint match_captain2_fkey
			references players,
	score1 varchar(50),
	score2 varchar(50),
	score3 integer default '-1'::integer,
	score4 integer default '-1'::integer,
	venue varchar(200),
	stadium_name varchar(200),
	start_date date,
	winner integer
		constraint match_winner_fkey
			references teams,
	motm integer
		constraint match_motm_fkey
			references players,
	series_id integer
		constraint match_series_id_fkey
			references series
);

alter table match owner to postgres;

create table umpires_conducts_match
(
	match_id integer not null
		constraint umpires_conducts_match_match_id_fkey
			references match,
	player_id integer not null
		constraint umpires_conducts_match_player_id_fkey
			references players,
	umpiring_role varchar(50),
	constraint umpires_conducts_match_pkey
		primary key (player_id, match_id)
);

alter table umpires_conducts_match owner to postgres;

create table match_performance_data
(
	match_id integer not null
		constraint match_performance_data_match_id_fkey
			references match,
	innings_no integer not null,
	team_id integer
		constraint match_performance_data_team_id_fkey
			references teams,
	player_id integer not null
		constraint match_performance_data_player_id_fkey
			references players,
	runs_scored integer default 0,
	balls_batted integer default 0,
	fours_scored integer default 0,
	sixes_scored integer default 0,
	overs_bowled double precision default 0,
	maidens integer default 0,
	runs_conceded integer default 0,
	wickets_taken integer default 0,
	no_balls integer default 0,
	wides integer default 0,
	final_out_condition varchar(200),
	constraint match_performance_data_pkey
		primary key (match_id, innings_no, player_id)
);

alter table match_performance_data owner to postgres;




create table ball_by_ball_performance_data (
  match_id                 integer not null
    constraint ball_by_ball_performance_data_match_id_fkey
    references match,
  batting_team_id                  integer
    constraint ball_by_ball_performance_data_batting_team_id_fkey
    references teams,
  balling_team_id                  integer
    constraint ball_by_ball_performance_data_balling_team_id_fkey
    references teams,
  batsman_id               integer not null
    constraint ball_by_ball_performance_data_batsman_id_fkey
    references players,
  batsman_second_id        integer not null
    constraint ball_by_ball_performance_data_batsman_second_id_fkey
    references players,
  baller_id                integer not null
    constraint ball_by_ball_performance_data_baller_id_fkey
    references players,
  wicket_taking_fielder_id integer
    constraint ball_by_ball_performance_data_wicket_taking_fielder_id_fkey
    references players,
  innings_no               integer not null,
  over_number              integer not null,
  ball_number              integer not null,
  commentary               varchar(1000),
  run_scored               integer not null default 0,
  is_free_hit              boolean          default false,
  wicket_type              varchar(100),
  balling_violation_type   varchar(100),
	outed_batsman_id integer constraint ball_by_ball_performance_data_outed_batsman_id_fkey
    references players, 

    constraint ball_by_ball_performance_data_pkey primary key (match_id, batting_team_id, balling_team_id, innings_no, over_number, ball_number)


);


alter table ball_by_ball_performance_data owner to postgres;


--DO $$
--  <<first_block>>
--  BEGIN
--    CREATE TEMP TABLE tmp_table ON COMMIT DROP AS
--    SELECT * FROM match_performance_data WITH NO DATA;
--    copy tmp_table FROM 'F:/Database/Database Project All/cric_final/match_performance_data/22248.csv' DELIMITER ',' CSV HEADER;
--    INSERT INTO match_performance_data SELECT DISTINCT ON (match_id,innings_no,player_id) * FROM tmp_table ON CONFLICT DO NOTHING;
--    COMMIT;
--  END first_block $$;



--call init_all_match_data();


-- SELECT player_id,SUM(runs_scored),SUM(runs_conceded) FROM match_performance_data
-- WHERE match_id = 21197
-- GROUP BY player_id
-- ORDER BY player_id;

-- SELECT DISTINCT match_id FROM match_performance_data;
