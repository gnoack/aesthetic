from PIL import Image
from PIL import ImageDraw


def render(animation, out, scale=8):
  images = [render_frame(colors, scale=scale) for colors in animation]
  save_gif(out, *images)

def render_frame(colors, scale=8):
  led_count = 53
  size = (led_count * scale, scale)

  im = Image.new("RGB", size, "black")
  d = ImageDraw.Draw(im)
  for idx, color in enumerate(colors):
    color = tuple(map(int, color))
    x0 = scale * idx
    y0 = 0
    x1 = scale * (idx + 1)
    y1 = scale
    d.rectangle((x0, y0, x1, y1), fill=color)
  return im

def save_gif(out, image, *more_images):
  image.save(out, save_all=True,
             append_images=list(more_images),
             loop=1000,
             duration=50)
