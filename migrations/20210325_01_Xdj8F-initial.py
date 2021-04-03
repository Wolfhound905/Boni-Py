"""
Initial
"""

from yoyo import step, transaction

__depends__ = {}

steps = [
    step("""
        CREATE TABLE stats (
                season INT PRIMARY KEY NOT NULL,
                wins INT NOT NULL,
                losses INT NOT NULL,
                win_streak INT NOT NULL,
                loss_streak INT NOT NULL,
                max_win_streak INT NOT NULL,
                max_loss_streak INT NOT NULL);
        """,
        "DROP TABLE stats;"),
        
    step(
        """
        CREATE TABLE user_xp (
                id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                user_id BIGINT NOT NULL,
                timestamp DATETIME NOT NULL,
                xp INT NOT NULL);
        """,
        "DROP TABLE user_xp;"),

        step("""
            CREATE TABLE voice_channels (
                active_vc bigint(20) UNSIGNED NOT NULL PRIMARY KEY
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        """,
        "DROP TABLE voice_channels;"),

]
