# drift

A flow field. A few thousand particles, each asking the same question every frame: *which way is the wind blowing here?*

## what you're looking at

There is no drawing of curves anywhere in the code. Every particle only ever draws a tiny straight line, one or two pixels long. The curves appear because neighbouring particles get nearly the same direction, so their trails bundle into strands.

The canvas is never cleared. A nearly transparent black wash goes over it each frame, which is what turns moving dots into fading trails.

## things worth stealing from the prompt

- **"Never clear the canvas"** is the single most important sentence. Remove it and you get a screen of dots.
- **"One particle in twenty is bright lime"** gives the eye something to follow. All-white reads as texture; a rare accent reads as motion.
- **"Wind made visible, or hair, or iron filings"** tells the agent what to tune towards when it has to pick numbers.

## try changing

- the fade strength (slower fade = denser, more painterly)
- the number of wave layers in the field (more layers = more turbulence)
- the lifetime (short lives give stubble, long lives give rivers)
