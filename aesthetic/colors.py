from aesthetic.util import normalize

red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
yellow = (128, 255, 0)
white = (255, 255, 255)

icyblue = (0x43, 0xff, 0xe8)
lightblue = (0x88, 0x88, 0xde)
sunyellow = (0xff, 0xe2, 0x43)
orange = (0xff, 0x7a, 0x00)

def mix_color(a, b, f):
  ar, ag, ab = a
  br, bg, bb = b
  return (f*br + (1-f)*ar, f*bg + (1-f)*ag, f*bb + (1-f)*ab)

def get_color(temperatur):
  eiskalt = white
  kuehl = icyblue
  normal = sunyellow
  warm = orange
  heiss = red

  punkte = [
    (0, eiskalt),
    (10, kuehl),
    (15, normal),
    (22, warm),
    (30, heiss),
  ]
  if temperatur < 0:
    return eiskalt
  elif temperatur > 30:
    return heiss
  else:
    prev_temp, prev_color = punkte[0]
    for next_temp, next_color in punkte:
      if prev_temp <= temperatur < next_temp:
        f = normalize(temperatur, prev_temp, next_temp)
        return mix_color(prev_color, next_color, f)
      prev_temp, prev_color = next_temp, next_color
