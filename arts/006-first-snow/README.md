# first snow

A pixel-art postcard that never quite ends: a girl walking home down a snowy back street, a boy waiting by a pole, a cat on the wall.

## what you're looking at

Nothing here is a sprite sheet or an image. Every pixel is drawn by code, every frame.

- **The street is real perspective.** One function turns a point in the world (left-right, height, distance) into a pixel. Walls, stone blocks, windows, icicles, poles and wires all go through it, so they all agree on where the vanishing point is.
- **The people are shapes plus an outline.** Each one is drawn on its own small canvas from flat polygons and ellipses, with a shade and a highlight. Then every empty pixel that touches the figure turns dark. That one pass is most of what makes it read as pixel art.
- **The walk is planted.** Her feet stay put on the road while her body moves over them, and her speed is tied to her stride, so she doesn't skate. The footprints land where her feet actually touched.
- **Scale comes from distance.** She is drawn once and sized by her distance from the camera, at the same rate as the boy, so they're the right height when they're side by side.

## things worth stealing from the prompt

- **One projection for everything.** "Every wall, window, pole and wire goes through it." Hand-placed perspective drifts; one function can't.
- **Auto-outline.** Drawing outlines by hand is where code-made pixel art usually looks wrong. Let the computer add them afterwards.
- **"It must not slide."** Then say how: the standing foot is fixed to the ground, speed is tied to stride. A walk cycle on its own isn't enough.
- **Give the heights in metres.** "About 1.6 m and 1.75 m, same perspective." Without it, two characters drawn separately never match.

## how it was made

This one took several rounds of feedback rather than a single prompt: the camera moved closer, the girl went from crossing the street to walking toward us, her proportions and height were fixed twice, and the walk was rebuilt so her feet stop sliding. The prompt above is the version that would get there in one go.

## credit

The mood, a quiet snowy street in pixel art, comes from [nazeondo's #pixelartpark postcards](https://www.instagram.com/nazeondo/). This is my own scene and my own code, not a copy of theirs.
