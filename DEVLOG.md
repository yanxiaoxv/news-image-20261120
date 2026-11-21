# DEVLOG — news-image-20261120 build notes and self-scores

Judge criteria (from the kit, in the judge's own order):
1. One day's news, and it names that day.
2. Selection and breadth.
3. It reads — a viewer who missed the day can tell what happened.
4. Faithful — as reported, no hype or speculation as fact.
5. Craft — clean composition, legible at about 300 px.

## Draft v1 (morning of 20 Nov 2026, CST)

First render: 1024x768, 179,588 bytes. Layout carried over from the
19 November page the user approved: masthead + numbers band + 15
cards + dot map + briefs.

Self-score against the five criteria:
1. Date discipline — strong by design. Every card is an event of,
   or first reported on, Friday 20 Nov; seven Thursday stories were
   deliberately held back (see README, "Considered but not
   printed"). Weakest point: cards 5 and 17 are follow-throughs of
   Thursday events and must stay framed as Friday developments.
2. Breadth — war, climate, markets, energy, diplomacy, tech
   controls, courts, humanitarian aid, EU–UK, protest, big tech,
   environment, health, sport; Europe, Middle East, Asia, Africa,
   the Americas and Oceania all appear. Weakest: no Latin America
   story made the cut on Friday morning's wires.
3. Readability — headlines carry the news; details add one fact
   each. Weakest: the map's Europe/Middle East pin cluster.
4. Faithfulness — every figure traced to a named wire or official
   release; claims are tagged as claims (tags say REPORTED where
   sourcing is single-wire).
5. Craft — weakest criterion in v1: the footer line was clipped by
   the briefs block, three icons (missile, scales, cricket bat)
   read poorly, and one brief ran off its line.

## Polish round 1 → v2 (same morning)

- Card height 93 → 91 and the bottom band moved up 10 px; the
  footer now sits clear of the briefs and nothing is clipped.
- Map pins shrunk (r 7 → 5.5) and the Europe/Middle East pins
  nudged apart; all 12 placed pins are individually readable.
- Missile, scales and cricket icons redrawn; the scales' pans are
  now solid dishes and the missile has fins and a flame trail.
- Brief 26 shortened so its source credit fits its line.
- Re-rendered: 1024x768, 179,192 bytes. Checked at full size and at
  300x225: masthead, date pill, numbers and headlines stay legible
  at thumbnail size; no overlaps anywhere on the page.

Self-score after round 1: criterion 5 (craft) is now the weakest of
the five rather than failing; criterion 1 remains the one to defend
at final edition, when late-Friday stories (COP31's close, APEC's
wrap, US Friday trading) may displace morning cards.

## Final edition (evening of 21 Nov 2026, CST)

Headline refresh carried out after 20 November ended in every time
zone. All three flagged risk points moved and were re-based:

- **Card 2 (COP31):** the draft's "final day, no deal in sight"
  became the outcome — talks extended into Saturday, Kurum
  adjourning Friday's plenary with finance and fossil fuels
  unresolved, a third draft due Saturday. Tag changed to
  HURRIYET / AFP.
- **Card 3 (markets) and the numbers band:** morning intraday
  figures replaced with closes — Nikkei −5.06% at 56,436.65
  (fifth-biggest point drop), Kospi −5.21% at 4,869.96, Taiex
  −6.6%, MSCI Asia-Pacific −8% on the week; Brent −$92.22
  intraday quote replaced with the $92.57 settlement. Wall
  Street's Friday close (S&P 500 −3.7%, Nasdaq −5.3%) added to
  the card detail. Numbers band now reads −5.1% / $92.57.
- **Card 5 (APEC):** replaced outright. The ministers' statement
  was Thursday's Outlook in substance; Friday's real APEC news
  was Trump's 88-minute White House briefing defending the
  summit ($17bn in deals, Putin-diplomacy claim). New tag:
  CONFIRMED — AFP. Its map pin was dropped (Washington is
  already pin 6); the map note now reads "5 = WASHINGTON
  (SEE 6)".
- **Latin America:** no mainland main-card candidate survived the
  date check — the Pope's Peru farewell was Monday 16 Nov and
  Paraguay's Peña Senate vote was Friday 6 Nov (both only
  *listed* under 20 Nov). Both are documented in the README's
  rejected list. The gap was closed in the briefs instead: brief
  19 is now Latin oil shares falling on Friday (Petrobras −1.7%,
  YPF −2.9%, Rio Times), replacing the Kirsten Davies brief.
- **Round-2 fix during the final render:** card 3's detail
  truncated mid-phrase ("Nasdaq −5.3% on ...") at two lines; it
  was shortened to fit whole ("Taiex down 6.6%. Wall Street
  follows: S&P 500 −3.7%, Nasdaq −5.3% on Friday.").
- Re-rendered: 1024x768, 181,908 bytes. Checked at full size and
  at 300x225: masthead, date pill and numbers legible at thumbnail
  size; no overlaps, no clipped text anywhere. `main.py` run twice
  from clean output dirs — identical MD5 both times.

Final self-score:
1. Date discipline — strong. Every card and brief is a Friday
   20 Nov event or first report; four near-misses (Pope, Peña,
   Bukele, ministers' statement) were caught and rejected on
   their real dates, not their listing dates.
2. Breadth — strong. War, climate, markets, energy, summit
   politics, tech controls, courts, diplomacy, aid, EU–UK,
   protest, big tech, environment, health, sport; six continents
   including Latin America (brief 19) and Oceania (card 15).
3. Readability — strong. Every headline carries the news; the
   300 px thumbnail still reads.
4. Faithfulness — strong. Closing figures from Reuters wires;
   single-source cards still tagged REPORTED; the $300bn
   climate-finance figure in one COP31 write-up (a COP29
   carry-over) was deliberately not used.
5. Craft — weakest of the five, but no longer failing: the
   Europe/Middle East pin cluster is dense by geography, and
   three icons (cricket bat, scales, missile) are stylised
   rather than literal. Nothing on the page is clipped or
   overlapping.

Status: final edition complete. Not submitted, not pushed, not
built as a GitHub repo — awaiting main-session review.
