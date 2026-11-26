# close-up portrait

Ten seconds, one continuous take, very close to a face. She looks at the camera, glances to the right, blinks twice, closes her eyes for a moment, turns slowly toward the window into profile, raises her eyes, then turns back and finds the camera again.

The video plays muted; use its controls for sound.

## how it was made

A single prompt to Veo in the Gemini app. Unlike the other pieces here, there is no code: the clip comes straight from the video model. The original Gemini chat is shared here: [share.gemini.google/MZIfpF044Ivm](https://share.gemini.google/MZIfpF044Ivm).

The prompt is unusually long, about 27,000 characters, and reads like a shot list for a performance:

- **Framing to the percent.** Where each iris sits in the frame, where the lip line and chin fall, how the crop changes as the head turns.
- **Light.** Soft overcast window light from the upper left, a small window reflection in the near eye, which highlights move as the nose turns.
- **Skin, lashes and hair.** Pore scale by area, how the eyelid crease flattens on a blink, which loose strands cross the nose and lips and how their tips lag behind the head.
- **A second-by-second timeline.** Eleven beats from 0.00 to 9.00 s: blinks at 1.38 s and 2.83 s, a longer eye closure at 3.58 s, the profile turn at about 5.75 s, a raised gaze, the turn back at about 8.21 s and a last blink.
- **A negative prompt.** A long list of what must not happen: face redraws, jumping irises, hair whipping in the wind, light switching sides, colour casts, push-ins, handheld shake, watermarks, new people.

The prompt also asks the model to lock the face to a first-frame reference image.
