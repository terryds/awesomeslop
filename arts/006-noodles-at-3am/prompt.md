Make a single self-contained HTML file: a painting called "noodles at 3 a.m.", drawn entirely with JavaScript on a 2D canvas. No libraries, no images, no WebGL. It should look like oil pastel on dark paper: every part of the picture is made of visible brush marks, and you can watch it being painted.

THE PICTURE
A narrow city street at night in the rain, seen from the middle of the road, in strict one-point perspective. Landscape format. The vanishing point is dead centre, a little below the middle. Everything is dark blue-violet except the light.

- Two walls of tall buildings, one each side, receding to the vanishing point. The near ones run off the top of the picture; the far ones get shorter, so the sky shows as a narrowing gap in the middle. Scattered lit windows, bunched closer together with distance.
- In the gap: a near-black sky going violet, then a hot magenta haze at the end of the street, with thin far towers half lost in it and two faint searchlights.
- Neon signs hanging out over the street from both walls, facing us, about ten each side: mostly tall narrow banners, a few wide ones, in magenta, cyan, yellow, orange, violet and green. Bigger near, tiny far. Each has made-up lettering built from a few bars (no real words, no real brands) and throws a soft glow into the wet air.
- The street is wide: the walls meet the bottom edge off-screen, so wet road fills the lower third of the picture. Every sign appears again in it as a long vertical smear of its colour, starting just below the point where the sign would touch the ground and fading toward us. The haze at the end of the street is mirrored as a glow down the middle of the road.
- Left, near us: a noodle stand. Striped awning, a box of warm orange light, a dark counter, two customers on stools with their backs to us, three red lanterns, steam rising. It is the only warm light in the picture.
- Right of centre, further off: one person walking away under a clear umbrella, a black silhouette with a cyan edge on one side and a magenta edge on the other, and a broken reflection under their feet.
- Cables sagging across the street at several depths. Two small fliers high up, trailing their lights.
- Rain over everything: thin slanted marks, and small rings where drops land on the road.
- Darken the corners so the eye goes to the haze.

HOW TO PAINT IT
Work like a painter, in this order:

1. Off-screen, draw a plain flat version of the scene with ordinary shapes and gradients, including the glows (added light) and the reflections. Nobody sees this. It is only a colour reference.
2. Cover the canvas with brush marks in three passes: big, then medium, then small. Each mark takes its colour from the reference under its centre, with a little random variation. In the last pass, only paint where the picture changes. Then give the signs, the stand and the people one extra pass of very fine marks so they stay crisp.
3. A mark is not one line. It is a handful of thin, slightly curved lines side by side, like bristles, each a bit different in length, brightness and opacity.
4. The direction of the marks follows what is being painted. Sky: one slanted hatch, loosened by noise. Walls: mostly vertical, like rain streaks, with some marks running down the street. Signs and the stand: square. Wet road: long vertical marks first, so reflections smear downward, then short horizontal ones on top, so the surface ripples. People: up and down.
5. Now and then let a mark pick up the colour of something nearby.
6. Last, paint the small things directly on top: a crisp dab for each lit window, the sign lettering and the white-hot edges of the tubes, bright dashes of each sign's colour in the road, cables, fliers, steam, the walker's rim light and umbrella ribs, then the rain and the rings.
7. Finish with a faint paper grain over everything.

Paint over about ten seconds, a batch of marks per frame, in random order within each pass so the picture resolves from blur to detail. Then stop: the finished painting is still.

Clicking paints a new version with a different random seed (new buildings, new signs), alternating between a magenta-and-cyan palette and an amber-and-teal one. Show a small "click to paint it again" hint when a painting is done.

Paint at a fixed 1920 by 1200 and scale the canvas to cover the window.
