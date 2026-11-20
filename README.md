# The World in One Day — Friday 20 November 2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/xiangbingxi/makefun-news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/xiangbingxi/makefun-news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A one-page newspaper front page summing up the world's news of Friday
20 November 2026: **36 stories, 7 regions**, with sources named on the page.
Entry for the make.fun bounty
[`news-image-20261120`](https://make.fun/c/news-image-20261120)
($250 pool, $50 for 1st place).

## The image

- Masthead: `THE WORLD IN ONE DAY`, dated Friday 20 November 2026.
- Lead story: Russian ballistic missiles smash three Kyiv bridges over the
  Dnipro — hand-drawn illustration of the river, the bridges, one broken.
- Three illustrated cards: Cyclone Akvan's landfall in Odisha, Asia's AI
  sell-off (Nikkei −5.1%, Taiwan −6.3%, Kospi −5.2%), and the COP31 final-day
  deadlock in Antalya.
- A "day in numbers" strip (100+ missiles and 400+ drones, 300,000 evacuated,
  −5.1% Nikkei, $81bn Anthropic IPO, $120bn COP31 fund cut, 100,000 UK–EU
  youth visas).
- A numbered index of the remaining 32 stories in four columns, plus a
  sources footer (Reuters, BBC, Ukrainska Pravda, Arab News, CNA, Carbon
  Brief, UN News, Bloomberg, CNBC, NPR, DW, Euronews, Amnesty International,
  FBC, Business Insider, OneTurn, FXStreet, TechCrunch).

Every story was checked against reporting published on 20 November 2026;
the source of each line is recorded in [`NEWS.md`](NEWS.md). Nothing is
invented: casualty and market figures are the figures the cited outlets
reported that day.

## How it is built

`tools/gen_image.py` (Python 3 + Pillow, run once by hand) draws the page
with PIL primitives only — no photos, no downloaded art, no network — and
writes `entry.png` (1024×1024, ~200 KB). The drawing is deterministic: a
fixed seed drives the paper speckle and the hand-drawn wobble, so repeated
runs produce identical bytes.

The entry program itself is `main.ts` (Node 22, standard library only). The
grader runs it with no network; it copies the bundled `entry.png` to
`/output/entry.png` byte for byte and refuses to finish if the file is over
the 1 MiB gate.

## Run it

```sh
# regenerate the image (needs Pillow + Liberation fonts, local use only)
python3 tools/gen_image.py

# run the entry program the way the grader does
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# -> entry.png: 203601 bytes, sha256 <digest>
```

## License

MIT — see [`LICENSE`](LICENSE).

<sub>Entered on [make.fun](https://make.fun/?ref=efzg7wym&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
