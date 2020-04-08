create or replace procedure init_teams()
	language plpgsql
as $$
BEGIN
    CREATE TEMP TABLE tmp_table ON COMMIT DROP AS SELECT * FROM TEAMS WITH NO DATA;
    copy tmp_table FROM 'F:/Database/Database Project All/cric_final/api_data/teams.csv' DELIMITER ',' CSV HEADER;
    INSERT INTO TEAMS SELECT DISTINCT ON (team_id) * FROM tmp_table ON CONFLICT DO NOTHING;
    COMMIT;
END;
$$;

alter procedure init_teams() owner to postgres;

create or replace procedure init_players()
	language plpgsql
as $$
DECLARE R RECORD;
BEGIN
    CREATE TEMP TABLE tmp_table ON COMMIT DROP AS SELECT * FROM PLAYERS WITH NO DATA;
    copy tmp_table FROM 'F:/Database/Database Project All/cric_final/api_data/players.csv' DELIMITER ',' CSV HEADER;
    FOR R IN (SELECT * FROM tmp_table) LOOP
    IF R.player_id IN (SELECT player_id FROM players) THEN
      UPDATE players SET nationality = R.nationality WHERE player_id = R.player_id;
    ELSE INSERT INTO players VALUES(R.player_id,R.full_name,R.nationality,R.batting_style,R.bowling_style,R.speciality);
    END IF ;
    END LOOP;
    COMMIT;
END;
$$;

alter procedure init_players() owner to postgres;

create or replace procedure init_players_plays_for_teams()
	language plpgsql
as $$
BEGIN
    CREATE TEMP TABLE tmp_table ON COMMIT DROP AS SELECT * FROM PLAYER_PLAYS_FOR_TEAMS WITH NO DATA;
    copy tmp_table FROM 'F:/Database/Database Project All/cric_final/api_data/player_plays_for_teams.csv' DELIMITER ',' CSV HEADER;
    INSERT INTO PLAYER_PLAYS_FOR_TEAMS SELECT DISTINCT ON (player_id,team_id) * FROM tmp_table ON CONFLICT DO NOTHING;
    COMMIT;
END;
$$;

alter procedure init_players_plays_for_teams() owner to postgres;

create or replace procedure init_series()
	language plpgsql
as $$
DECLARE R RECORD;
BEGIN
    CREATE TEMP TABLE tmp_table ON COMMIT DROP AS SELECT * FROM SERIES WITH NO DATA;
    copy tmp_table FROM 'F:/Database/Database Project All/cric_final/api_data/series.csv' DELIMITER ',' CSV HEADER;
    FOR R IN (SELECT * FROM tmp_table) LOOP
    IF R.series_id IN (SELECT series_id FROM series) THEN
      UPDATE series SET mots = R.mots,winner = R.winner WHERE series_id = R.series_id;
    ELSE INSERT INTO SERIES VALUES(R.series_id,R.series_name,R.mots,R.winner);
    END IF ;
    END LOOP;
COMMIT;
END;
$$;

alter procedure init_series() owner to postgres;

create or replace procedure init_teams_play_in_series()
	language plpgsql
as $$
BEGIN
    CREATE TEMP TABLE tmp_table ON COMMIT DROP AS SELECT * FROM TEAMS_PLAYS_IN_SERIES WITH NO DATA;
    copy tmp_table FROM 'F:/Database/Database Project All/cric_final/api_data/teams_plays_in_series.csv' DELIMITER ',' CSV HEADER;
    INSERT INTO TEAMS_PLAYS_IN_SERIES SELECT DISTINCT ON (series_id,team_id) * FROM tmp_table ON CONFLICT DO NOTHING;
    COMMIT;
END;
$$;

alter procedure init_teams_play_in_series() owner to postgres;

create or replace procedure init_umpires()
	language plpgsql
as $$
DECLARE R RECORD;
BEGIN
    CREATE TEMP TABLE tmp_table
    (
      umpire_id INTEGER,
      full_name VARCHAR(100),
      nationality VARCHAR(100)
    ) ON COMMIT DROP ;
    copy tmp_table FROM 'F:/Database/Database Project All/cric_final/api_data/umpires.csv' DELIMITER ',' CSV HEADER;
    FOR R in (SELECT * FROM tmp_table) LOOP
      CALL validate_umpire_fk(R.umpire_id,R.full_name,R.nationality);
    END LOOP;
    COMMIT;
END;
$$;

alter procedure init_umpires() owner to postgres;

create or replace procedure validate_umpire_fk(integer, character varying, character varying)
	language plpgsql
as $$
DECLARE u_id INTEGER; f_name VARCHAR(100); nation VARCHAR(100);
BEGIN
    u_id = $1; f_name = $2; nation = $3;
    INSERT INTO PLAYERS(player_id, full_name, nationality) VALUES(u_id,f_name,nation) ON CONFLICT DO NOTHING ;
    INSERT INTO UMPIRES(player_id) VALUES(u_id) ON CONFLICT DO NOTHING;
    COMMIT;
END;
$$;

alter procedure validate_umpire_fk(integer, varchar, varchar) owner to postgres;

create or replace procedure init_umpire_conducts_match()
	language plpgsql
as $$
BEGIN
    CREATE TEMP TABLE tmp_table ON COMMIT DROP AS SELECT * FROM umpires_conducts_match WITH NO DATA;
    copy tmp_table FROM 'F:/Database/Database Project All/cric_final/api_data/umpire_conducts_match.csv' DELIMITER ',' CSV HEADER;
    INSERT INTO umpires_conducts_match SELECT DISTINCT ON (player_id,match_id) * FROM tmp_table ON CONFLICT DO NOTHING;
    COMMIT;
END;
$$;

alter procedure init_umpire_conducts_match() owner to postgres;

create or replace procedure init_matches()
	language plpgsql
as $$
BEGIN
    CREATE TEMP TABLE tmp_table ON COMMIT DROP AS SELECT * FROM MATCH WITH NO DATA;
    copy tmp_table FROM 'F:/Database/Database Project All/cric_final/api_data/match.csv' DELIMITER ',' CSV HEADER;
    INSERT INTO MATCH SELECT DISTINCT ON (match_id) * FROM tmp_table ON CONFLICT DO NOTHING;
    COMMIT;
END;
$$;

alter procedure init_matches() owner to postgres;

create or replace procedure init_all_match_data()
	language plpgsql
as $$
BEGIN

call init_teams();
call init_players();
call init_players_plays_for_teams();
call init_series();
call init_teams_play_in_series();
call init_umpires();
call init_matches();
call init_umpire_conducts_match();
    COMMIT;
END;
$$;



alter procedure init_all_match_data() owner to postgres;


create or replace function initialize_match(integer, character varying, integer, integer, integer, integer, character varying, character varying, date, integer, integer, integer, integer, integer, integer, integer, integer, integer, integer, integer, integer, integer, integer, integer, integer, integer, integer, integer, integer, integer, integer, integer, integer, integer, integer)
language plpgsql
as $$
DECLARE u_id INTEGER; f_name VARCHAR(100); nation VARCHAR(100);
BEGIN

  insert into match (match_id, match_type, team1_id, team2_id, captain1, captain2, venue, stadium_name, start_date, series_id)  values  ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10) on conflict do nothing;

  insert into match_performance_data (match_id, innings_no, team_id, player_id) values ($1, 1, $3, $11 ) on conflict do nothing;

  insert into player_plays_for_teams (team_id, player_id) VALUES ($3, $11) on conflict do nothing ;

   insert into match_performance_data (match_id, innings_no, team_id, player_id) values ($1, 1, $3, $12 ) on conflict do nothing;

  insert into player_plays_for_teams (team_id, player_id) VALUES ($3, $12) on conflict do nothing ;

   insert into match_performance_data (match_id, innings_no, team_id, player_id) values ($1, 1, $3, $13 ) on conflict do nothing;

  insert into player_plays_for_teams (team_id, player_id) VALUES ($3, $13) on conflict do nothing ;

   insert into match_performance_data (match_id, innings_no, team_id, player_id) values ($1, 1, $3, $14 ) on conflict do nothing;

  insert into player_plays_for_teams (team_id, player_id) VALUES ($3, $14) on conflict do nothing ;

   insert into match_performance_data (match_id, innings_no, team_id, player_id) values ($1, 1, $3, $15 ) on conflict do nothing;

  insert into player_plays_for_teams (team_id, player_id) VALUES ($3, $15) on conflict do nothing ;

   insert into match_performance_data (match_id, innings_no, team_id, player_id) values ($1, 1, $3, $16 ) on conflict do nothing;

  insert into player_plays_for_teams (team_id, player_id) VALUES ($3, $16) on conflict do nothing ;

   insert into match_performance_data (match_id, innings_no, team_id, player_id) values ($1, 1, $3, $17 ) on conflict do nothing;

  insert into player_plays_for_teams (team_id, player_id) VALUES ($3, $17) on conflict do nothing ;

   insert into match_performance_data (match_id, innings_no, team_id, player_id) values ($1, 1, $3, $18 ) on conflict do nothing;

  insert into player_plays_for_teams (team_id, player_id) VALUES ($3, $18) on conflict do nothing ;

   insert into match_performance_data (match_id, innings_no, team_id, player_id) values ($1, 1, $3, $19 ) on conflict do nothing;

  insert into player_plays_for_teams (team_id, player_id) VALUES ($3, $19) on conflict do nothing ;

   insert into match_performance_data (match_id, innings_no, team_id, player_id) values ($1, 1, $3, $20 ) on conflict do nothing;

  insert into player_plays_for_teams (team_id, player_id) VALUES ($3, $20) on conflict do nothing ;

   insert into match_performance_data (match_id, innings_no, team_id, player_id) values ($1, 1, $3, $21 ) on conflict do nothing;

  insert into player_plays_for_teams (team_id, player_id) VALUES ($3, $21) on conflict do nothing ;

  insert into match_performance_data (match_id, innings_no, team_id, player_id) values ($1, 2, $4, $22 ) on conflict do nothing;

  insert into player_plays_for_teams (team_id, player_id) VALUES ($4, $22) on conflict do nothing ;



    insert into match_performance_data (match_id, innings_no, team_id, player_id) values ($1, 2, $4, $23 ) on conflict do nothing;

  insert into player_plays_for_teams (team_id, player_id) VALUES ($4, $23) on conflict do nothing ;


    insert into match_performance_data (match_id, innings_no, team_id, player_id) values ($1, 2, $4, $24 ) on conflict do nothing;

  insert into player_plays_for_teams (team_id, player_id) VALUES ($4, $24) on conflict do nothing ;


    insert into match_performance_data (match_id, innings_no, team_id, player_id) values ($1, 2, $4, $25 ) on conflict do nothing;

  insert into player_plays_for_teams (team_id, player_id) VALUES ($4, $25) on conflict do nothing ;


    insert into match_performance_data (match_id, innings_no, team_id, player_id) values ($1, 2, $4, $26 ) on conflict do nothing;

  insert into player_plays_for_teams (team_id, player_id) VALUES ($4, $26) on conflict do nothing ;


    insert into match_performance_data (match_id, innings_no, team_id, player_id) values ($1, 2, $4, $27 ) on conflict do nothing;

  insert into player_plays_for_teams (team_id, player_id) VALUES ($4, $27) on conflict do nothing ;


    insert into match_performance_data (match_id, innings_no, team_id, player_id) values ($1, 2, $4, $28 ) on conflict do nothing;

  insert into player_plays_for_teams (team_id, player_id) VALUES ($4, $28) on conflict do nothing ;


    insert into match_performance_data (match_id, innings_no, team_id, player_id) values ($1, 2, $4, $29 ) on conflict do nothing;

  insert into player_plays_for_teams (team_id, player_id) VALUES ($4, $29) on conflict do nothing ;


    insert into match_performance_data (match_id, innings_no, team_id, player_id) values ($1, 2, $4, $30 ) on conflict do nothing;

  insert into player_plays_for_teams (team_id, player_id) VALUES ($4, $30) on conflict do nothing ;


    insert into match_performance_data (match_id, innings_no, team_id, player_id) values ($1, 2, $4, $31 ) on conflict do nothing;

  insert into player_plays_for_teams (team_id, player_id) VALUES ($4, $31) on conflict do nothing ;

  insert into match_performance_data (match_id, innings_no, team_id, player_id) values ($1, 2, $4, $32 ) on conflict do nothing;

  insert into player_plays_for_teams (team_id, player_id) VALUES ($4, $32) on conflict do nothing ;

  insert into umpires (player_id)  values ($33) on conflict do nothing;
  insert into umpires_conducts_match (match_id, player_id, umpiring_role)  values ($1, $33, 'umpire1');

  insert into umpires (player_id)  values ($34) on conflict do nothing;
  insert into umpires_conducts_match (match_id, player_id, umpiring_role)  values ($1, $34, 'umpire2');

  insert into umpires (player_id)  values ($35) on conflict do nothing;
  insert into umpires_conducts_match (match_id, player_id, umpiring_role)  values ($1, $35, 'umpire3');

END;
$$;

alter function initialize_match(integer, varchar, integer, integer, integer, integer, varchar, varchar, date, integer, integer, integer, integer, integer, integer, integer, integer, integer, integer, integer, integer, integer, integer, integer, integer, integer, integer, integer, integer, integer, integer, integer, integer, integer, integer)
  owner to postgres;



create or replace procedure destroy_db()
	language plpgsql
as $$
BEGIN
drop trigger update_match_count_on_umpires ON umpires_conducts_match;
drop procedure init_teams();
drop procedure init_players();
drop procedure init_players_plays_for_teams();
drop procedure init_series();
drop procedure init_teams_play_in_series();
drop procedure init_umpires();
drop procedure validate_umpire_fk(integer, varchar, varchar);
drop procedure init_umpire_conducts_match();
drop procedure init_matches();
drop procedure init_all_match_data();
drop procedure destroy_db();
drop function update_no_of_matches_umpired_trigger_function();
DROP TABLE match_performance_data;
DROP TABLE Umpires_Conducts_Match;
DROP TABLE MATCH;
DROP TABLE COACHES;
DROP TABLE UMPIRES;
DROP TABLE PLAYER_PLAYS_FOR_TEAMS;
DROP TABLE PLAYER_RANKING;
DROP TABLE TEAM_RANKING;
DROP TABLE TEAMS_PLAYS_IN_SERIES;
DROP TABLE SERIES;
DROP TABLE PLAYERS;
DROP TABLE TEAMS;

COMMIT;
END;
$$;

alter procedure destroy_db() owner to postgres;
