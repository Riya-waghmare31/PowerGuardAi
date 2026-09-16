import sqlite3
from pathlib import Path

import pandas as pd


def initialize_database(path: str = "powerguard.db") -> None:
    connection = sqlite3.connect(path)
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS processing_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            processed_at TEXT DEFAULT CURRENT_TIMESTAMP,
            record_count INTEGER NOT NULL
        )
        """
    )
    connection.commit()
    connection.close()


def log_processing(record_count: int, path: str = "powerguard.db") -> None:
    connection = sqlite3.connect(path)
    connection.execute(
        "INSERT INTO processing_log (record_count) VALUES (?)",
        (record_count,),
    )
    connection.commit()
    connection.close()


def export_sqlite(df: pd.DataFrame, path: str = "powerguard.db") -> None:
    connection = sqlite3.connect(path)
    df.to_sql("analyzed_records", connection, if_exists="replace", index=False)
    connection.commit()
    connection.close()
