import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Imposta le tue credenziali
client_id = '5ac01819a18e445c824ea3120d950b13'
client_secret = '15d8e6f00d0f4f858b4273d7456dd07c'

# Crea un oggetto di autenticazione
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)


sp = spotipy.Spotify(auth_manager=auth_manager)
artist_name = "Queen"
results = sp.search(q=artist_name, type='artist')

if results['artists']['items']:
    artist = results['artists']['items'][0]
    artist_genres = artist['genres']
    print(f"Generi dell'artista {artist_name}: {artist_genres}")
else:
    print(f"Artista '{artist_name}' non trovato.")
