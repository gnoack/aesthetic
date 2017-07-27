#!/usr/bin/python3
import time
import math
import collections
import csv
import sys
from urllib import request as urlrequest

import colors
import animate
from util import normalize
from output import blinkstick
from output import tkinter

def log(*args):
  print(args)

def fetch_data():
  return urlrequest.urlopen('http://data.geo.admin.ch/ch.meteoschweiz.swissmetnet/VQHA69.csv')

def open_saved_data():
  return open('VQHA69.csv')

Wetter = collections.namedtuple(
  'Wetter',
  (
    'temperatur_celsius',
    'windgeschwindigkeit_kmh',
    'niederschlag_mm_10m',
  )
)

def visualize2(wetter):
  if not wetter:
    log("Keine Wetterdaten")
    return

  log(wetter)
  wind = normalize(wetter.windgeschwindigkeit_kmh, 0, 30)
  regen = normalize(wetter.niederschlag_mm_10m, 0, 10)
  farbe = colors.get_color(wetter.temperatur_celsius)

  farben1 = (colors.icyblue, colors.lightblue)
  farben2 = (colors.sunyellow, colors.orange, colors.red)
  def drag(col):
    return animate.mix_color(col, farbe, 0.6)
  farben1 = list(map(drag, farben1))
  farben2 = list(map(drag, farben2))

  if blinkstick.is_available():
    renderer = blinkstick
  else:
    renderer = tkinter

  renderer.render(animate.animate(glow1_colors=farben1,
                                  glow2_colors=farben2,
                                  hectic=wind))


def interpret_data(reader):
  for unused in range(2):
    reader.readline()  # Discard two lines... :-/

  for line in csv.DictReader(reader, delimiter='|'):
    if line['stn'] == 'SMA':  # Zurich Fluntern
      wetter = Wetter(
        temperatur_celsius=float(line['tre200s0']),
        windgeschwindigkeit_kmh=float(line['fu3010z0']),
        niederschlag_mm_10m=float(line['rre150z0']),
      )
      return wetter
  return None

def main(args):
  if "-quiet" in args:
    global log
    log = lambda *args: None

  if "-web" in args:
    reader = fetch_data()
  elif "-local" in args:
    reader = open_saved_data()
  else:
    sys.exit("need to pass -web or -local")

  visualize2(interpret_data(reader))

if __name__ == "__main__":
  main(sys.argv[1:])
