"""
better-db
"""

from yoyo import step

__depends__ = {'20210325_01_Xdj8F-initial'}

steps = [
    step("""
            CREATE TABLE matches (
                id int(10) UNSIGNED NOT NULL,
                win tinyint(1) NOT NULL,
                overtime tinyint(1) DEFAULT NULL,
                match_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        """,
        "DROP TABLE matches;"),

    step("""
            CREATE TABLE seasons (
                id int(10) UNSIGNED NOT NULL,
                number int(10) UNSIGNED NOT NULL,
                date_start timestamp NOT NULL,
                date_end timestamp NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        """,
        "DROP TABLE seasons;"),

    step("""
            CREATE TABLE users_matches (
                user_id bigint(20) UNSIGNED NOT NULL,
                match_id int(10) UNSIGNED NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        """,
        "DROP TABLE users_matches;"),

    step("""
        ALTER TABLE matches
        ADD PRIMARY KEY (id);
        """),

    step("""
        ALTER TABLE seasons
        ADD PRIMARY KEY (id);
        """),

    step("""
        ALTER TABLE users_matches
        ADD PRIMARY KEY (user_id,match_id),
        ADD KEY users_matches_FK (match_id);
        """),

    step("""
        ALTER TABLE matches
        MODIFY id int(10) UNSIGNED NOT NULL AUTO_INCREMENT;
        """),

    step("""
        ALTER TABLE seasons
        MODIFY id int(10) UNSIGNED NOT NULL AUTO_INCREMENT;
        """),

    step("""
        ALTER TABLE users_matches
        ADD CONSTRAINT users_matches_FK FOREIGN KEY (match_id) REFERENCES matches (id);
        """),

    ]
