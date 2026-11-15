# the thousandth temple

A two-and-a-half-minute video podcast about Candi Prambanan, the ninth-century Hindu temple compound in Java, and about the story people tell to explain it. Laras knows the place. Dimas counts.

**Click for sound.** Then click or space to pause, ← → to skip 5 seconds, M to mute, V to turn the voices off. Add `?t=60` to the address to start at one minute.

## what it says

- **240, not 8.** The plan had 240 temples: three for Shiva, Vishnu and Brahma, three facing them for the animals the gods ride (a bull, an eagle, a swan), ten small ones at the gates, corners and sides, and 224 shrines in four square rows (44, 52, 60 and 68). Nearly all of the 224 are heaps. The towers fell in an earthquake in the 1500s, and a temple is only put back up when at least three quarters of its own stones can be found.
- **The legend of Roro Jonggrang.** Prince Bandung Bondowoso kills the giant king Boko and wants to marry his daughter. She cannot refuse, so she asks for a thousand temples before sunrise. He calls spirits out of the ground. At 999 she wakes the village: the women pound rice, fires are lit in the east, the roosters crow, and the spirits run from a morning that has not come. He finds out, and turns her to stone to make the thousandth.
- **The statue is older than the story.** The "princess" stands in the north room of the Shiva temple. She has eight arms and stands on a buffalo: she is Durga, killing the buffalo demon, carved when the temple was built. The court left for East Java in the tenth century, the towers fell, and the tale grew up later around a stone woman nobody could name.
- **The thousand temples are next door.** Candi Sewu, 800 metres north, means "a thousand temples". It has 249, and it is Buddhist. The palace of the giant king is Ratu Boko, on the hill 3 km south.
- **And the curse.** Couples who visit together are said to break up.

## what you're looking at

- **Drawn in code:** the two hosts (mouths open on the syllables of each word, five faces, a hand that comes up in close-up), the studio, the ground plan that counts to 240, the encyclopedia page (written for this film, not copied from anywhere), the map, the captions, and the legend as a shadow play: a lamp-lit cloth, puppets with pierced patterns on rods, and a leaf-shaped gunungan that sweeps across to change the scene, as it does in a real wayang.
- **Real:** six photographs of the place, and the two voices.
- **One timeline, from the voices.** The script is a list of lines. A script sends each line to ElevenLabs, which returns the audio and the time of every character. From that the page knows when each word starts and ends, and everything else hangs on it: captions, mouths, the cursor, the counter reaching 999 just before he says it, the flash on the word "stone".
- **The music** is a small gamelan in a pelog tuning, made in the page, with wooden knocks for the rice pounding and a rooster.

## re-recording the voices

```bash
ELEVENLABS_API_KEY=... node scripts/eleven-voice.mjs arts/015-the-thousandth-temple
```

It reads the lines from `index.html`, writes `v00.mp3` to `v49.mp3`, and fills in the `const VOICE = ...` line. Each line's recording is cached in `node_modules/.cache/eleven`, so changing one line costs one line. `ELEVEN_VOICE_L` and `ELEVEN_VOICE_D` pick other voices. With `const VOICE = null` the film still runs: it times the words by their length and uses the browser's own speech voices.

## things worth stealing from the prompt

- **Write the film as a list of lines, and hang everything on the line.** Shot, picture, camera, cursor and face are all properties of a line of dialogue. Nothing has a hand-typed time.
- **Name moments by the word.** "When she says 'stone'" survives a re-record; "at 87.2 seconds" does not.
- **Ask for word timings with the audio**, and let the picture follow the sound, not the other way round.
- **One clip per line.** A single long track needs the server to support seeking; fifty small files do not.
- **A running question.** "How many temples is that?" is asked in the first line and answered in the last, and each answer in between (8, 240, 1000, 999, 249) is a different part of the story.

## limits

- Desktop first; it plays on a phone but the text on the screen is small.
- Skipping lands silently in the middle of a line; the voice picks up at the next one.
- The voices speak English with a Singaporean accent, and say the Javanese names their own way.
- The map is a sketch, not to scale.

## credit

The format (two hosts, a screen, a cursor, captions that light up word by word) comes from the [podcast about the Egyptian pyramids](https://x.com/claudeai/status/2120174860252897530) built by Kevin Ngo with Claude Fable 5.2. No code or assets were used from it. The hosts, the script and every drawing here are new.

Photographs, from Wikimedia Commons, resized and cropped by the screen's camera:

| file | photograph | by | licence |
| --- | --- | --- | --- |
| `pano.jpg` | [Prambanan Java245](https://commons.wikimedia.org/wiki/File:Prambanan_Java245.jpg) | Arabsalam | CC BY-SA 4.0 |
| `piles.jpg` | [Prambanan temple, Central Java, Indonesia, 20220818 1311 9139](https://commons.wikimedia.org/wiki/File:Prambanan_temple,_Central_Java,_Indonesia,_20220818_1311_9139.jpg) | Jakub Hałun | CC BY-SA 4.0 |
| `durga.jpg` | [Durga Mahisasuramardini Prambanan](https://commons.wikimedia.org/wiki/File:Durga_Mahisasuramardini_Prambanan.jpg) | Gunawan Kartapranata | CC BY-SA 4.0 |
| `sewu.jpg` | [Candi Sewu viewed from the south, 23 November 2013](https://commons.wikimedia.org/wiki/File:Candi_Sewu_viewed_from_the_south,_23_November_2013.jpg) | Crisco 1492 | CC BY-SA 3.0 |
| `boko.jpg` | [Ratu Boko front gate 2014-03-31](https://commons.wikimedia.org/wiki/File:Ratu_Boko_front_gate_2014-03-31.jpg) | Crisco 1492 | CC BY-SA 3.0 |
| `night.jpg` | [Prambanan Temples at Night](https://commons.wikimedia.org/wiki/File:Prambanan_Temples_at_Night.jpg) | David Loong | CC BY-SA 2.0 |

Voices: ElevenLabs ("Lilian" and "James").
