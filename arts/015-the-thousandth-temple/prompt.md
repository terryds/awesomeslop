Make a single self-contained HTML file: a short animated "video podcast" called "the thousandth temple", about Candi Prambanan in Java and the legend told about it. About two and a half minutes, looping. Every frame is drawn live with JavaScript on a 2D canvas, with no libraries. The hosts, the studio, the diagrams and the music are made in code. Two things are real and sit next to the file: six photographs of the place (freely licensed, from Wikimedia Commons, credited on screen) and the two voices (recorded with ElevenLabs, one small mp3 per line).

THE FORMAT
Two hosts sit at a desk with microphones, in front of one big screen. The film is a conversation, cut like a podcast video, with hard cuts between four shots:
- the screen alone, filling the frame;
- a two-shot: the screen as the whole background, a host in each bottom corner, laptops on the desk;
- a close-up of either host in the studio, with the edge of the screen still showing what is on it.
A mouse cursor lives on the screen: it glides to what is being talked about and a soft yellow disc pulses under it when it lands. The screen has its own camera that pushes in slowly and zooms to details.
Captions: a dark rounded pill near the bottom with three or four words at a time in bold white; the word being spoken is coloured (warm orange for her, mint for him).
Stage 1280 by 720 with rounded corners, fitted inside any window on a near-black page.

THE HOSTS (flat cartoon, dark outlines, three-quarter view, facing each other)
- Laras, on the left: sage-green hijab, terracotta top, a small gold brooch, cream headphones over the hijab. She knows the place.
- Dimas, on the right: black wavy hair, rectangular glasses, a brown batik shirt in the kawung pattern (draw the pattern), dark headphones. He guesses.
Mouths open and close on the syllables of each word. They blink, bob a little when talking, and have five faces to cut between: neutral, smug, shock, thinking, flat. In close-up the speaker's hand comes up and moves. The studio: dark green wall, a warm lamp glow, a length of parang batik hanging, a rattan lamp, mugs.

THE SCREEN (photographs for what is real, drawings for what has to be explained)
Photographs, each drawn 1280 wide and as tall as it comes so the screen's camera can move over it, with "photo: name, licence" small in the top right corner:
1. pano.jpg: the towers by day. He counts them with the cursor.
2. piles.jpg: the same towers seen across a field of fallen blocks. "They're the piles."
3. durga.jpg (a tall photo): the statue in its chamber, shown whole in the middle of the frame over a dark, enlarged piece of the same wall. Labels "eight arms" and "a buffalo" appear when he points; later a slow push in to the face.
4. sewu.jpg: Candi Sewu, with a small name plate.
5. night.jpg: the towers floodlit gold, for the ending and the title card.
6. boko.jpg: the gate of Ratu Boko, as a small print pinned on the map.
Drawings:
7. A ground plan on cream paper, north up: two square walls; the three big temples in a row, the three facing them, labels; then 224 small squares filling four square rings (44, 52, 60, 68) one after another while a big number counts to 240.
8. An encyclopedia page of your own (plainly labelled as written for the film): title, three short paragraphs with blue links, a box at the side with the day photo. Two phrases get selected, left to right, as they are said: "at least 75% of its original stones" and "Durga, slayer of the buffalo demon".
9. The legend as wayang kulit: a lamp-lit cloth that flickers, puppets as dark silhouettes with pierced patterns and rods, a leaf-shaped gunungan sweeping across to change scenes. Four scenes: the prince strikes down the giant king; the prince and the princess, and her demand ("× 1000, before sunrise"); the night's work (spirits rise, small temples pop up in rows while a counter runs to 999, then women pound a rice trough, a glow and flames rise in the east, a rooster crows "kukuruyuuuk!", the spirits flee); the curse (a white flash, and she is grey stone on a plinth; the counter reads 1000).
10. A simple map: Prambanan, Candi Sewu 800 m north, Ratu Boko 3 km south on its hill, Merapi, the Opak river, the road to Yogyakarta.

THE SCRIPT (short lines, a running joke about counting; get the facts right)
Open on the temples. He: "How many temples is that?" She: "Guess." He counts with the cursor: "One, two, three... six? Eight?" She: "Two hundred and forty." "Where?!"
The plan: three for Shiva, Vishnu and Brahma; three facing them for the animals they ride ("The gods have parking?" "A bull, an eagle, and a swan."); 224 small ones in four rows. "And where did those go?" "They're the piles." An earthquake in the 1500s; you may only rebuild one if you find 75% of its stones. "So it's a jigsaw." "With pieces in people's houses."
"But I heard a thousand temples. Built in one night." "Ah. That's the other story." Tell the legend of Roro Jonggrang over the shadow play: Bandung Bondowoso kills the giant king Boko, falls for his daughter; she cannot refuse, so she asks for a thousand temples before sunrise; he calls up spirits; at 999 she wakes the village to pound rice and light fires in the east; the roosters crow, the spirits run; he is one short, knows who did it, and turns her to stone: temple number one thousand.
"And she's still there. North room of the Shiva temple." He: "Hang on. She has eight arms. And she's standing on a buffalo." "Because that's Durga. A goddess, killing a demon. Carved around the year eight fifty." "So the story's wrong?" "The story's younger. The kings moved away. The towers fell. Centuries later, people found a stone woman in the dark. And explained her."
"And the thousand temples?" "Next door. Candi Sewu. It means 'a thousand temples'." "And it has a thousand?" "Two hundred forty-nine. And it's Buddhist."
End at dusk: "So. How many temples?" "You answer." "Nine hundred ninety-nine. And one princess." "I'll allow it." "Oh. And never bring a date here." "Why?" "They say you'll break up. She's still angry." Then a title card over the floodlit towers.

TIMING AND SOUND
Write the script as a list of lines (who, text, and whatever changes on that line: shot, picture, camera, cursor, face). Build one timeline from it, and name the moments the pictures need ("the word 'stone'") so nothing is timed by hand. ?t=<seconds> starts anywhere; ?hold freezes there.
- Voices: write a small Node script that sends each line to ElevenLabs (text to speech with timestamps, a different voice for each host), keeps each answer in a cache so nothing is paid for twice, saves one trimmed mp3 per line (v00.mp3, v01.mp3, ...) and writes into the page, as one constant, where every line starts, how long it is, and when each of its words starts and ends. The page builds its timeline from that, so captions and mouths are on the word. When a line starts, its clip plays, and while it plays the film's clock follows the clip. Keep the clips separate, not one long track: skipping then needs no seeking inside a file.
- If that constant is empty, fall back: give every word a length from its letter count, and speak the lines with the browser's own speech voices.
- Music: a quiet gamelan loop in a five-note pelog tuning, made in the page: bell tones from a few sine partials with a slightly detuned twin, a 32-beat melody, a lower bell every fourth beat, a gong at the end of the cycle.
- A few effects, also made in the page: a tick when the cursor counts, wooden knocks for the rice pounding, a rooster, a gong on the curse.
Sound starts on a click ("click for sound" hint). Click or space pauses, left and right skip 5 seconds, M mutes, V turns the voices off. With ?thumb=1: no hint, no sound.
