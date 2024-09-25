import httpx
from .models import Episode

OMDB_API_URL = "https://www.omdbapi.com/"
OMDB_API_KEY = "428f05c3"

def fetch_episode_data(season, episode):
    params = {
        'apikey': OMDB_API_KEY,
        'i': 'tt0944947',  # Game of Thrones IMDb ID
        'Season': season,
        'Episode': episode,
    }
    response = httpx.get(OMDB_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get("Response", "False") == "True":
            return data
    return None

def save_episode_data(season, episode):
    data = fetch_episode_data(season, episode)
    if data:
        Episode.objects.create(
            title=data['Title'],
            imdb_id=data['imdbID'],
            runtime=data['Runtime'],
            rating=data['imdbRating']
        )
