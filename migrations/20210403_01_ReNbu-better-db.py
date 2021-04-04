"""
better-db
"""

from yoyo import step

__depends__ = {'20210325_01_Xdj8F-initial'}

steps = [
    step("""
            CREATE TABLE matches (
                id int(10) UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
                win tinyint(1) NOT NULL,
                overtime tinyint(1) DEFAULT NULL,
                match_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        """,
        "DROP TABLE matches;"),

    step("""
            CREATE TABLE seasons (
                id int(10) UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
                number int(10) UNSIGNED NOT NULL,
                date_start timestamp NOT NULL,
                date_end timestamp NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        """,
        "DROP TABLE seasons;"),

    step("""
            CREATE TABLE users_matches (
                user_id bigint(20) UNSIGNED NOT NULL,
                match_id int(10) UNSIGNED NOT NULL,

                PRIMARY KEY (user_id, match_id),
                CONSTRAINT users_matches_FK FOREIGN KEY (match_id) REFERENCES matches (id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        """,
        "DROP TABLE users_matches;"),

        #Remove now redundant table
        step("DROP TABLE stats;",
        """
        CREATE TABLE stats (
                season INT PRIMARY KEY NOT NULL,
                wins INT NOT NULL,
                losses INT NOT NULL,
                win_streak INT NOT NULL,
                loss_streak INT NOT NULL,
                max_win_streak INT NOT NULL,
                max_loss_streak INT NOT NULL);
        """)
    ]
