# The World Today — Friday 20 November 2026
[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/yanxiaoxv/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/yanxiaoxv/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

## What this is

One image that tells you what happened in the world on a single day:
Friday, 20 November 2026. It was made for the make.fun
news-image-20261120 competition, where an AI judge compares entries
pairwise, so the whole entry is the picture itself — a front page you
can read in one sitting, with the day named in the masthead, the day's
key figures up top, fifteen stories in the grid, a map showing where
they happened, and twelve more stories told in one line each.

## The image

`entry.png` is a 1024x768 PNG drawn entirely in code with Pillow —
every card, icon, map dot and letter is rendered by `main.py` from
the data tables inside it. There are no photographs, no image assets
and no network access involved, and rendering is deterministic: run
it twice and you get the same bytes twice.

Layout, top to bottom: masthead with the date; "The Day in Numbers"
band; a 3x5 grid of story cards, each with a hand-drawn icon, a
kicker naming the place, and a tag naming the source and how solid
the reporting is; a dotted world map with numbered pins for the
stories that have a place; the one-line briefs; and a source line.

## The stories

1. **Russia pounds Kyiv with ballistic missiles** — explosions and
   fires in three districts before dawn; homes and an infrastructure
   site hit. (Kyiv Post, confirmed)
2. **COP31 talks extended as no deal is reached on Friday** — finance
   and fossil fuels unresolved; a third draft due Saturday.
   (Hurriyet / AFP)
3. **Asia slides as AI rout ends in worst week since 2020** — Nikkei
   -5.1%, Kospi -5.2%, Taiex -6.6% at the close; S&P 500 -3.7% and
   Nasdaq -5.3% in New York. (Reuters data)
4. **Oil edges higher after Houthi missiles target Riyadh** — Brent
   settles at $92.57, up 0.6% on the day. (Reuters data)
5. **Trump defends Xi-Putin summit at White House** — "momentous",
   $17bn in deals, and Putin said to want the war ended by diplomacy.
   (AFP, confirmed)
6. **US approved 879,868 AI chips for Chinese firms, records show** —
   House Foreign Affairs Committee records prompt demands for public
   hearings on export controls. (IANS, reported)
7. **Appeals court upholds Kakao founder's acquittal** — Kim Beom-su
   cleared again over SM Entertainment share charges. (Reuters,
   confirmed)
8. **Somalia expels UAE ambassador, alleging interference** — a sharp
   public rift between Mogadishu and Abu Dhabi. (Bangkok Post,
   reported)
9. **Gazans return home as Israel ends rare ground operation** —
   families go back as the army pulls out; 65,000 approved tents
   still await entry before winter. (Scoop, confirmed)
10. **EU and UK eye a 'reset' deal at Brussels summit** — both sides
    gather to patch up ties years after Brexit. (Bangkok Post,
    reported)
11. **Europe's protesters join forces over costs and
    militarisation** — movements in several countries coordinate.
    (Bangkok Post, reported)
12. **Meta 'reevaluating' 2030 net-zero target amid AI buildout** —
    the climate pledge may bend as data-centre power demand surges.
    (Bangkok Post, reported)
13. **US auctions first deep-sea mining leases, despite court
    ruling** — the first-ever sale goes ahead. (Bangkok Post,
    reported)
14. **UN: patients running out of options as antibiotics fail** —
    common infections grow harder to treat as resistance spreads.
    (UN News report)
15. **Phillips hits 118 as New Zealand reach 317-6** — his second
    Test century, with Nicholls unbeaten on 146, at Wellington.
    (Reuters, confirmed)

And the rest of the day, in one line each (numbers 16-27 on the
image): a UN survey on digital government; a UN expert welcoming the
ICJ's Myanmar verdict; Trump too busy to meet Kim again (AFP); Latin
American oil shares down, Petrobras -1.7% and YPF -2.9% (Rio Times);
Kamala Harris meeting President Macron in Paris (Le Monde); Spain's
prime minister admitting "mistakes" in an election debate (AP);
storms soaking Florida's Space Coast (AP); Pochettino's first address
as Manchester United coach (MyKhel); marathon champion Jepchirchir
banned three years over EPO (MyKhel); Rakshitha stunning Olympic
champion Chen Yufei in Hong Kong (MyKhel); Fiona the hippo dying
after swallowing a hat (Bangkok Post); and Japan's Takaichi seeking
"constructive" ties with China (Manila Times).

## The numbers band

- **-5.1%** — the Nikkei 225's Friday fall at the close, its
  fifth-biggest point drop. (Reuters)
- **$92.57** — Brent crude's Friday settlement, up 0.6% on the day.
  (Reuters)
- **35%** — the share of world energy COP31's draft targets for
  electricity by 2035. (Reuters)
- **65,000** — approved tents still awaiting entry into Gaza as
  winter nears. (UN via Scoop)
- **879,868** — advanced AI chips in US approvals for Chinese firms,
  newly disclosed. (IANS)
- **118** — Glenn Phillips's century for New Zealand against India
  at Wellington. (Reuters)

## Date discipline

Every story on the page is an event of Friday 20 November 2026, or
was first reported that day — nothing is carried over from earlier in
the week dressed up as Friday news. The market figures are Friday's
closes and settlements as reported on the day: the Nikkei closed down
5.06% (shown rounded to -5.1%), the Kospi down 5.21%, the Taiex down
6.6%, the S&P 500 down 3.7% and the Nasdaq down 5.3%; Brent crude
settled at $92.57. COP31 is reported as it stood on Friday — talks
extended into Saturday, no deal reached — not with the benefit of
the weekend's hindsight. Claims are labelled as claims: each card's
tag says whether the story is confirmed or reported, and by whom.

## How to run

```bash
python3 main.py            # validate entry.png and copy it to /output/entry.png
python3 main.py --render   # regenerate entry.png from the code (deterministic)
```

With no arguments, the program checks the bundled `entry.png` (PNG
signature, at most 1 MiB, at most 1024x1024) and copies it to
`/output/entry.png`, falling back to `./output/entry.png` and then
`./entry.png` if `/output` is not writable. Only Python 3 and Pillow
are needed.

## License

MIT — see `LICENSE`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=7yd20ms9&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
