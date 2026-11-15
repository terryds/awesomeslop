# odd sock

A laundromat at night. One odd sock on top of the washing machines sings a disco song about its missing pair, a mirror ball comes down, and in the last chorus the door of the middle machine springs open. Seventy-six seconds.

**Click for sound.** Then click or space to pause, ← → to skip 5 seconds, M to mute. Add `?t=48` to the address to start at 48 seconds.

## how it was made

The whole film is one Python file, [film/sock.py](/a/017-odd-sock/film/sock.py), run by Blender with no window open:

```bash
blender -b --factory-startup -P film/sock.py -- 0 1825 1080 frames 64
```

- **No assets.** The room, the five machines, the neon sign, the gauges, the mirror ball, the socks, the pegs and the bottle are all built by the script from boxes, cylinders, spheres, curves and text.
- **No keyframes.** One `update(T)` function poses everything for a time `T`, so any frame can be rendered on its own and the film renders in four pieces side by side.
- **The mirror ball's dots are worked out, not lit.** For each of 170 directions the script finds where a ray from the ball meets the floor, a wall, the counter or the machine fronts, and lays a small glowing disc there.
- **Post.** ffmpeg adds a little bloom, a fade at each end, and the song.

## the song drives the picture

The song was generated with ElevenLabs Music from a seven-section plan with lyrics ([film/music-plan.json](/a/017-odd-sock/film/music-plan.json)). The finished track was then measured by [film/analyze.py](/a/017-odd-sock/film/analyze.py), which writes [film/data.json](/a/017-odd-sock/film/data.json):

| measured | how | what it moves |
| --- | --- | --- |
| loudness of bass, drums, vocals and the rest, per frame | the track split into stems | dial needles, level lights, the bottle's bobbing |
| the beat grid (120 bpm, first beat at 0.10 s) | the drum stem | hops, spot colours, cuts |
| every kick drum hit | the drum stem below 120 Hz | flashes, the glow inside the drums |
| the time of every sung letter | the lyrics aligned to the vocal stem | the mouths: wide for "a", round for "o", shut for "m", "b", "p" |

The measurements also changed the plan. The first half of each chorus turned out to have no drums, so those eight seconds became the quiet part: one spotlight, the mirror ball coming down, a slow turn. The full lights wait for the drums.

The mouth follows the letters, not the sounds, so it is approximate: "through" opens as if every letter were sung.

## credit

The idea of a sung music video animated in Python and rendered in Blender comes from a music video by [@kevin_t_ngo](https://x.com/kevin_t_ngo). The song, characters and set here are new.
