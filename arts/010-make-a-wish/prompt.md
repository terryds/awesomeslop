Make a single self-contained HTML file: a birthday card called "make a wish". A cake draws itself, stroke by stroke, on a 2400 x 1350 canvas (16:9) scaled to fit the window; then the viewer lights the candles and blows them out. Plain JavaScript, Canvas 2D and WebAudio only. No libraries, no images, no fonts, no audio files.

THE MOOD
Cosy and quiet. One cake, one dark room, candlelight. No confetti, no fireworks.

THE LOOK
It must look drawn by hand in dry media on dark plum paper, not digital.
- One tileable height field is the tooth of the paper. Draw each batch of strokes on a spare canvas, knock the valleys of the tooth out of it with a mask, then lay it on the page. The mask never moves.
- Four tools: soft pastel (broad, misses about a fifth of the tooth), oil pastel (narrow, nearly solid), coloured pencil (2 to 3 px), chalk.
- A stroke is a ribbon with a wandering spine, a ragged edge and more weight in the middle than at the ends.
- A small box of sticks per area; between two neighbours pick one or the other at random, never blend.
- Every surface is hatched in its own direction: the wall on a diagonal, the table level, the side of the cake upright.

THE ROOM
- Wall: dark plum, warming to rose-brown in a wide halo behind the cake.
- Top left, a four-pane window: deep blue night, stars, a crescent moon, snow on the sill outside, a black cat asleep on the sill inside with its tail hanging down.
- Across the top, a sagging string of small bunting flags in muted rose, mustard, teal, cream and lilac, with a little warm bulb between each pair.
- Top right, three balloons in the same colours, their strings going down behind the table.
- A round wooden table across the bottom.
- In the middle of it, on a cream plate: a round cake with cream sides, pink piped rosettes round the foot, dark chocolate poured over the top and running down in drips of different lengths, strawberries on dollops of cream round the edge.
- Left of the cake a teal present with cream dots and a pink ribbon and bow. Right of it a cream cup of tea with a pink stripe, on a saucer.
- Candles: one thin striped candle per year for ages 1 to 10 (five if no age is given), in two staggered rows. Above 10, number candles spelling the age instead.

WHAT HAPPENS
1. The room draws itself in about six seconds, in the order a person would: wall, window, bunting, balloons, table, present, cup, cake, candles. The room is dim and bluish. A small line of text says "click to light the candles".
2. Click: the flames catch one after another from left to right, the room warms up, a music box plays Happy Birthday once, and the greeting is written on the wall above the cake in chalk, left to right: "happy birthday," and under it the name, bigger, shrunk to fit if it is long. With no name: "happy birthday" / "to you".
3. After a few seconds: "make a wish, then click to blow them out". Click: the flames lean, go out in a quick wave, a puff of breath is heard, thin smoke curls up from each wick, and the room goes dim again. Then: "click to light them again".

WHAT MOVES
Everything that moves is redrawn 12 times a second, in the same tools and through the same paper tooth, so it boils slightly like hand-drawn animation: the flames (an orange body, a yellow heart, a white core, a blue dot at the wick, each leaning on its own), the smoke, snow falling outside the window, steam off the tea, the bulbs twinkling. Light is done when the layers are put together: a blue multiply over the whole drawing when the candles are out, a soft warm glow around the flames and the bulbs when they are lit.

FOR ANYONE
?name= sets who it is for (up to 24 characters) and ?age= the candles. In the bottom left corner, a small "make one for someone" opens a panel with a name field, an age field, "show it" and "share it". Next to it, "share this card" for the card on screen, and a sound on/off (also the M key). Sharing copies the link and says "link copied, now paste and share it to celebrate!". If the browser refuses the clipboard, show the link in a box, already selected, with "press Ctrl+C to copy the link". Build the link from location.href, because inside a sandboxed frame location.origin is "null". Draw the name with canvas text into a hidden mask and fill the mask with chalk strokes, so any name in any script works and nothing typed is ever put into the page as HTML.

Clicking while it is still drawing finishes the drawing at once. Loaded with ?thumb=1: no text or controls, draw as fast as possible, fill the frame, and light the candles without being asked (no sound).
