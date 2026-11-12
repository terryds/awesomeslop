Make a single self-contained HTML file: a full-window canvas artwork called "drift". No libraries, no text on screen, no controls.

Thousands of tiny particles move across a black background, each one following an invisible field of directions. Build the field from three layered sine and cosine waves of the particle's position, and let it shift very slowly over time so the currents never repeat.

Each particle draws a one-pixel line from where it was to where it is now. Most lines are faint white, about 20% opacity. Roughly one particle in twenty is bright lime (#b8ff2c) instead.

Never clear the canvas. Each frame, paint a nearly transparent black rectangle over everything so old trails fade out over a few seconds. The result should look like wind made visible, or hair, or iron filings.

A particle lives for a random 1 to 4 seconds, then respawns at a random position. It also respawns when it leaves the canvas.

Scale the particle count with the canvas area, capped so it stays smooth on a laptop. Handle window resize and high-density screens.
