import random
import itertools
import math
import time

from aesthetic import colors
from aesthetic.output import blinkstick


def mix_color(a, b, f=0.5):
  ar, ag, ab = a
  br, bg, bb = b
  fneg = 1-f
  return (ar*fneg + br*f, ag*fneg + bg*f, ab*fneg + bb*f)

def numbers(init=0, step=1):
  while True:
    yield init
    init += step

def sine_gen(bottom, top, init=0, speed=0.1):
  step = speed * math.pi * 2
  for x in numbers(init, speed):
    normalized = (math.sin(x) + 1) / 2
    yield bottom + normalized * (top-bottom)

def blend_up(steps=20):
  for x in range(steps, 0, -1):
    yield (math.cos(x * (math.pi / steps)) + 1) / 2

def blend_down(steps=20):
  return (1-f for f in blend_up(steps=steps))

def repeat(value, steps=20):
  return (value for _ in range(steps))

def forever(value=1):
  while True:
    yield value

def ones(steps=20):
  return (1 for _ in range(int(steps)))

def cycle_colors(colors, blend_steps=40, sustain_steps=30):
  blend_steps = int(blend_steps)
  sustain_steps = int(sustain_steps)

  color_cycle = itertools.cycle(colors)
  old_color = next(color_cycle)
  for new_color in color_cycle:
    for f in blend_up(steps=blend_steps):
      yield mix_color(old_color, new_color, f=f)
    for _ in range(sustain_steps):
      yield new_color
    old_color = new_color

def draw_glow(colscreen, position, width, color, f=0.5):
  for x in range(max(0, int(position-width)),
                  min(len(colscreen), int(position+width))):
    pixel_f = (math.cos((position - x) * (math.pi / width)) + 1) / 2
    colscreen[x] = mix_color(colscreen[x], color, f * pixel_f)

def draw_clear(colscreen):
  for idx in range(len(colscreen)):
    colscreen[idx] = (0, 0, 0)

def generate_glow(colorscreen, position_gen, color_gen):
  for pos, col in zip(position_gen, color_gen):
    width = 15
    draw_glow(colorscreen, pos, width, col, f=1)
    yield

def cycle_visibility_phases(invisible_steps=30, visible_steps=60,
                            transition_steps=10):
  invisible_steps = int(invisible_steps)
  visible_steps = int(visible_steps)
  transition_steps = int(transition_steps)

  while True:
    for _ in range(invisible_steps):
      yield 0
    for f in blend_up(steps=transition_steps):
      yield f
    for _ in range(visible_steps):
      yield 1
    for f in blend_up(steps=transition_steps):
      yield 1-f

def draw_pixel(colorscreen, pos, color, f=0.5):
  pos = int(pos)
  if 0 <= pos < len(colorscreen):
    colorscreen[pos] = mix_color(colorscreen[pos], color, f)

def draw_blended_pixel(colorscreen, pos, color, f=0.5):
  x_min = int(pos)
  x_max = x_min + 1
  f_max = pos - x_min
  f_min = x_max - pos
  draw_pixel(colorscreen, x_min, color, f=f*f_min)
  draw_pixel(colorscreen, x_max, color, f=f*f_max)

def generate_floatie(colorscreen, position_gen, appearance_gen,
                     color=(255, 255, 255)):
  for pos, f in zip(position_gen, appearance_gen):
    draw_blended_pixel(colorscreen, pos, color, f=f)
    yield

def multiple_floaties(colorscreen, hectic=0):
  leds = len(colorscreen)
  floaties = [
    generate_floatie(
      colorscreen,
      (x % leds for x in numbers(
        step=random.choice((1, -1)) * (random.uniform(0.2, 0.8) + hectic) * 0.3)),
      cycle_visibility_phases(
        transition_steps=random.randint(60, 150) - 60*hectic,
        visible_steps=random.randint(10, 30),
        invisible_steps=random.randint(100, 1000)),
      color=colors.white)
    for _ in range(int(5 + 10*hectic))
  ]
  while True:
    for f in floaties:
      next(f)
    yield

def dampen_color(color, f=0.5):
  r, g, b = color
  return f*r, f*g, f*b

def generate_dampen(colorscreen, brightness):
  """Dampen the screen in each step according to brightness setting."""
  for f in brightness:
    for idx, x in enumerate(colorscreen):
      colorscreen[idx] = dampen_color(x, f=f)
    yield

def generate_multiple(colorscreen, animations):
  while True:
    draw_clear(colorscreen)
    for animation in animations:
      next(animation)
    yield colorscreen

def animate(leds=53, glow1_colors=None,
            glow2_colors=None, hectic=0):
  glow1_colors = glow1_colors or (colors.icyblue, (255, 255, 255), colors.lightblue)
  glow2_colors = glow2_colors or (colors.sunyellow, colors.orange, colors.red)

  colorscreen = [(0,0,0)] * leds
  animations = (
    generate_glow(colorscreen,
                  sine_gen(0, leds, speed=-0.002),
                  cycle_colors(glow1_colors, blend_steps=300, sustain_steps=30)),
    # generate_glow(colorscreen,
    #               sine_gen(0, leds, speed=0.004),
    #               cycle_colors(glow1_colors, blend_steps=30, sustain_steps=9)),
    generate_glow(colorscreen,
                  sine_gen(0, leds, speed=0.006),
                  cycle_colors(glow2_colors, blend_steps=400, sustain_steps=10)),
    multiple_floaties(colorscreen, hectic=hectic),
    generate_dampen(
      colorscreen,
      itertools.chain(blend_up(100), ones(1600), blend_down(100),)
    ),
  )
  return generate_multiple(colorscreen, animations)


if __name__ == "__main__":
  blinkstick.render(animate(hectic=0))
