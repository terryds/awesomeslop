# little band

A needle drops on a record, and three round birds join in one at a time: one plucks a guitar with its beak, one hops on a snare drum, one runs along the keys of a piano. Thirty seconds, in one small room.

**Click for sound.** Then click or space to pause, ← → to skip 5 seconds, M to mute. Add `?t=19` to the address to start at 19 seconds.

## how it was made

The whole film is one Python file, [film/band.py](/a/016-little-band/film/band.py), run by Blender with no window open:

```bash
blender -b --factory-startup -P film/band.py -- 0 719 1080 frames
```

- **No assets.** The room, the record player, the guitar, the drum, the piano's 49 white keys and the birds are all built by the script from boxes, cylinders, spheres and curves, with rounded edges.
- **No keyframes.** One `update(T)` function poses everything for a time `T`: the record, the tone arm, each bird, each string and key, the floating notes and the camera. Any frame can be rendered on its own, so the film renders in four pieces side by side.
- **One room, five cameras.** Every instrument keeps playing whether or not it is in shot, so the wide shot at the end is the same band you met one by one.
- **Post.** ffmpeg adds a little bloom, a fade at each end, and the music.

## music and sync

The music was generated with ElevenLabs Music from a five-section plan at 80 BPM. The beat grid was then measured from the audio (a beat every 0.75 seconds, music starting 1.56 seconds in), and the animation is timed to it: the needle drops in the silence before the first note, the cuts fall on bar lines, and plucks, hops and hi-hat taps land on beats.

The sync is to the beat, not to the notes: the piano keys the bird presses are not the notes you hear.

## credit

The idea of a short music video with instruments in a warm room, animated in Python and rendered in Blender, comes from a music video by [@kevin_t_ngo](https://x.com/kevin_t_ngo). The characters, room and music here are new.
