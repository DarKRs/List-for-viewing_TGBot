import config
from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.request.films.film_request import FilmRequest
from kinopoisk_unofficial.request.films.search_by_keyword_request import SearchByKeywordRequest

api_client = KinopoiskApiClient(config.KINOPOISK_TOKEN)

def search_film_api(film):
    request = SearchByKeywordRequest(film)
    response = api_client.films.send_search_by_keyword_request(request)
    return 'https://www.kinopoisk.ru/film/' + response.films[0].kinopoisk_id

def getCategory(film_id):
    request = FilmRequest(film_id)
    response = api_client.films.send_film_request(request)
    return "test"