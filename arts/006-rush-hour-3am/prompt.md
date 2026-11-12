Make a single self-contained HTML file: a painting called "rush hour, 3 a.m.", drawn entirely with JavaScript on a 2D canvas. No libraries, no images, no WebGL. It should look like oil pastel on dark paper: every part of the picture is made of visible brush marks, and you can watch it being painted.

THE PICTURE
A crowded city street at night in the rain, in strict one-point perspective, landscape format. We are standing on a footbridge a little above head height, looking straight down the street, so the crowd spreads out below us and shrinks toward a vanishing point dead centre, a little below the middle. Everything is dark blue-violet except the light.

- The street is wide and clearly a street: wet road down the middle, a sidewalk each side with a pale kerb line, and a zebra crossing in the foreground. The walls meet the bottom edge off-screen, so the ground fills the lower third.
- The crowd is the subject. About 130 people on the road and sidewalks, all standing on the same ground so they shrink together with distance: big at the bottom edge, specks at the far end. Most are dark silhouettes. About half carry umbrellas: mostly dark, some clear, a few red, yellow, cyan, white or violet. A few wear a bright coat. Far people are drawn first so near ones overlap them.
- Two walls of tall buildings receding to the vanishing point. The near ones run off the top; the far ones are shorter, so the sky shows as a narrowing gap. Rows of windows storey by storey, a storey being a bit taller than a person, some lit.
- At the foot of every building, lit shopfronts: a band of warm or neon light one storey high with a dark fascia above. This is the light the crowd is seen against.
- Neon signs hanging out over the street from both walls, facing us, about ten each side: mostly tall narrow banners, in magenta, cyan, yellow, orange, violet and green. Made-up lettering built from a few bars (no real words, no real brands). Each throws a soft glow.
- In the gap: near-black sky going violet, a hot magenta haze at the end of the street with thin far towers in it, two faint searchlights.
- Wet ground: every sign and shopfront appears again below it as a vertical smear of its colour, fading toward us. The haze is mirrored as a glow down the middle of the road. Each person has a short dark reflection.
- Cables sagging across the street. Two small fliers high up, trailing their lights. Steam rising from two street grates. Light rain, and rings where drops land.

HOW TO PAINT IT
Work like a painter, in this order:

1. Off-screen, draw a plain flat version of the scene with ordinary shapes and gradients, including glows (added light) and reflections. Nobody sees this. It is only a colour reference.
2. Cover the canvas with brush marks in three passes: big, then medium, then small. Each mark takes its colour from the reference under its centre, with a little random variation. In the last pass, only paint where the picture changes. Then give signs, shopfronts and people one extra pass of very fine marks so they stay crisp.
3. A mark is not one line. It is a handful of thin, slightly curved lines side by side, like bristles.
4. The direction of the marks follows what is being painted. Sky: one slanted hatch, loosened by noise. Walls: mostly vertical, like rain streaks. Signs and shopfronts: square. Wet ground: long vertical marks first, so reflections smear downward, then short horizontal ones on top, so the surface ripples. People: up and down.
5. Last, paint the small things directly on top: sign lettering and the white-hot edges of the tubes, bright dashes of each sign's colour on the ground, cables, fliers, steam. Every person near enough to matter gets a cyan edge on one side and a magenta edge on the other, and a shine along the umbrella. Then the rain.
6. Finish with a faint paper grain.

Paint over about eleven seconds, a batch of marks per frame, in random order within each pass so the picture resolves from blur to detail. Then stop: the finished painting is still.

Clicking paints a new version with a different random seed (new buildings, signs and crowd), alternating between a magenta-and-cyan palette and an amber-and-teal one. Show a small "click to paint it again" hint when a painting is done.

Paint at a fixed 1920 by 1200 and scale the canvas to cover the window.
