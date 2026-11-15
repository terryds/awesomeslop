# one big berry

A 77-second crayon cartoon that loops: a small hedgehog finds one enormous strawberry, can't lift it, loses it down a hill, and then gets it home in the one way only a hedgehog could.

**Click for sound.** Then click or space to pause, ← → to skip 5 seconds, M to mute. Add `?t=40` to the address to start at 40 seconds.

## what you're looking at

Nothing here is an image, a sprite or a sound file. Every frame is drawn again from scratch, and the music is played note by note as it goes.

- **Crayon is clipping plus scribbles.** Each shape is a list of points. To fill it, the code clips to a slightly wobbled, slightly bigger copy of the outline (so the colour goes a little over the lines), paints paper underneath so the shape is opaque, then scribbles hundreds of short strokes at one angle in three pressures, adds a few darker ones in a second colour and a faint cross-hatch. A layer of paper-coloured specks over the whole frame makes it look like the crayon skipped over the grain.
- **The lines boil.** Every outline is pushed around by smooth noise that is re-rolled 8 times a second, and drawn twice: a firm pen line and a faint sketchy one. The hatching is re-scribbled at the same rate. That's the "drawn on every frame" shimmer.
- **The writing is a font made of strokes.** Signs, sound words ("plop", "bonk", "thunk", "nom") and the title card use a tiny handwriting font where each letter is a few lines, drawn through the same wobbly ink as everything else, so the words boil too. The title writes itself on letter by letter.
- **One timeline, thirteen shots.** Each shot has its own little stage and camera, and every move is a keyframe with an ease. Jumps stretch in the air and squash on landing with a damped wobble, and the walking is tied to distance travelled so feet don't skate.
- **The music follows the story.** 32 bars at 100 bpm fill the loop exactly. Each bar has a chord and a mood: ukulele strums (a Karplus-Strong plucked string computed into a buffer), a marimba tune written as scale steps over the chord, a triangle bass, shaker and woodblock; sparse and tense when lifting, urgent in the chase, a music box when sad and at night. Sound effects (boings, a slide whistle, a sad trombone, a falling whistle, noms) sit on a cue sheet in story time. The picture runs off the audio clock, so they stay together, even after a pause or a skip.

## things worth stealing from the prompt

- **Write the story as numbered shots.** "Close-up: eyes pop wide, a big !" gets you camera cuts and timing for free, and makes the cartoon readable without a word of dialogue.
- **Name the comic beats and their sound words.** Squash, strain, collapse, "plop". A setback that turns into the solution (the berry landing on the spines) is what makes a story out of a sequence of gags.
- **"Paint paper underneath."** Crayon hatching is see-through; without an opaque base the hedgehog's face turns the colour of its spines.
- **"Keep stroke widths steady on screen however much a shot zooms."** Otherwise close-ups look like they were drawn with a broom.
- **Drive the picture from the audio clock.** Two clocks always drift; one doesn't.

## limits

- The sound needs a click (browsers insist). Skipping restarts the music from the new spot, so a note that was already ringing gets cut.
- The handwriting font only has the letters the film needs.
- Screens much wider or taller than square see more meadow, not more story; things entering a shot can be visible a moment early at the very edges.

## credit

The drawing style (crayon hatching, boiling blue ink, red ground line, blush, big shiny eyes) is inspired by Kevin Ngo's crayon short. The story, the hedgehog family and all the code are new.
