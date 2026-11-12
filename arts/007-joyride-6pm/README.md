# joyride, 6 p.m.

A city, a car, and the last hour of sun. Nothing to win.

**Click the scene, then:** W A S D to drive, Space for the handbrake, **C** to change camera, **T** for night, R to reset, M for sound.

Try the night. Then find the boulevard with the palms and take the handbrake into a corner.

## what you're looking at

A 7 by 7 grid of city blocks, built from nothing but code when the page loads: about 120 buildings, 60 cars, 100 people, 400 street lamps and 100 traffic signals. No models or image files.

- **The road is one painting.** Every lane line, zebra crossing, manhole and skid mark is drawn once onto a single big texture laid over the ground. That is far cheaper than geometry and reads as more detail.
- **Six facades, a whole city.** Each building wears one of six hand-drawn window textures, tiled to its size, plus a strip of shopfronts. A second copy of each texture says which windows are lit, and only shows at night.
- **Everything repeated is one object.** All the cars are one shape drawn sixty times with different colours and proportions. Same for people, trees, lamps and every small box on a rooftop.
- **The traffic thinks a little.** Each car holds its lane, reads the signal ahead, and brakes for whatever is in front of it, including you.
- **Reflections are the real sky.** The sky is captured once for day and once for night, and the glass towers and car paint reflect it.

## what it is not

It is not a copy of any existing game, and it is not AAA. Big-budget open worlds are built from thousands of hand-made models. This one is boxes with good textures, good light and things that move. You cannot get out of the car, go indoors, or cause any harm: people on the sidewalk ignore you.

## things worth stealing from the prompt

- **Say where the detail lives.** "Roads are painted in detail on one large ground texture" and "six kinds of facade, tiled" tell the agent how to afford a city.
- **List what moves, and the rules it follows.** "Keeps to its lane, stops at red, brakes for the car in front" is a complete traffic system in one sentence.
- **Ask for the second look.** The night switch reuses everything and doubles what there is to see.
- **Put the performance plan in the prompt.** Instancing, a resolution cap and a lighter mode for small windows.
