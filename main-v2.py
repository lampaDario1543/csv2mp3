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

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="5ac01819a18e445c824ea3120d950b13",
                                                           client_secret="15d8e6f00d0f4f858b4273d7456dd07c"))

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


def run():
    #CHANGE FILE TITLE.
    songs=getCSV("titles.csv")
    DIM=len(songs)
    for i in range(DIM):
        print("Download "+str(i+1)+" di "+str(DIM)+" - "+ str(((i+1)/DIM)*100)[0:4]+"% canzoni scaricate, mancanti: "+str(DIM-(i+1)))
        video_url = getUrl(songs[i]['title']+' '+songs[i]['artist'],songs[i])
        
        for rule in rules:
            songs[i]['title']=songs[i]['title'].replace(rule[0],rule[1])
            songs[i]['album']=songs[i]['album'].replace(rule[0],rule[1])

        track=getInfo(songs[i]['title']+' '+songs[i]['artist'])
        if not os.path.exists(songs[i]['album']):
            os.mkdir(songs[i]['album'])
            img=open(songs[i]['album']+"/thumb.jpg","wb")
            response=requests.get(track['album']['images'][0]['url'])
            img.write(response.content)
            img.close()
        
        
        filename = f"{songs[i]['album']}/{songs[i]['title']}.temp"
        video = YouTube(video_url)
        audio_streams = video.streams.filter(only_audio=True)
        audio_streams = audio_streams.order_by('abr')
        highest_quality_audio = audio_streams.last()
        highest_quality_audio.download(filename=filename)
        print("Download complete..."+songs[i]['title'])
        os.system('cls')
        print("Conversione di "+songs[i]['title']+" in mp3")
        audio=AudioSegment.from_file(songs[i]['album']+"/"+songs[i]['title']+".temp")
        audio.export(songs[i]['album']+"/"+songs[i]['title']+".mp3", format="mp3")
        os.remove(songs[i]['album']+"/"+songs[i]['title']+".temp")
        print("\nAggiunta dati a: "+str(i+1))
        audio=eyed3.load(songs[i]['album']+"/"+songs[i]['title']+".mp3")
        audio.tag.title=track['name']
        audio.tag.album=track['album']['name']
        audio.tag.artist=songs[i]['artist']
        audio.tag.track_num=track['track_number'], track['album']['total_tracks']
        audio.tag.recording_date=int(track['album']['release_date'][0:4])
        with open(songs[i]['album']+"/thumb.jpg", "rb") as cover_art:
            audio.tag.images.set(3, cover_art.read(), "image/jpeg")
        audio.tag.save()
        os.system('cls')
        last=open("last.txt","w",encoding="utf8")
        last.write(track['name'])
        last.write("\n"+str(datetime.today()));
        last.close()

def getUrl(title, song):
    ytmusic = YTMusic()
    url="https://music.youtube.com/watch?v="
    temp=str(ytmusic.search(title,"songs"))
    url+=temp[temp.find("videoId")+11:temp.find("videoId")+22]
    song['imgUrl']=imgUrl=temp[temp.find("https://lh3.googleusercontent.com/"):temp.find("w60-h60-l90-rj")]+"w544-h544-l90-rj"
    return url



def getCSV(file:str) -> list:
	songs = []
	with open(file,"r",encoding="utf-8") as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for x in csv_reader:
			songs.append(x)
	return songs

def getInfo(title):
    results = sp.search(q=title, limit=1)

    for idx, track in enumerate(results['tracks']['items']):
        print(str(track['name']))
    return track

if __name__=='__main__':
    run()