import requests
import json
import math
import rich
from rich.console import Console
from rich.table import Table
import os

#Objekt Tabelle erzeugen
tableSongs = Table(title="Songs im Album")
tableAlbum = Table(title="Alben von Künstler")
tableArtist= Table(title="Künstler bei Suche")


#code abfrage ichman.de
status_code = 0
#solange abgrage nicht erfolgreich (!=200) token abrfragen
while status_code != 200:
    requesttoken = requests.get('https://token.ichmann.de')
    token = requesttoken.text
    status_code = requesttoken.status_code
#authoriaztion Header erzeugen
print(token)
headers = {'Authorization':f'Bearer {token}'}


#Nach Künstler suchen
input_artist = input("Artist: ")
search_artist = requests.get(f'https://api.spotify.com/v1/search?q=artist:{input_artist}&type=artist',headers=headers)
daten_artist = search_artist.json()


os.system('cls')
#Tabelle mit Künstlern
tableArtist.add_column("Nummer",justify="center", style="cyan")
tableArtist.add_column("Name", justify="center" ,style="cyan")
tableArtist.add_column("Popularität", justify="center",style="cyan")
i=0
for i in range((daten_artist['artists']['limit'])):
    #print(i)
    tableArtist.add_row(f'{i}',f'{daten_artist['artists']['items'][i]['name']}',f'{daten_artist['artists']['items'][i]['popularity']}')
    
    
#Tabelle Künstler Ausgeben
console = Console()
console.print(tableArtist)


#Artist auswählen
select_artist=daten_artist['artists']['limit']
while select_artist >=20 or select_artist<0:
    select_artist = int(input("Auswahl Artist: "))
os.system('cls')

artist_id = daten_artist['artists']['items'][select_artist]['id']


#Album von ausgewähltem Künstler anzeigen
search_album = requests.get(f'https://api.spotify.com/v1/artists/{artist_id}/albums?limit=50',headers=headers)
daten_album = search_album.json()


#Tabelle mit Alben
tableAlbum.add_column("Nummer",justify="center", style="cyan")
tableAlbum.add_column("Name", justify="center" ,style="cyan")
tableAlbum.add_column("Release", justify="center",style="cyan")
tableAlbum.add_column("Total Tracks", justify="center",style="cyan")
i=0
for i in range((daten_album['limit'])):
    tableAlbum.add_row(f'{i}',f'{daten_album['items'][i]['name']}',f'{daten_album['items'][i]['release_date']}',f'{daten_album['items'][i]['total_tracks']}')
    
    
##Tabelle mit Alben augsben
console = Console()
console.print(tableAlbum)


#Album auswählen
select_album=daten_album['limit']
while select_album >= daten_album['limit'] or select_album < 0:
    select_album = int(input("Auswahl Artist: "))
os.system('cls')

album_id = daten_album['items'][select_album]['id']


#Tracks von ausgewähltem Album anzeigen
search_tracks = requests.get(f'https://api.spotify.com/v1/albums/{album_id}?limit=50',headers=headers)
daten_tracks = search_tracks.json()


#Tabelle mit Alben
tableSongs.add_column("Nummer",justify="center", style="cyan")
tableSongs.add_column("Name", justify="center" ,style="cyan")
tableSongs.add_column("Dauer", justify="center",style="cyan")
i=0
for i in range((daten_tracks['limit'])):
    track_duration = f'{math.floor(daten_tracks['tracks']['items'][i]['duration_ms']/1000/60)}:{math.floor((daten_tracks['tracks']['items'][i]['duration_ms']/1000)%60)}'
    tableSongs.add_row(f'{i}',f'{daten_tracks['tracks'][i]['items']['name']}',f'{track_duration}')
    
    
##Tabelle mit Tracks augsben
console = Console()
console.print(tableSongs)




"""
search_track = requests.get(f'https://api.spotify.com/v1/albums/{album_id}',headers=headers)
daten_track= search_track.json()
track_name = daten_track['tracks']['items'][0]['name']
track_duration = daten_track['tracks']['items'][0]['duration_ms']

print(track_name)
print()
"""