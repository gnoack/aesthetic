"""Support for Blinkstick."""
from __future__ import absolute_import

import time
from blinkstick import blinkstick


def is_available():
  return bool(blinkstick.find_all())


def render(animation, channel=1):
  """Render animation on a multi-LED Blinkstick Pro.

  Args:
    animation: A generator of [(r, g, b), ...] lists
    channel: Blinkstick pro channel: r=0, g=1, b=2.
  """
  bs, = blinkstick.find_all()
  #bs.set_mode(2)
  for colors in animation:
    data = [int(value) for r, g, b in colors
            for value in (g, r, b)]
    bs.set_led_data(channel=channel, data=data)
    time.sleep(0.02)
