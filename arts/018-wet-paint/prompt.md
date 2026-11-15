Make a 60-second animated short film called "wet paint", drawn live in one HTML file with canvas 2D and Web Audio. No libraries, no images, no video: every picture is painted by code when the page loads.

THE IDEA
The little Claude Code mascot (a small coral block with two tall dark eyes, a stubby arm on each side and four short legs) carries a paintbrush as long as he is wide. He walks through five unfinished paintings, each in a different style, and paints in the one thing each is missing. In the last scene the five finished paintings hang on a gallery wall, he paints a small self-portrait and falls asleep next to it.

SIX SCENES, TEN SECONDS EACH (96 bpm, four bars per scene, cuts on bar lines)
1. Harbour, pencil and watercolour. It starts as a pencil sketch on cream paper: a lighthouse on a cliff, two sailing boats, a low sun, a wooden quay. He walks along the quay holding the brush up behind him and the watercolour follows it across the page, with a wobbly wet edge and small blooms running ahead. When he reaches the end the boats start to sail and the gulls fly, and he hops.
2. Plum branch, ink on rice paper. A bare black branch, dry at the edges, a pale red sun, grey hills as a faint wash. He hops up the branch, one hop per beat, and pink blossoms open where he lands. Petals start to fall. Then he jumps off the end, lands hard in the corner and steps aside: where he landed there is a red seal the shape of his body, with his two eyes left blank.
3. Night town, gouache. Flat blue houses with dark windows. He runs along the rooftops, jumping the gaps, and the windows light up behind him. At the last roof he jumps and sweeps the brush across the sky: the stars come on along the stroke and a crescent moon pops in at the end.
4. Sunflowers, thick paint. The sky is thousands of short strokes following a flow field that curls around a yellow sun; the field is green and yellow strokes. He walks through touching the ground with the brush, and a sunflower taller than him shoots up at each touch. The last one grows under his feet and lifts him up above the others.
5. Koi pond, seen from above. Teal water, lily pads, two lotus flowers, pebbles in the corners, one gold koi. He stands on the biggest pad. Two plain white koi swim past, one after the other, and he flicks drops of paint at them: three orange patches on the first, one red and two black on the second. Each drop makes rings on the water.
6. The gallery. A warm wall with the five finished paintings in frames (render each scene's last frame, without him, into its frame), a window, a wooden floor, an easel with a blank canvas. He walks in looking up at the pictures, paints a small picture of himself on the easel in three strokes plus eyes and legs, steps back, puts the brush down, sits and falls asleep. The title "wet paint" fades in on the wall. Then it loops.

HOW IT MOVES
- A camera: each scene starts close on him and follows him, then pulls back to show the whole painting.
- Scenes change with a wipe of seven wide brush strokes, alternating left and right, with ragged bristle ends.
- He has a walk cycle, a little bob, squash when he lands, blinks, wide eyes when surprised and curved happy eyes when a painting is done.
- Everything is a function of the film time, so any second can be drawn on its own.

THE LOOK
Soft and painterly: paper grain over everything, washes with darker dried edges, brush strokes made of parallel bristles where some run dry, foliage and sky built from short rounded dabs. The static part of each painting is drawn once into its own layer; only the moving things are drawn each frame.

SOUND
All made in Web Audio: a soft plucked tune on a pentatonic scale with a different four-chord loop for each scene, a bass note and a quiet pad on each bar, plus small sounds for the action (brush swishes, a pop for each blossom, a thud for the seal, a chime for each window, a plop for each drop of paint).

THE PAGE
The film fits the window (16:9, letterboxed in paper colour) and loops. It starts silent: click for sound, then click or space to pause, ← → skip 5 seconds, M mutes. `?thumb=1` hides the hint, `?t=25` starts at 25 seconds.
