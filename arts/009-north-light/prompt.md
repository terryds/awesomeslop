Make a single self-contained HTML file: a drawing called "north light" that draws itself, stroke by stroke, on a 2400 x 1350 canvas (16:9), scaled to fit the window. Plain JavaScript and Canvas 2D only. No libraries, no images, no fonts, no WebGL.

THE LOOK
This is the heart of the piece; if something has to give, keep this. It must look drawn by a hand with dry tools on dark toned paper, not digital, not like an SVG.
- The paper is deep indigo with a fine tooth. Build one tileable height field for the tooth. Every tool only leaves pigment where it can reach: draw each batch of strokes on a spare canvas, knock out the valleys of the tooth with a mask made from that height field, then lay the batch on the page. The mask never moves, so the same specks of bare paper show through every layer.
- Four tools and a finger. Soft pastel: broad, catches about four fifths of the tooth. Oil pastel: narrower, nearly solid. Coloured pencil: 2 to 3 px lines. Chalk: stars and dust. Finger: soft rubbed-in glows, used sparingly.
- A stroke is a ribbon, not a line: a spine that wanders a little, a ragged edge, heavier in the middle than at the ends, sometimes bowed. No two alike.
- A finite box of sticks. Give each area a short row of colours and, between two neighbours, pick one or the other at random; never blend them. The mixing happens in the eye, through hatching.
- Fill areas with hatching that has a direction: the sky on a diagonal, mountain faces down their slope, water and snow level, roofs along the pitch. Flat shapes are filled with parallel strokes that overshoot the edge a little.
- Colour like a 90s anime cel at night: indigo, ultramarine, teal, mint green, rose, peach, one warm yellow.

THE SCENE
A fjord in the far north, just after the last of the twilight.
- Sky: near-black indigo overhead, through ultramarine, to teal at the horizon. Low on the left, where the sun went, a rose and peach glow with two flat little clouds. Chalk stars, a few with four points, one falling star.
- The aurora: three curtains, each a winding path with rays rising from it toward a single point far above the page, so they fan out. One long curtain starts small near the left horizon, folds back on itself and sweeps up and out through the top right corner, growing as it comes. Rays come in bundles with dark gaps between. Each ray is several short pastel strokes: almost white at the hem, mint, green, teal, then violet and magenta at the crown, fading as it climbs. Rub a little green and violet into the paper first, pull long pencil lines up through the rays after, and finish the brightest hems in oil pastel.
- Mountains: a pale far range across the water and a darker, taller one on the right. Left faces lit, right faces in shadow, snow broken by dark rock, a pencil line along each ridge, mist at the foot. A line of tiny trees and seven lit windows on the far shore.
- Water: level strokes, the sky upside down, the mountains dark in it, and the aurora lying on it in broken green dashes under where it hangs.
- Snow in front: blue-violet drifts, green where the sky reaches them, a lip of ice along the water, two ski tracks coming up from the bottom of the page.
- A small red cabin on the shore, left of centre: snow thick on the roof, icicles, chimney smoke, three lit windows and a lit door, and their light lying yellow on the snow. It is the only warm thing on the page.
- Spruces heavy with snow: four small ones by the cabin, three big ones framing the left and right edges.
- No people.

THE DRAWING
Draw in the order a person would: sky, stars, aurora, mountains, water, snow, cabin, trees, last touches. A few strokes per frame so it takes about 6 seconds; a ?speed=N query multiplies the strokes per frame. Click while it is drawing to finish it at once; click when it is done to start again with a different seed. Loaded with ?thumb=1, draw as fast as possible and fill the frame.
