import csv
import requests
import datetime
from dateutil import parser

from src.database.setup import SessionLocal
from src.database.setup import engine

import src.models as models
from src.models.base import Base

Base.metadata.create_all(bind=engine)

API_KEY = "41d39b28"
db = SessionLocal()


def get_img(name: str):
    response = requests.get(
        f"http://www.omdbapi.com/?t={name.replace(' ', '+')}&apikey={API_KEY}"
    )
    if response:
        json = response.json()

        if (
            "Title" not in json
            or "Director" not in json
            or "Released" not in json
            or "Poster" not in json
            or "Plot" not in json
            or "Runtime" not in json
            or "N/A"
            in [
                json["Title"],
                json["Director"],
                json["Released"],
                json["Poster"],
                json["Plot"],
                json["Runtime"],
            ]
        ):
            return None

        return json

    return None


def add_to_database(json):
    try:
        date = parser.parse(json["Released"])
        length = json["Runtime"].split(" ")[0]

        movie = models.Movie(
            title=json["Title"],
            director=json["Director"],
            length=int(length),
            poster_url=json["Poster"],
            summary=json["Plot"],
            release_date=datetime.date(date.year, date.month, date.day),
        )

        db.add(movie)
        db.commit()
    except Exception as e:
        print(e)


with open("./initializer/IMDB-Movie-Data.csv", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    names = []
    row_num = 0

    for row in reader:
        if row_num == 0:
            for col in row:
                names.append(col)
        else:
            entry = dict()
            for idx, col in enumerate(row):
                entry[names[idx]] = col

            json = get_img(entry["Title"])
            if json is not None:
                add_to_database(json)

        row_num += 1
