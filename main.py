import json
import os
import traceback
from time import sleep

from providers.bdnews24 import Bdnews24
from providers.bntribune import BnTribune
from providers.dhktribune import DHKTribune
from providers.dstar import DStar
from providers.ittefaq import Ittefaq
from providers.tbs import TBS



while True:
  for provider in (Bdnews24, TBS, DStar, BnTribune, DHKTribune, Ittefaq):
    print(f"Extracting stories from {provider}")
    try:
      new_stories = provider().get_stories()
      for story in new_stories:
        if not story.is_complete():
          continue
        with open('testnews.json', 'r') as j:
          data = json.load(j)
          if story.title in [s['title'] for s in data[story.lang]]:
            continue
        with open('testnews.json', 'w') as j:
          data[story.lang].append({
            'title': story.title,
            'summary': story.summary
          })
          json.dump(data, j, indent=2)
    except Exception as e:
      print("Something went wrong:" + str(traceback.format_exc()))
  os.system("gsutil -m cp testnews.json -r ./static gs://shotto/static")
  print("Gonna take a nap for 30mins. 😴")
  sleep(1600)
