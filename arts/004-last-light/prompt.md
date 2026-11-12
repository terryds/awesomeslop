Make a single self-contained HTML file: a small 3D world called "last light" that you can walk around in. Use three.js 0.170 from a CDN through an import map. No other libraries, no downloaded models, textures or sounds: everything is made in code.

THE PLACE
A small island at dusk, about 250 metres across, alone in an open sea. The sun has just touched the horizon. The island is rolling meadow with stands of pine, a sand beach all the way round, and one high headland on the east side. On the headland stands a white lighthouse with two red bands. On the opposite shore there is a wooden cabin with lit windows and a pier running out over the water, with a lantern at its end.

THE LOOK
Low-poly and flat-shaded, like a paper model lit by a sunset. Every triangle of the land has one flat colour: sand near the water, two greens for meadow, grey where it is steep. Warm orange light from the low sun, violet in the shadows. Distance fades into a peach haze that is exactly the colour of the sky at the horizon, so the sea has no hard edge.

Sky: a gradient from peach at the horizon to deep indigo overhead, a small bright sun, and clouds cut from one noise field with a hard edge so they look painted, pink where they face the sun. A few stars and a thin crescent moon.

Sea: no geometry waves. Fake them in the shader with a few moving sine waves that tilt the surface, reflect the sky, and leave a long glittering path under the sun. Turquoise in the shallows, navy in the deep. White foam bands that run up the beach.

Grass: tens of thousands of single blades, dark green at the root and gold at the tip, swaying in the wind. Only draw one patch of them around the viewer and wrap it as they move, so the meadow seems endless. No grass on sand or steep rock.

THE LIGHTHOUSE
The lamp turns once every 15 seconds and throws two opposite beams: long, soft cones of light visible in the haze. As a beam passes, it must visibly rake across the meadow, the trees and the water. This sweep is the heart of the piece; if something has to give, keep this.

Fireflies over the meadow. A warm glow from the cabin windows and the pier lantern.

WALKING
It opens on a slow drifting tour at head height that keeps the lighthouse in view. On click, the visitor takes over: mouse to look (pointer lock, with drag-to-look as a fallback), WASD or arrows to move, Shift to run. They stay on the ground, cannot walk into the sea, the lighthouse, the cabin, trees or big rocks, and can walk out along the pier.

T fades between dusk and night over a few seconds: the sun's light goes, the sky turns near-black, stars and moon come up, moonlight on the water, fireflies and the beam get stronger.

Sound starts on the first click: surf that swells every nine seconds or so and a quiet wind, both made from filtered noise. M mutes.

Show a small "click to walk" hint with the keys, and hide it once they are walking. Hide all text when the window is very small.

Keep it smooth on a laptop: no shadows, no post-processing, cap the pixel ratio and lower it if frames get slow. Handle window resize.
