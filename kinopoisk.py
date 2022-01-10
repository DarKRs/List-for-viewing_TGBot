import config
import sys
from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.request.films.film_request import FilmRequest
from kinopoisk_unofficial.request.films.search_by_keyword_request import SearchByKeywordRequest
from kinopoisk_unofficial.model.filter_country import FilterCountry
from kinopoisk_unofficial.model.filter_order import FilterOrder
from kinopoisk_unofficial.request.films.film_search_by_filters_request import FilmSearchByFiltersRequest

api_client = KinopoiskApiClient(config.KINOPOISK_TOKEN)

def search_film_api(film):
    request = FilmSearchByFiltersRequest()
    request.keyword = film
    response = api_client.films.send_film_search_by_filters_request(request)
    return response.items


def getCategory(film_id):
    request = FilmRequest(film_id)
    response = api_client.films.send_film_request(request)
    return response.film.genres[0]

def getDescription(film_id):
    request = FilmRequest(film_id)
    response = api_client.films.send_film_request(request)
    return response.film.description

def getYear(film_id):
    request = FilmRequest(film_id)
    response = api_client.films.send_film_request(request)
    return response.film.year

def getFullName(film_id):
    request = FilmRequest(film_id)
    response = api_client.films.send_film_request(request)
    return response.film.name_ru + " (" + response.film.name_original + ")" 

def getName_ru(film_id):
    request = FilmRequest(film_id)
    response = api_client.films.send_film_request(request)
    return response.film.name_ru

def getName_orig(film_id):
    request = FilmRequest(film_id)
    response = api_client.films.send_film_request(request)
    return response.film.name_original

def getUrl(film_id):
    request = FilmRequest(film_id)
    response = api_client.films.send_film_request(request)
    return response.film.web_url