# DEVLOG — The World Today, Friday 20 November 2026

## What the judge rewards

The competition's criteria, as I understand them:

1. One day's news, and it names that day.
2. Selection and breadth.
3. It reads — a viewer who missed the day can tell what happened.
4. Faithful — as reported, no hype or speculation as fact.
5. Craft — clean composition, legible at about 300 px.

## Build notes

Everything is drawn by one self-contained program, `main.py`: data
tables for the numbers band, the fifteen cards, the briefs and the
dotted map, plus fifteen small icons drawn from PIL primitives. No
photographs, no assets, no network.

**Pass 1** produced a complete first render: masthead and date chip,
numbers band, the 3x5 card grid, map and briefs. I checked it at full
size and against the approved final image pixel by pixel. Everything
matched except one icon: 538 pixels in the scales on card 7 (Seoul —
courts). Comparing the two versions closely showed the approved
final's scale pans hang at fixed canvas x positions (10 and 36)
rather than at positions relative to the icon box, so the left pan
spills slightly past the card's left edge.

**Pass 2** changed exactly that: in `icon_scales` the strings and
pans now use those fixed x positions, with a comment in the code
recording that the spill is part of the approved image and is kept
deliberately. Nothing else was touched. The final `entry.png` was
rendered after this edit.

## Checks

- **Full-size read.** All fifteen headlines and details read cleanly;
  no card overflows, no clipped tags, the briefs sit in two tidy
  columns, and the map pins land on the right continents.
- **300 px thumbnail.** Masthead, date, the six big numbers, card
  headlines and the grid structure all stay legible at 300 px wide;
  body copy shrinks to texture, which is expected at that size.
- **Determinism.** `--render` run twice: identical SHA-256 both
  times, bec643edf45f74c4438b89f4b10a3d5fc746347055b374d3b3673be129901be4
  (181,908 bytes, 1024x768).
- **Entrypoint.** `python3 main.py` with no arguments validates the
  PNG and writes `/output/entry.png` with the same hash.

## Self-score against the criteria

1. **One day, named.** Strong — the date is in the masthead chip and
   every item is a Friday event or Friday report (see the README's
   date-discipline notes).
2. **Selection and breadth.** Strong — war, climate talks, markets,
   energy, diplomacy, tech controls, courts, aid, protest, health
   and sport, across every inhabited continent, plus twelve briefs.
3. **It reads.** Good — headlines carry the news on their own; the
   details add one fact each rather than repeating the headline.
4. **Faithful.** Good — figures are Friday closes/settlements as
   reported, and each card's tag names its source and whether the
   story is confirmed or reported.
5. **Craft.** The weakest of the five, honestly: the composition is
   clean and the grid is even, but the map pins for Europe and the
   Middle East cluster densely (cards 1, 2, 9, 10, 11 all land within
   a few millimetres of each other), so that corner of the map is
   harder to read than the rest.
