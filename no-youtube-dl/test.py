from pytube import YouTube

url = "https://music.youtube.com/watch?v=VyV54YwPAkk&list=RDAMVMVRpptE7F9I0"
video = YouTube(url)
audio_stream = video.streams.filter(only_audio=True).first()
audio_stream.download(filename="scrauso.mp3")
'''

from pytube import YouTube

url = "https://music.youtube.com/watch?v=VyV54YwPAkk&list=RDAMVMVRpptE7F9I0"
video = YouTube(url)

# Filtra solo le tracce audio
audio_streams = video.streams.filter(only_audio=True)

# Ordina le tracce audio per bitrate (maggiore è meglio)
audio_streams = audio_streams.order_by('abr')

# Ottieni la traccia audio con la qualità massima
highest_quality_audio = audio_streams.last()

# Scarica l'audio con la qualità massima
highest_quality_audio.download(filename="nome_file.mp3")
'''
