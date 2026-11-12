Make a single self-contained HTML file: a painting called "the long way home", drawn entirely with JavaScript on a 2D canvas. No libraries, no images, no WebGL. It should look like oil pastel on toned paper: every part of the picture is made of visible brush marks, and you can watch it being painted.

THE PICTURE
A wide wheat field at golden hour, landscape format, horizon a little below the middle. The sun is low on the left, just behind the hills, so everything has a warm lit side and a long violet shadow pointing right.

- Sky: deep blue at the top, turquoise in the middle, peach at the horizon. The sun is a pale disc sitting on the far ridge, with a glow around it. Heaped clouds with cream tops, lavender shade and an orange underside, plus a few thin bars of cloud low over the horizon. A loose flock of birds.
- Three ranks of blue-violet hills, each paler than the one in front, and a row of poplars.
- The field: gold, paler far away, deep ochre at our feet, cut into wedges of slightly different tone that all converge on one vanishing point.
- A dirt road that starts wide at the bottom edge, winds once, and thins to a thread at a farmhouse on the right: white gable catching the sun, red roof, long wall in shade with two lit windows, chimney smoke, a barn, a big tree beside it.
- Telegraph poles down the left side of the road, the nearest one tall enough to cross the horizon, with sagging wires between them and long shadows.
- One small cyclist on the road, heading for the house.
- Foreground: dark wheat stalks leaning in the wind, a few catching the light, and red poppies.

HOW TO PAINT IT
Work like a painter, in this order:

1. Off-screen, draw a plain flat version of the scene with ordinary shapes and gradients. Nobody sees this. It is only a colour reference.
2. Cover the canvas with brush marks in three passes: big marks first, then medium, then small. Each mark takes its colour from the reference under its centre, with a little random variation. In the last pass, only paint where the picture changes (edges) and in the foreground, so flat areas stay broad and calm. Give the farmhouse one extra pass of very fine marks so its windows and roof edges stay crisp.
3. A mark is not one line. It is a handful of thin, slightly curved lines side by side, like bristles, each a bit different in length, brightness and opacity.
4. The direction of the marks follows what is being painted. Sky: one consistent slanted hatch, loosened a little by noise. Hills: along the ridges. Field and road: toward the vanishing point. Near wheat: short upright flicks. Foliage: every direction. Walls and roofs: square, horizontal or vertical.
5. Now and then let a mark pick up the colour of something nearby, the way a loaded brush does.
6. Last, paint the small things directly on top with the same kind of marks: poles, wires, shadows, the cyclist, smoke, window glow, birds, sun flecks, stalks, poppies.
7. Finish with a faint paper grain over everything.

Paint over about nine seconds, a batch of marks per frame, in random order within each pass so the picture resolves from blur to detail. Then stop: the finished painting is still.

Clicking paints a new version with a different random seed (new clouds, new marks), alternating between golden hour and a blue-hour palette. Show a small "click to paint it again" hint when a painting is done.

Paint at a fixed 1920 by 1200 and scale the canvas to cover the window.
