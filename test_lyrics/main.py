'''
import lyricsgenius as lg

API_TOKEN="QU18sqNtEhT2H9F_Zd9aBa6GeMEdPY4aWAu47tdvEr5NuLvNCGO_u9xSd-FZFpLu"
genius = lg.Genius(API_TOKEN, skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"], remove_section_headers=True,verbose=False)

song=genius.search_song(title="Shape of you", artist="Ed sheeran", get_full_info=False)
if song is not None:
    lyr=song.lyrics
    print(lyr)
else:
    print("No testo")

import requests

def get_lyrics(song_title, artist):
    base_url = "https://api.genius.com"
    search_url = f"{base_url}/search"
    headers={
        "Authorization":"Bearer QU18sqNtEhT2H9F_Zd9aBa6GeMEdPY4aWAu47tdvEr5NuLvNCGO_u9xSd-FZFpLu"
    }
    params = {
        "q": f"{song_title} {artist}"
    }
    response = requests.get(search_url, params=params,headers=headers)
    print(response.status_code)
    if response.status_code == 304 or response.status_code == 200:
        data = response.json()
        hits = data["response"]["hits"]
        
        for hit in hits:
            song_info = hit["result"]
            if song_info["title"].lower() == song_title.lower() and song_info["primary_artist"]["name"].lower() == artist.lower():
                song_id = song_info["id"]
                break
        else:
            return f"Song not found: {song_title} by {artist}."
        
        lyrics_url = f"{base_url}/songs/{song_id}"
        headers={
            "access_token": "QU18sqNtEhT2H9F_Zd9aBa6GeMEdPY4aWAu47tdvEr5NuLvNCGO_u9xSd-FZFpLu" 
        }
        response_lyrics = requests.get(lyrics_url, headers=headers)
        if response_lyrics.status_code == 200:
            lyrics_data = response_lyrics.json()
            song_path = lyrics_data["response"]["song"]["path"]
            lyrics_page_url = f"{base_url}{song_path}"
            
            response_lyrics_page = requests.get(lyrics_page_url)
            if response_lyrics_page.status_code == 200:
                lyrics_page = response_lyrics_page.text
                start_tag = '<div class="lyrics">'
                end_tag = '<div class="rg_embed_footer">'
                start_index = lyrics_page.find(start_tag)
                end_index = lyrics_page.find(end_tag)
                
                if start_index != -1 and end_index != -1:
                    lyrics = lyrics_page[start_index + len(start_tag):end_index].strip()
                    lyrics = lyrics.replace("<br/>", "\n")
                    return lyrics
                else:
                    return f"Lyrics not found for {song_title} by {artist}."
            else:
                return f"Failed to retrieve lyrics page for {song_title} by {artist}."
        else:
            return f"Failed to retrieve lyrics for {song_title} by {artist}."
    else:
        return "Error retrieving search results from Genius."

# Usage example
song_title = "Il cielo d'irlanda"
artist = "Fiorella Mannoia"
result = get_lyrics(song_title, artist)
print(result)
'''

import requests

client_access_token = 'QU18sqNtEhT2H9F_Zd9aBa6GeMEdPY4aWAu47tdvEr5NuLvNCGO_u9xSd-FZFpLu'
base_url = 'https://api.genius.com'

user_input = input('artist and song: ').replace(" ", "-")

path = 'search/'
request_uri = '/'.join([base_url, path])
print(request_uri + user_input)

params = {'q': user_input}

token = 'Bearer {}'.format(client_access_token)
headers = {'Authorization': token}

r = requests.get(request_uri, params=params, headers=headers)
print(r.text)