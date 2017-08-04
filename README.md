# AESTHETIC

aesthetic is a utility for LED visualizations which
can be displayed on individually controlled LED pixels
such as LED strips.

Like this:

![An example animation](docs/example.gif)

Goals:
 - Decouple the three aspects:
   - device driver
   - animation
   - signal sources
 - It's a goal to make this drivable from the command line
   and to make it easy to hook it up to other input sources
   that can be visualized such as status monitoring, weather
   monitor, etc.

Non-goals:
 - Supporting all possible input sources is a non-goal. It should
   rather have a generic interface so it's easy to hook up.

WARNING: This is very experimental code. There is duplicated code here
and there, but it's wrong to be ashamed for one's throwaway code. :)
Just don't copy it around too much.
