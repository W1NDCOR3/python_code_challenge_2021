# main.py or app.py

from fastapi import FastAPI
import httpx

OMDB_API_KEY = '428f05c3'  # Replace with your actual API key

app = FastAPI()

# Step 2: Define the function to fetch episode IDs
async def fetch_episode_ids():
    base_url = "http://www.omdbapi.com/"
    episode_ids = []

    async with httpx.AsyncClient() as client:  # Use the AsyncClient for async requests
        # Loop through seasons and episodes
        for season in range(1, 9):  # Game of Thrones has 8 seasons
            for episode in range(1, 11):  # Adjust this according to actual episodes
                response = await client.get(base_url, params={
                    't': 'Game of Thrones',
                    'season': season,
                    'episode': episode,
                    'apikey': OMDB_API_KEY
                })
                data = response.json()
                if 'Episode' in data:  # Check if the episode exists
                    episode_id = data['imdbID']
                    episode_ids.append(episode_id)
                    print(f"Season {season}, Episode {episode}: ID = {episode_id}")

    return episode_ids

# Step 3: Create a FastAPI endpoint to access this functionality
@app.get("/fetch-episode-ids")
async def get_episode_ids():
    episode_ids = await fetch_episode_ids()
    return {"episode_ids": episode_ids}

# Step 4: Define a function to fetch episode titles and ratings
async def fetch_episode_details(episode_ids):
    base_url = "http://www.omdbapi.com/"
    episode_details = []

    async with httpx.AsyncClient() as client:
        for episode_id in episode_ids:
            response = await client.get(base_url, params={
                'i': episode_id,
                'apikey': OMDB_API_KEY
            })
            data = response.json()
            if 'Title' in data and 'imdbRating' in data:  # Check if the response contains Title and Rating
                episode_details.append({
                    "id": episode_id,
                    "title": data['Title'],
                    "rating": data['imdbRating']
                })

    return episode_details

# Step 5: Create a FastAPI endpoint to get episode titles and ratings
@app.get("/fetch-episode-details")
async def get_episode_details():
    episode_ids = await fetch_episode_ids()  # Fetch episode IDs
    episode_details = await fetch_episode_details(episode_ids)  # Fetch details using IDs
    return {"episode_details": episode_details}

# Example of running the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
