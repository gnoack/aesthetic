import time

def _to_tkcolor(color):
  return "#%02x%02x%02x" % tuple(map(int, color))

def render(animation, scale=16, gap=1):
  # Import lazy, so we don't crash for other use cases if tk is not installed.
  import tkinter as tk

  led_count = 53
  delay_ms = int(1000 * 0.05)

  root = tk.Tk()
  canvas = tk.Canvas(root, width=led_count*gap*scale, height=scale)
  canvas.pack()

  rects = [canvas.create_rectangle(i*gap*scale, 0,
                                   (i+1)*gap*scale, scale,
                                   fill="black")
           for i in range(led_count)]

  def animate():
    colors = next(animation)
    for color, rect in zip(colors, rects):
      canvas.itemconfig(rect, fill=_to_tkcolor(color))
    canvas.update()
    root.after(delay_ms, animate)

  root.after(0, animate)
  root.mainloop()
