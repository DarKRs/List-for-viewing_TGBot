import config
import sys
from KinoPoiskAPI.kinopoisk_api import KP

kinopoisk = KP(token=config.KINOPOISK_TOKEN)

def search_film_by_name(film):
    return kinopoisk.search(film)

def get_film_by_id(film_id):
    return kinopoisk.get_film(film_id)