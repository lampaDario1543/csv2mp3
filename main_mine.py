from ytmusicapi import YTMusic
from pytube import YouTube
import os
import csv
import requests
from pydub import AudioSegment
import eyed3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime
import time as t
import sys #per prendere il path del file
import msvcrt #per chiudere il programma
from colorama import Fore, Style, init # per colorare gli errori
import sys
import json
from bs4 import BeautifulSoup

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="5ac01819a18e445c824ea3120d950b13",
                                                           client_secret="15d8e6f00d0f4f858b4273d7456dd07c"))
os.system("title csv2mp3")

init()#coloram
AudioSegment.ffmpeg = r"C:\PATH_Programs\ffmpeg.exe"
#caratteri proibiti e replace per il nome del file e della cartella

rules = [
    ('?', ''),
    ('<', '('),
    ('>', ')'),
    (':', ' -'),
    ('\\', ''),
    ('/', '-'),
    ('*', ''),
    ('"', ''),
    ('|', ''),
    ('.', '')
]

def get_song_lyrics(artist, song_title): #ottiene il testo di una canzone.
    artist = artist.lower().replace(' ', '-')
    song_title = song_title.lower().replace(' ', '-')
    url = f"https://lyrics.lyricfind.com/lyrics/{artist}-{song_title}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tag = soup.find("script", id="__NEXT_DATA__", type="application/json")
        if script_tag:
            json_data = json.loads(script_tag.string)
            try:
                lyrics = json_data['props']['pageProps']['songData']['track']['lyrics']
                return lyrics
            except KeyError:
                print("Lyrics not found.")
                return ""
        else:
            print("Script tag not found.")
            return ""
    else:
        print("Failed to retrieve lyrics.")
        return ""

def getCsvPath(): #ottengo il percorso del file csv tramite argomenti
    if len(sys.argv) < 2:
        print("Inserisci il percorso del file csv:")
        path=input("> ")
        if(not path.lower().endswith('.csv')):
            print(f"{Fore.RED}Errore: Il file deve essere un csv.{Style.RESET_ALL}\n\n")
            return None
        elif(not os.path.exists(path)):
            print(f"{Fore.RED}Errore: Il file non esiste.{Style.RESET_ALL}\n\n")
            return None
        return path
    path = ' '.join(sys.argv[1:])
    if(not path.lower().endswith('.csv')):
        print(f"{Fore.RED}Errore: Il file deve essere un csv.{Style.RESET_ALL}\n\n")
        return None
    if(not os.path.exists(path)):
        print(f"{Fore.RED}Errore: Il file non esiste.{Style.RESET_ALL}\n\n")
        return None
    return path

def run(path):
    songs=getCSV(path)
    DIM=len(songs)
    if not os.path.exists('csv2mp3/'):
        os.mkdir('csv2mp3/')
    for i in range(DIM):
        print("Download "+str(i+1)+" di "+str(DIM)+" - "+ str(((i+1)/DIM)*100)[0:4]+"% canzoni scaricate, mancanti: "+str(DIM-(i+1)))
        video_url = getUrl(songs[i]['title']+' '+songs[i]['artist'],songs[i])
        
        #rimuovo i caratteri proibiti per il nome del file e della cartella

        for rule in rules:
            songs[i]['title']=songs[i]['title'].replace(rule[0],rule[1])
            songs[i]['album']=songs[i]['album'].replace(rule[0],rule[1])

        track=getInfo(songs[i]['title']+' '+songs[i]['artist'])
        if not os.path.exists('csv2mp3/'+songs[i]['album']): #se la cartella dell'album non esiste
            os.mkdir("csv2mp3/"+songs[i]['album']) #creo la cartella col nome dell'album
            img=open("csv2mp3/"+songs[i]['album']+"/thumb.jpg","wb") #creo l'immagine dell'album
            response=requests.get(track['album']['images'][0]['url']) #richiedo l'url dell'immagine dell'album
            img.write(response.content) #scrivo l'immagine
            img.close() #chiudo l'immagine
        
        #scarico la canzone

        filename = f"csv2mp3/{songs[i]['album']}/{songs[i]['title']}.temp" #creo il file temporaneo
        video = YouTube(video_url) #ottengo il video
        audio_streams = video.streams.filter(only_audio=True)
        audio_streams = audio_streams.order_by('abr')
        highest_quality_audio = audio_streams.last()
        highest_quality_audio.download(filename=filename)
        print("Download complete..."+songs[i]['title'])
        os.system('cls')

        #converto il file in mp3

        print("Conversione di "+songs[i]['title']+" in mp3")
        audio=AudioSegment.from_file("csv2mp3/"+songs[i]['album']+"/"+songs[i]['title']+".temp")
        audio.export("csv2mp3/"+songs[i]['album']+"/"+songs[i]['title']+".mp3", format="mp3")
        os.remove("csv2mp3/"+songs[i]['album']+"/"+songs[i]['title']+".temp")

        #aggiungo le informazioni alla canzone

        print("\nAggiunta dati a: "+str(i+1))
        audio=eyed3.load("csv2mp3/"+songs[i]['album']+"/"+songs[i]['title']+".mp3")
        audio.tag.title=track['name']
        audio.tag.album=track['album']['name']
        audio.tag.artist=songs[i]['artist']
        audio.tag.track_num=track['track_number'], track['album']['total_tracks']
        audio.tag.recording_date=int(track['album']['release_date'][0:4])
        audio.tag.lyrics.set(get_song_lyrics(songs[i]['artist'], songs[i]['title']))
        with open("csv2mp3/"+songs[i]['album']+"/thumb.jpg", "rb") as cover_art:
            audio.tag.images.set(3, cover_art.read(), "image/jpeg")
        audio.tag.save()
        os.system('cls')

        #aggiorno il file last.txt con l'ultima canzone scaricata

        last=open("last.txt","w",encoding="utf8")
        last.write(track['name'])
        last.write("\n"+str(datetime.today()));
        last.close()
    print("Download completato con successo!\n\n")
    print("Premi un tasto per uscire...")
    msvcrt.getch()
    sys.exit()

def getUrl(title, song): #ottengo l'url del video
    ytmusic = YTMusic()
    ytmusic=YTMusic()
    url="https://music.youtube.com/watch?v="
    temp=str(ytmusic.search(title,"songs"))
    url+=temp[temp.find("videoId")+11:temp.find("videoId")+22]
    song['imgUrl']=imgUrl=temp[temp.find("https://lh3.googleusercontent.com/"):temp.find("w60-h60-l90-rj")]+"w544-h544-l90-rj" #ottengo l'url dell'immagine della canzone
    return url


def getCSV(file:str) -> list: #ritorno la lista di canzoni presa dal file csv
    songs = []
    with open(file, "r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            songs.append(row)
        if(len(songs)==0):
            print(f"{Fore.RED}Errore: Il file '{file}' è vuoto.{Style.RESET_ALL}\n\n")
            print("Premi un tasto per uscire...")
            msvcrt.getch()
            sys.exit()
        required_fields = ['title', 'artist', 'album']
        if(len(songs[0].keys())!=len(required_fields)):
            print(f"{Fore.RED}Errore: I campi del file devono essere: {len(required_fields)} {Style.RESET_ALL}\n\n")
            print("Premi un tasto per uscire...")
            msvcrt.getch()
            sys.exit()
        for r in required_fields:
            try:
                songs[0][r]
            except Exception as e:
                print(f"{Fore.RED}Errore: I campi del file devono essere: {required_fields} {Style.RESET_ALL}\n\n")
                print("Premi un tasto per uscire...")
                msvcrt.getch()
                sys.exit()
    return songs

def getInfo(title): #ritorno le informazioni della canzone
    results = sp.search(q=title, limit=1)
    for idx, track in enumerate(results['tracks']['items']):
        print(str(track['name']))
    return track

if __name__=='__main__':
    path=getCsvPath() #ottengo il percorso del file csv
    if(path==None):
        print("Premi un tasto per uscire...")
        msvcrt.getch()
        sys.exit()
    else:
        run(path)