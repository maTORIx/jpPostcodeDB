# jpPostcode.py
# These codes are licensed under CC0.
# http://creativecommons.org/publicdomain/zero/1.0/deed.ja

from datetime import date, datetime
import sqlite3
import urllib.request
import tempfile, zipfile, shutil, csv, io, sys, os, re, datetime

DEFAULT_POSTCODE_DATA_URL = (
    "https://www.post.japanpost.jp/zipcode/dl/kogaki/zip/ken_all.zip"
)
DB_NAME = "jpPostcode.db"
UPDATEAT_FILE_PATH = os.path.join(os.path.dirname(__file__), ".updateat")
DB_INIT_SQL = """
CREATE TABLE IF NOT EXISTS postcodes(
    id integer PRIMARY KEY AUTOINCREMENT,
    postcode integer NOT NULL,
    prefecture text NOT NULL,
    prefecture_kana text NOT NULL,
    municipalities text NOT NULL,
    municipalities_kana text NOT NULL,
    town_area text NOT NULL,
    town_area_kana text NOT NULL,
    unique(postcode, prefecture, municipalities, town_area)
);
"""
DB_INSERT_SQL = """
INSERT OR IGNORE INTO postcodes(
    postcode,
    prefecture,
    prefecture_kana,
    municipalities,
    municipalities_kana,
    town_area,
    town_area_kana
) values(?, ?, ?, ?, ?, ?, ?);
"""
DB_SELECT_SQL = """
SELECT
    postcode,
    prefecture,
    prefecture_kana,
    municipalities,
    municipalities_kana,
    town_area,
    town_area_kana
FROM postcodes WHERE postcode = ?
"""


def fetch_postcode_data(url, callback):
    with urllib.request.urlopen(url) as response:
        with tempfile.NamedTemporaryFile() as temp_file:
            shutil.copyfileobj(response, temp_file)
            return callback(temp_file)


def read_postcode_data(f, callback):
    with zipfile.ZipFile(f, "r") as zip:
        with zip.open(zip.namelist()[0]) as f:
            return callback(io.TextIOWrapper(f))


def generate_postcode_db(url):
    init_db()
    callback = lambda f: read_postcode_data(f, insert_csv)
    fetch_postcode_data(url, callback)


def select_postcode(postcode):
    if type(postcode) is not int:
        postcode = int(postcode)
    con = sqlite3.connect(DB_NAME)
    return con.cursor().execute(DB_SELECT_SQL, (postcode,))


def replace_columns(row):
    return (
        int(row[2]),  # postcode
        row[6],  # prefecture
        row[3],  # prefecture_kana
        row[7],  # municipalities
        row[4],  # municipalities_kana
        row[8],  # town_area
        row[5],  # town_area_kana
    )


def init_db():
    con = sqlite3.connect("jpPostcode.db")
    cur = con.cursor()
    cur.execute(DB_INIT_SQL)
    con.commit()


def insert_csv(f):
    init_db()
    con = sqlite3.connect("jpPostcode.db")
    reader = csv.reader(f)
    for row in reader:
        con.cursor().execute(DB_INSERT_SQL, replace_columns(row))
    con.commit()
    con.close()


def write_updateat():
    with open(UPDATEAT_FILE_PATH, "w") as f:
        f.write(datetime.date.today().isoformat())


def read_updateat():
    longtime_ago = datetime.date.today() - datetime.timedelta(days=999)
    if not os.path.exists(UPDATEAT_FILE_PATH):
        return longtime_ago
    with open(UPDATEAT_FILE_PATH, "r") as f:
        try:
            return datetime.date.fromisoformat(f.read())
        except:
            return longtime_ago


def is_updatable():
    update_at = read_updateat()
    today = datetime.date.today()
    if today.month != update_at.month:
        return True
    elif today - update_at > datetime.timedelta(days=32):
        return True
    elif not os.path.exists("jpPostcode.db"):
        return True
    else:
        return False


if __name__ == "__main__":
    if is_updatable():
        generate_postcode_db(DEFAULT_POSTCODE_DATA_URL)  # generate or update
        write_updateat()
    if len(sys.argv) > 1:
        target = sys.argv[1]
        if not re.match(r"^[0-9]+$", target):
            print("Unexpected postcode.")
        else:
            for result in select_postcode(target):
                print(result)
