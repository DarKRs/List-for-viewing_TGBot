#No longer in use

import config
import sys
from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.request.films.film_request import FilmRequest
from kinopoisk_unofficial.request.films.search_by_keyword_request import SearchByKeywordRequest
from kinopoisk_unofficial.model.filter_country import FilterCountry
from kinopoisk_unofficial.model.filter_order import FilterOrder
from kinopoisk_unofficial.request.films.film_search_by_filters_request import FilmSearchByFiltersRequest
from kinopoisk_unofficial.request.films.seasons_request import SeasonsRequest

api_client = KinopoiskApiClient(config.KINOPOISK_TOKEN)

def search_film_api(film):
    request = FilmSearchByFiltersRequest()
    request.keyword = film
    response = api_client.films.send_film_search_by_filters_request(request)
    return response.items


def getGenres(film_id):
    try:
        request = FilmRequest(film_id)
        response = api_client.films.send_film_request(request)
        return response.film.genres
    except Exception as e:
        print(repr(e))
        return 

def getCategory(film_id):
    genres = str(getGenres(film_id))
    if 'аниме' in genres:
        return "Аниме"  
    elif 'мультфильм' in genres:
        return "Мультфильм"
    elif 'сериал' in genres:
        return "Сериал"
    else:
        return "Фильм"

def getDescription(film_id):
    try:
        request = FilmRequest(film_id)
        response = api_client.films.send_film_request(request)
        return response.film.description
    except Exception as e:
        print(repr(e))
        return 


def getYear(film_id):
    try:
        request = FilmRequest(film_id)
        response = api_client.films.send_film_request(request)
        return response.film.year
    except Exception as e:
        print(repr(e))
        return 

def getFullName(film_id):
    try:
        request = FilmRequest(film_id)
        response = api_client.films.send_film_request(request)
        if response.film.name_original is None:
            return response.film.name_ru + " ( )" 
        else:
            return response.film.name_ru + " (" + response.film.name_original + ")" 
    except Exception as e:
        print(repr(e))
        return 

def getName_ru(film_id):
    try:
        request = FilmRequest(film_id)
        response = api_client.films.send_film_request(request)
        return response.film.name_ru
    except Exception as e:
        print(repr(e))
        return 

def getName_orig(film_id):
    try:
        request = FilmRequest(film_id)
        response = api_client.films.send_film_request(request)
        return response.film.name_original
    except Exception as e:
        print(repr(e))
        return 

def getUrl(film_id):
    try:
        request = FilmRequest(film_id)
        response = api_client.films.send_film_request(request)
        return response.film.web_url
    except Exception as e:
        print(repr(e))
        return     
