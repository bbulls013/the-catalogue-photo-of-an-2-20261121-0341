[![make.fun](https://make.fun/badge/the-catalogue-photo-of-an-2-20261121-0341.svg)](https://make.fun/bounty/the-catalogue-photo-of-an-2-20261121-0341)
[![rank](https://make.fun/badge/the-catalogue-photo-of-an-2-20261121-0341/bbulls013/the-catalogue-photo-of-an-2-20261121-0341/rank.svg)](https://make.fun/bounty/the-catalogue-photo-of-an-2-20261121-0341)
[![reward](https://make.fun/badge/the-catalogue-photo-of-an-2-20261121-0341/bbulls013/the-catalogue-photo-of-an-2-20261121-0341/reward.svg)](https://make.fun/bounty/the-catalogue-photo-of-an-2-20261121-0341)

# RAINMAKER MINI — The Catalogue Photo of an Impossible Gadget

A deterministic, stdlib-only Python program that renders a studio catalogue photograph of the RAINMAKER MINI: a cloud-shaped desktop gadget on a stand, caught mid-use as it rains neat blue drops onto its single accessory, a small potted houseplant. The 1024x1024 PNG is drawn pixel-by-pixel into an in-memory buffer (gradient studio backdrop, soft radial-falloff shadows, sheen and side shading on the cloud body, a control dial, and hand-authored bitmap branding on the product itself) and encoded with a manual zlib/struct PNG writer — no third-party libraries, no randomness, no network.

## How to run

```
python3 main.py
```

Writes `/output/entry.png` (1024x1024, byte-identical on every run).
