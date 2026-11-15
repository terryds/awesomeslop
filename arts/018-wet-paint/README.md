# wet paint

The little Claude mascot has a brush and five unfinished paintings. In each one something is missing, and he paints it in: colour on a pencil harbour, blossoms on a bare branch, lights and stars over a dark town, sunflowers in an empty field, spots on two plain koi. Then the five paintings hang on a wall, he paints himself, and falls asleep. Sixty seconds, then it loops.

**Click for sound.** Then click or space to pause, ← → to skip 5 seconds, M to mute. Add `?t=30` to the address to start at 30 seconds.

## the six scenes

| at | painting | what he adds |
| --- | --- | --- |
| 0:00 | harbour, pencil and watercolour | the colour: it follows his brush across the sketch |
| 0:10 | plum branch, ink | a blossom at every hop, then a seal in the corner, stamped with his own body |
| 0:20 | night town, gouache | the lit windows, then the stars and the moon in one sweep |
| 0:30 | sunflowers, thick paint | each sunflower; the last one grows under him |
| 0:40 | koi pond, from above | the patches on the two white koi |
| 0:50 | the gallery | a small self-portrait |

## how it was made

It is one HTML file with no libraries and no image files. Everything is drawn in canvas 2D.

- **Each painting is painted once.** When the page loads, the still part of every scene is drawn into its own layer: about 3,400 short strokes for the sunflower sky, placed along a flow field that curls around the sun; bristle strokes for the ink branch; flat shapes with a darker dried edge for the watercolour. Each frame only draws the things that move on top.
- **The harbour is painted twice**, once as pencil outlines and once in colour, from the same shapes. The colour is shown only behind a wobbly edge that follows the brush.
- **The framed pictures in the gallery are the real scenes.** The last frame of each scene is drawn into its frame, without the mascot.
- **Every frame is worked out from the film time**, so the film can start at any second and the scene changes can draw two scenes at once: the new one through a mask of seven wide brush strokes.
- **The sound is made in the page** with Web Audio: a plucked tune with a different four-chord loop per scene, and small sounds for the action.

The sound was checked for errors but not listened to by the model that wrote it.

## credit

The format comes from a one-minute canvas film posted by [@chetaslua](https://x.com/chetaslua/status/2121704006779290054): the mascot finishing a painting in each scene, drawn in pure JavaScript. The six paintings here are new. The character is the Claude Code mascot, which belongs to Anthropic.
