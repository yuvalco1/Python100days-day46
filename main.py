from pprint import pprint
import re

import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth


travel_date = input ("Which date do you want to travel to? Type in YYYY-MM-DD format: ")
travel_date_year = travel_date[:4]
url = "https://www.billboard.com/charts/hot-100/" + travel_date + "/"

# billboard url example https://www.billboard.com/charts/hot-100/1990-08-12/

headers = {'user-agent': 'my-app/0.0.1'}
response = requests.get(url=url, headers=headers)

song_html = response.text
song_soup = BeautifulSoup(song_html, "html.parser")


song_titles = song_soup.find_all(name="div", class_="o-chart-results-list-row-container")

song_names =[song.find(name="h3",id="title-of-a-story").get_text(strip=True) for song in song_titles]

print (song_names)
artist_names = [song.find_all(name="span", class_=re.compile("c-label"))[1].get_text(strip=True).split("(")[0] for song in song_titles]
print (artist_names)

spotify_client_id = "f8eff7f2e6a6408692181ed953a5d578"
spotify_client_secret = "94e7dc4032ed42dfb65a8c86237efed0"
my_spotify_id = "21lvv76q7swazoiyutj3kgjti"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(username="Yuval cohen",client_id=spotify_client_id, client_secret=spotify_client_secret, redirect_uri="https://www.example.com", scope="playlist-modify-public", show_dialog=True, open_browser=True, cache_path="token.txt"))
songs_links = []
user_id = sp.current_user()['id']

# search for songs in spotify
for i in range(len(song_names)):
    search_results = sp.search(q=f"{song_names[i]} artist:{artist_names[i]}", limit=1, type="track", market="US")
    #pprint(search_results)
    try:
        #song_link = search_results['tracks']['items'][0]['external_urls']['spotify'].strip("https://open.spotify.com/track/")
        song_link = search_results['tracks']['items'][0]['uri']
        songs_links.append(song_link)
    except IndexError:
        #songs_links.append("Not found")
        print("Not found")
print(songs_links)

# create a playlist in spotify
playlist_name = (f"{travel_date} Billboard 100")
print(user_id)
playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True, collaborative=False, description="Billboard 100 Hot 100 songs for " + travel_date)
playlist_id = playlist['id']
sp.playlist_add_items(playlist_id, songs_links)
