Make a 76-second animated music video called "odd sock", built and animated entirely in Python and rendered with headless Blender (EEVEE with ray tracing). No imported models, textures or keyframes: one Python file builds the whole set from primitives and poses every frame from the time and from measurements of the song. Square, 1080 × 1080, 24 frames a second.

THE STORY
A laundromat at night. One odd sock lies on the counter above the washing machines. The machines start by themselves, the strip lights flicker out, a neon sign comes on, and the sock stands up and sings a disco song about its missing pair. In the bridge it goes to the edge and looks down through the glass of the middle machine: the other sock is in there, tumbling slowly. The door springs open, the pair jumps out and up onto the counter, and they finish the song together. When the song ends the strip lights come back on and they are just two socks lying side by side.

THE SET
Pale mint walls, a wet checker floor, a row of five white front-loading washing machines along the back wall with a folding counter on top: that counter is the stage. Each machine has a chrome porthole with a drum of coloured laundry turning behind the glass, a round dial with a red needle, a row of eight level lights (green, amber, red) and an amber display. On the wall above: a pink neon sign, "SPIN CYCLE", with "open all night" in blue under it; copper pipes with four big brass gauges; a clothes line. On the ceiling: two fluorescent strip lights, a rail of six coloured spotlights, and a mirror ball that comes down for the chorus. A pink laundry basket and a bench on the floor.

THE CAST
- The singer: a mustard sock with a coral cuff, heel and toe and teal stripes, big round eyes with eyelids, pink cheeks and a mouth. A small microphone on a stand.
- The missing one: the same sock.
- Backing singers: three wooden clothes pegs on the line, each with a painted tip and two eyes; they sing by opening their legs.
- Bass: a blue detergent bottle with a red cap, a face on its label, two white gloves and a small orange bass.

THE MUSIC
Generate the song with ElevenLabs Music from a composition plan: disco pop, 120 BPM, A minor, four-on-the-floor kick, funk bass, guitar chops, disco strings, a bright female lead. Sections: intro 8 s (a washing-machine hum that turns into the kick), verse 16 s, pre-chorus 8 s, chorus 16 s, bridge 8 s, final chorus 16 s, outro 4 s. Lyrics:

Verse: Went in as a pair on a Friday night / Warm water, low light, you were holding tight / Then the drum went round and the door swung wide / Now I'm one odd sock on the folding side
Pre-chorus: Every dial is shaking, every light turns blue / Forty degrees and I'm still missing you
Chorus: Spin cycle, spin me back to you / Round and round till the wash is through / Spin cycle, I'm no good as one / Don't stop turning till the night is done
Bridge: Is that you behind the glass? / Tumbling slow, at last, at last
Final chorus: Spin cycle, you spun me back to you / Round and round, now the wash is through / Spin cycle, we're a pair again / Leave the light on, play it once again

Then measure the finished track instead of trusting the plan: split it into stems (vocals, bass, drums, guitar, other), align the lyrics to the vocal to get the time of every sung letter, find the beat grid and every kick drum hit from the drum stem, and save the loudness of each stem for every film frame.

EVERYTHING FOLLOWS THE SONG
- Dial needles and level lights show the loudness of one stem each: bass, drums, vocals, the rest. They sit at zero before the music and fall back to zero when it ends.
- The drums behind the glass turn slowly in the verse, fast in the full chorus, and coast to a stop at the end.
- The spotlights change colour on every beat in the full chorus and everything flashes on each kick drum hit.
- The mirror ball throws moving dots of light over the floor, the walls and the machines.
- The sock's mouth opens on the sung letters: wide for "a", round for "o", shut for "m", "b" and "p". The pegs sing the chorus.
- Do what the words say: all the dials shake on "every dial is shaking", the lights turn blue on "every light turns blue", the middle dial and display read 40 on "forty degrees", the sock turns once on "round and round".
- Soap bubbles rise in the full chorus.
- Cut only on beats, mostly on bar lines.

THE LOOK
Soft, toy-like 3D: rounded edges, enamel and chrome, knitted socks. Cold flat light from the strip lights at the start and end; in between, only neon, coloured spots through a thin haze, a follow spot on the singer and the glow from inside each drum. Shallow depth of field on the close shots, a little bloom added afterwards.

Put it together with ffmpeg and show it on a plain page: the video fills the window, loops, starts muted, click for sound.
