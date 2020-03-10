import sqlite3
import pandas as pd
from data.data import DB_LOC


def init_db():
    db = get_db()

    with open("db/schema.sql") as f:
        db.executescript(f.read())


def get_db():
    db = sqlite3.connect(DB_LOC, detect_types=sqlite3.PARSE_DECLTYPES)
    db.row_factory = sqlite3.Row
    return db


def check_ticker_exists(symbol: str) -> bool:
    smb = (
        get_db()
        .execute(
            "select Symbol from stock_meta_data where Symbol=?", (symbol,)
        )
        .fetchone()
    )
    if smb:
        return smb[0] == symbol
    else:
        return False


def get_time_series_from_db(symbol: list = None):
    if symbol:
        return pd.read_sql(
            "select * from time_series where Symbol in ({})".format(
                ",".join(["'{}'".format(s) for s in symbol])
            ),
            con=get_db(),
        )
    else:
        return pd.read_sql("select * from time_series", con=get_db())


def get_symbols() -> list:
    return [
        a[0]
        for a in get_db()
        .execute("select distinct(Symbol) from stock_meta_data")
        .fetchall()
    ]


def get_regions() -> list:
    return [
        a[0]
        for a in get_db()
        .execute("select distinct(Region) from stock_meta_data")
        .fetchall()
    ]


def get_types() -> list:
    return [
        a[0]
        for a in get_db()
        .execute("select distinct(Type) from stock_meta_data")
        .fetchall()
    ]


def update_blacklisted(symbol: str):
    db = get_db()
    with db:
        db.execute(
            "insert into black_listed_symbols(Symbol) values (?)", (symbol,)
        )


def check_blacklisted(symbol: str) -> bool:
    smb = (
        get_db()
        .execute(
            "select Symbol from black_listed_symbols where Symbol=?", (symbol,)
        )
        .fetchone()
    )
    if smb:
        return smb[0] == symbol
    else:
        return False

