# sword of the yellow wood

An autumn wood in the last hour of sun, painted in oils, that you can walk through with a sword. There are bears.

**Click the scene, then:** the mouse looks around. W A S D walk, Shift runs, Space jumps. Click again (or press F) to swing the sword: three clicks make a combo that ends in a leaping chop. Right click (or E) dodges. M turns the sound off. Esc lets go of the mouse.

A footpath loops through the wood, and in the middle there is a clearing with one old red tree, kept by one old bear. Seven more bears wander the wood. They leave you alone until you come close; you can outrun them. A bear growls and rears up before it swipes, which is the moment to dodge. A hit knocks a brown bear out of its swipe; the old one has to be dodged. You have five hearts: red mushrooms mend one each, and there are twenty golden acorns to find. If you fall, you wake up on the path.

## what you're looking at

Nothing is filtered. A normal 3D scene is never drawn and then made to look painted; the world itself is made of paint.

- **About 335,000 brush strokes.** Each is one flat rectangle in one flat colour, cut to the shape of a brush mark by a few lines of shader: streaks where the bristles ran, ragged ends where each bristle stopped, a ridge of thick paint down one side. Leaves are single pointed touches.
- **Three paints per thing.** A shadow colour, a middle and a light. A stroke takes one of them by how lit its spot is, and they are never blended. That is why a birch reads as cream on one side and lilac on the other.
- **Paint that holds still.** Every stroke is fixed in the world and sits at its own tiny depth, decided once. Nothing is sorted by distance to the camera, so nothing crawls or flickers as you move.
- **Painted shadows.** At the start, the shadow of every trunk and every clump of leaves is drawn on a hidden flat canvas, as seen from above. Each ground stroke looks up its own spot in that picture and takes sunlit gold or shadow plum.
- **A sky of 2,800 strokes**, swept in rings round the sun.
- **The walker and the bears are strokes too.** Because they move, their strokes choose their paint again every frame, and go dark when they step into a tree's shadow. A bear that is hit flashes pale, squashes, and throws off dabs of paint.
- **A blade that paints.** While the sword cuts, a pale stroke is laid each frame between where the blade was and where it is, and thins away in a fifth of a second.

## things worth stealing from the prompt

- **Say "do not filter the frame".** Ask for the surfaces to be covered in strokes that are fixed in the world. A filter gives paint that swims over the picture.
- **"Stroke order must never depend on the camera."** In practice: no transparency, no sorting, every stroke writes depth and has its own fixed lift off the surface.
- **Three named paints per object, never blended.** It is the cheapest way to get a painted look instead of a gradient.
- **Plain dark shapes under the strokes.** Gaps between strokes then read as underpainting, not as holes.
- **Draw the shadows once, from above, on a 2D canvas.** With a low sun and a still world you do not need shadow maps.
- **Lay ground strokes along the direction of the light.** Long shadows then look brushed in one go.

## what makes a hit feel like a hit

All of these were asked for by name in the prompt, and each is a few lines:

- the game **freezes** for a few hundredths of a second when a blow lands, longer for the chop;
- the **camera shakes**;
- each swing **steps you forward** and turns you to the nearest bear;
- a click during a swing is **remembered** and starts the next one, so the combo never drops a press;
- the bear **warns you** (a growl, half a second reared up) before it swipes;
- every one of those has a **sound**, made in the page.

## limits

- Desktop first. On a phone you can watch, and drag to look after a tap, but there are no keys to walk with.
- The light does not change: it is always the same late afternoon.
- You are turned back about 60 m from the middle; the wood beyond is there to be looked at.
- One kind of enemy, no levels or loot.
- No music, only effects.

## credit

The idea, a walkable world painted with brush strokes and not filtered afterwards, and the rule that stroke order must not depend on the camera, come from ["a walkable oil-painting world"](https://x.com/rewind02/status/2121575140307706285) by rewind. No code or assets were used from it. The wood, the walker and all the shaders here are new.
