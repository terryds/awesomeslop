Make a single self-contained HTML file: an animated pixel-art postcard called "first snow", drawn entirely with JavaScript on a 2D canvas. No libraries, no images. Portrait, 240 × 426 pixels, scaled up with hard edges.

THE PICTURE
A narrow residential back street in a snowy town, seen from standing height in the middle of the road, so everything runs to one vanishing point a little below the middle. Bright winter afternoon, blue sky.

- Sky: deep blue at the top to pale at the horizon, banded with ordered dithering, a few soft clouds. Pale mountains and a far row of little snowy houses on the horizon.
- Left: a stone-block wall with a thick cap of snow and a snowbank at its foot. Behind it, houses with heavy snow slabs on the eaves, lit windows, a chimney with smoke, and snow-laden pines. A black cat sits on the wall.
- Right: a row of houses facing the street, the nearest one big and close: siding, framed windows with snow on the sills, icicles, an AC unit, a small shop with a red-and-white awning.
- Utility poles down both sides, getting smaller, with sagging wires that cross the sky.
- The road: packed snow, tyre ruts running to the vanishing point.

Build it in real perspective: one projection function from (x, height, depth) to the screen, and every wall, window, block, pole and wire goes through it. That is what makes it hold together.

THE PEOPLE
Both drawn in code from shapes, flat colour plus one shade and one highlight each, then given a dark outline automatically (any empty pixel touching the figure becomes outline).

- A girl, about 5½ heads tall, in a cream knit beanie with a pom-pom, long dark hair, a red plaid scarf, a navy toggle coat, mittens, a pleated grey skirt, black tights, slouchy white leg warmers and loafers. She walks from the far end of the street toward us, facing us, and fades out as she reaches the camera; then the loop starts again.
- A boy leaning back against the near pole on the left, one foot up against it, in a black puffer with a fur-lined hood and red headphones, looking down at a glowing phone and nodding to music. When she walks past, he looks up.
- Scale both by the same perspective, at about 1.6 m and 1.75 m, so they agree when they stand at the same depth.

THE WALK
It must not slide. The foot on the ground stays fixed to the road while the body passes over it; the back heel peels up; the other leg lifts in an arc and lands in front. Tie her speed to her stride. Body rises mid-step, dips on landing, weight shifts onto the standing leg, arms swing against the legs. Each landing leaves a footprint that slowly fades.

LIFE
Snow falling in three depths, big soft flakes up close. Breath puffs from both of them. Chimney smoke. Her scarf and hair move in the wind. She blinks; the cat blinks and flicks its tail.
