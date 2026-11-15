Make a single self-contained HTML file: a short animated cartoon called "one big berry", about 77 seconds long and looping, where every frame is drawn live with JavaScript on a 2D canvas in a hand-drawn crayon and coloured-pencil doodle style. No libraries, no images, fonts or audio files: everything, including the music, is made in code.

THE LOOK
- Warm off-white paper with grain, faint fibres and a soft vignette. A layer of "paper tooth" (tiny paper-coloured specks) over the whole frame, so the crayon looks like it skipped over the grain.
- Characters are chunky round doodles filled with scribbly crayon hatching: clip to the shape (a slightly wobbled, slightly larger outline, so colour goes a little over the lines), paint paper underneath so shapes are opaque, then lay down many short jittered strokes at one angle in three pressures, a few darker strokes in a second colour, and a lighter cross-hatch.
- Outlines in dark-blue ink that wobble and "boil": displace every line by smooth noise that is re-rolled 8 times a second. Draw each line twice, a firm one and a faint sketchy one.
- Pink blush on cheeks, big shiny cartoon eyes (white, a big dark pupil, two white highlights).
- The ground is one wobbly red crayon line with tufts of grass and the odd doodle flower. Handwritten signs on red posts, written in a tiny single-stroke handwriting font of your own (each letter a few wobbly ink strokes).
- Expressive animation: squash and stretch on every jump and landing, speed lines, dust puffs, impact bursts with a handwritten sound word in them ("plop", "bonk", "thunk"), sweat drops, hearts, sparkles, a light bulb.
- Keep stroke widths and hatch spacing steady on screen however much a shot zooms. Fit any aspect ratio around a square stage (wider screens just see more meadow), crisp on retina with DPR capped at 2.

THE STORY (no dialogue; cut between wide shots and close-ups)
1. A sunny crayon meadow. A small round hedgehog strolls along humming (little music notes), past a sign "home →". A pink wisp of scent drifts in. Sniff, sniff.
2. Close-up: eyes pop wide, a big "!".
3. Wide: one enormous strawberry, twice the hedgehog's height. It dashes over, skids, hops for joy, hugs it. Hearts.
4. It tries to lift it: squats, strains, face going red, shaking, sweat flying, the berry rises a hair... and the hedgehog collapses flat as a pancake. "plop". Dizzy stars, then it pops back into shape.
5. Close-up: hmm... ding! A light bulb.
6. It rolls the berry along, pushing happily, past the "home →" sign.
7. The ground slopes downhill and the berry gets away. Panic, a chase, arms up. The berry hits a rock ("bonk") and flies up out of sight. The hedgehog stops, looks around, droops.
8. Close-up: a tear, a little rain cloud. Then a falling whistle; it looks up; a shadow grows around it.
9. Wide: the berry lands right on its back and sticks on its spines. "thunk". Blink, blink, a look over the shoulder, "?"... then "!" and happy hops. A hedgehog can carry a strawberry after all.
10. It trots home with the berry on its back to a tree-stump house with a round door. The door opens and three tiny hoglets hop out, one, two, three. Hearts all round.
11. Picnic: the family eats it in five bites ("nom"), the berry shrinking each time with red crumbs flying, until only the leafy cap is left. Everyone round and full and blushing.
12. Night: a blue crayon sky, a moon, twinkling star doodles, fireflies, a lit window. The family asleep in a heap with the strawberry cap as a blanket, z's floating up.
13. A title card, written on stroke by stroke: "one big berry", a little doodle of the hedgehog asleep against a berry, "the end". Fade to bare paper and loop.

Build a tiny toolkit first (wobbly line, crayon fill, ink, blush, eyes, keyframes with easing, squash & stretch) and a shot list with keyframes on one timeline. Add ?t=<seconds> to start at any moment.

SOUND (Web Audio, generated in code)
A gentle, playful tune at 100 bpm that follows the story's moods, 32 bars to the loop: Karplus-Strong ukulele strums, a marimba melody written as scale degrees over each bar's chord, soft triangle bass, shaker, woodblock and a soft kick. Tense and sparse for the lifting, a light bulb ding, bouncy for the rolling, minor and urgent for the chase, a sad music box, a march home, warm for the picnic, a music-box lullaby at night, a chime on the title card. Plus sound effects on the comic beats: sniffs, whoosh, skid, boings, a straining whine, plop, birdie tweets, slide whistles, bonk, a sad trombone, a falling whistle, thunk, a door creak, pops, noms, crickets. Schedule everything ahead against the audio clock and drive the animation from that clock so they never drift.

Browsers block audio until a gesture: show a small "click for sound" hint; on click start the sound in sync with wherever the film is. After that, click or space pauses, left and right arrows skip 5 seconds (restart the music at the new spot), M mutes. With ?thumb=1: no hint, no sound.
