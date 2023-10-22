# Csv2mp3

## Index:

- [Introduction](#intro)
- [Sample of input](#sample)
- [License](#licese)
- [Releases](https://github.com/lampaDario1543/csv2mp3/releases)

---

## Introduction:

This python program take a CSV file in input with songs, artist and album, and return a folder with the songs downloaded in .mp3 (quality 124 kbps), it inserts autmatically these mp3 tags:

- Title
- Artist
- Album
- Year
- Number of Track
- Album Cover

Example:

![sample-1](image/README/1697921399898.png)

## Sample of input:

The CSV file needs to contain 3 fields: title, artist and album, and then you can add how many rows do you want.

E.G.

`titles.csv`

| title                    | artist          | album                      |
| ------------------------ | --------------- | -------------------------- |
| Never Gonna Give You Up  | Rick Astley     | Whenever You Need Somebody |
| I'm gonna Be (500 Miles) | The Proclaimers | Sunshine on Leith          |

## How to use it:

#### From source code:

First of all you have to download `requirements.txt` file from

To use the program, simply run the command `python main.py file_path.csv` and provide the path to the CSV file as a command-line argument, if you don't, the program will detect that and will ask you for the path of the CSV file. The program will generate a folder on the desktop called `csv2mp3`, with other subfolders that are the names of the albums in the CSV file, in the folder there will be the mp3 file and an image `thumb.jpg`, which is the album cover.

#### From release:

If you don't want to download the source code, you can download a release from [here](https://github.com/lampaDario1543/csv2mp3/releases), you can download the `setup.exe`, after you have downloaded it you've to run it and it will install the program in your program folder.

⚠ It's important to give administrator permissions to the program, because when you run it creates `.cache` file for spotipy library, and needs admin permissions to create it and edit it.

## License:
