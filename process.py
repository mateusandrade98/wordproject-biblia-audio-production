import requests
from zipfile import ZipFile
from pathlib import Path
import shutil
import os
from os import listdir
from os.path import isfile, join
from dotenv import dotenv_values


# https://github.com/joandesonandrade/biblia-api
config = dotenv_values(".env")

response = requests.get(url="/".join((config.get('BIBLIA_API'), "books")))

if response.status_code != 200:
    raise Exception('API not return books.')

result = response.json()

if "data" in result:
    data = result["data"]
else:
    raise Exception('Data not found.')


"""
return data example:
{'_id': '629cde37468c56a808c68354', 'book': 'Gênesis', 'abbrev': 'gn', 'chapters': {'1': {'verses': 31}, '2': {'verses': 25}, '3': {'verses': 24}, '4': {'verses': 26}, '5': {'verses': 32}, '6': {'verses': 22}, '7': {'verses': 24}, '8': {'verses': 22}, '9': {'verses': 29}, '10': {'verses': 32}, '11': {'verses': 32}, '12': {'verses': 20}, '13': {'verses': 18}, '14': {'verses': 24}, '15': {'verses': 21}, '16': {'verses': 16}, '17': {'verses': 27}, '18': {'verses': 33}, '19': {'verses': 38}, '20': {'verses': 18}, '21': {'verses': 34}, '22': {'verses': 24}, '23': {'verses': 20}, '24': {'verses': 67}, '25': {'verses': 34}, '26': {'verses': 35}, '27': {'verses': 46}, '28': {'verses': 22}, '29': {'verses': 35}, '30': {'verses': 43}, '31': {'verses': 55}, '32': {'verses': 32}, '33': {'verses': 20}, '34': {'verses': 31}, '35': {'verses': 29}, '36': {'verses': 43}, '37': {'verses': 36}, '38': {'verses': 30}, '39': {'verses': 23}, '40': {'verses': 23}, '41': {'verses': 57}, '42': {'verses': 38}, '43': {'verses': 34}, '44': {'verses': 34}, '45': {'verses': 28}, '46': {'verses': 34}, '47': {'verses': 31}, '48': {'verses': 22}, '49': {'verses': 33}, '50': {'verses': 26}}, 'uid': '628c663cd6914a07ae2b0d2018db59a3'}
"""

_n = 0
for i, book in enumerate(data):
    book = book[0]
    chapters = book["chapters"]
    abbrev = book["abbrev"]
    _id = i + 1
    file = "2_BR_%s" % _id
    with ZipFile(Path("audios/source/%s.zip" % file), 'r') as _zip:
        print('Extracting all the files now...')
        _zip.extractall(Path("audios/tmp"))
        print('Done!')

    try:
        onlyfiles = [f for f in listdir(Path("audios/tmp/%s" % _id)) if
                         isfile(join(Path("audios/tmp/%s" % _id).absolute(), f)) and f.split(".")[-1] == "mp3"]
    except Exception:
        continue

    for f in onlyfiles:
        src = "%s/%s" % (_id, f)
        dst = "%s_%s" % (abbrev, f)

        if os.path.isfile(Path(dst)):
            continue

        try:
            shutil.copy(Path("audios/tmp/%s" % src), Path("audios/processed/%s" % dst))
        except FileNotFoundError:
            continue

print("ok!", _n)