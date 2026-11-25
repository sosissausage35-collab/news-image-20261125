# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/sosissausage35-collab/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/sosissausage35-collab/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

One image that sums up the world's news of **Wednesday 25 November 2026** — a newspaper front page with 35 stories across 6 regions, drawn entirely in code.

Lead stories: the CIA and the US Director of National Intelligence hit by a cyberattack (CNN); Huawei found guilty of stealing trade secrets on 10 of 12 counts by a New York jury; a Houthi strike hits a tower in Riyadh's financial district, injuring 11, as Iran says three more tankers struck mines in the Strait of Hormuz. Also inside: Ukraine sinks a Russian warship off Libya, leaked data put Russian soldiers killed past 700,000, the WHO evacuates its Ebola staff in DR Congo, Dell's AI-server earnings beat, Nvidia's slide as the AI rally cools, the Dow closing above 50,000 for the first time, Trump awarding Rudy Giuliani the Medal of Freedom, and 22 more stories — every one reported on 24–25 November 2026 (wires read up to 01:30 UTC, 25 Nov).

`draw.py` draws the page with Pillow (masthead, stat strip, region tabs, 3 illustrated lead stories, 10 more stories, a world map with numbered pins, and a date-check box). `main.ts` copies the shipped `entry.png` to the output directory, deterministically and with no network.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=f4pc3mbd&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
