Make a single self-contained HTML file: a small open-world driving game scene called "joyride, 6 p.m.". Use three.js 0.170 from a CDN through an import map (the core, plus its EffectComposer bloom add-ons). No downloaded models, textures or sounds: everything is made in code. It is an original city, not a copy of any existing game's map, cars or brands.

THE PLACE
A sunny coastal city at golden hour. A grid of 7 by 7 blocks with a four-lane road between every pair, sea and beach to the west, hazy hills to the east and north.

- Downtown in the middle: glass towers 70 to 220 metres tall, the taller ones stepping back partway up, with a crown and an antenna. Around them, mid-rise offices and flats. At the edges, low brick shops and apartment blocks. Two blocks are parks (lawn, paths, a fountain, benches, trees). A few are car parks full of parked cars.
- Six kinds of facade, each a hand-drawn window texture tiled over the building: blue glass, bronze glass, concrete office, stucco flats with balconies, brick, white modern. Windows have frames, sills, half-drawn blinds, rain stains and a streak of reflected sky. Most buildings have a band of shopfronts at street level with signs, doors and awnings, and rooftop units behind a parapet.
- Roads are painted in detail on one large ground texture: double yellow centre line, dashed lane lines, edge lines, stop lines, zebra crossings at every junction, tyre wear down each lane, manhole covers, skid marks and tar repairs. Raised tiled sidewalks.
- Street lamps down both sides of every road. Palms along three boulevards, round trees elsewhere, each in a square of earth. Traffic signals on mast arms at every junction, and they work: north-south green, amber, east-west green, amber.
- A few rooftop billboards with invented brands.

WHAT MOVES
- Traffic: about sixty cars in several colours and proportions (saloon, 4x4, van, small car). Each keeps to its lane, drives on the right, stops at red lights, and brakes for the car in front and for the player.
- People walking round the blocks on the sidewalks.
- The player's car: a low orange sports car with a spoiler, wheels that spin and steer, brake lights.

DRIVING
It opens on a slow flight around downtown. On click, the player takes the car. W and S for throttle and brake/reverse, A and D to steer, Space is the handbrake and lets the back slide. Arcade handling: quick, forgiving, top speed around 200 km/h, slower on sidewalks. The car cannot pass through buildings, parked cars or traffic; it bounces off and loses speed. Pedestrians are not affected by the car. C cycles three cameras (chase, bonnet, high and far). R puts the car back at the start.

On screen while driving: a round minimap bottom-left that turns with the car and shows roads and traffic, speed in km/h bottom-right, and the names of the nearest avenue and street top-right. Invent the street names.

LIGHT
Golden hour by default: sun in the west over the sea, long soft shadows that follow the player, warm light, peach haze the colour of the horizon. Glass towers and car paint reflect the sky. A little bloom.

T fades to night over a few seconds: stars, windows lit at random in every building, glowing shop signs and billboards, street lamps with pools of light on the road, brighter head and tail lights, and the player's headlights lighting the road ahead.

Sound on first click: an engine note that rises with speed. M mutes.

Keep it smooth on a laptop: instance everything that repeats (cars, people, trees, lamps, small boxes), cap the internal resolution, lower it further if frames get slow, and use a lighter mode with no bloom when the window is small. Hide the on-screen text when the window is very small. Handle resize.
