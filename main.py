#!/usr/bin/env python3
"""RAINMAKER MINI - catalogue photo of an impossible gadget.

Deterministic 1024x1024 PNG rendered with stdlib only.
A cloud-shaped desktop device on a stand rains neat drops onto
one small potted houseplant. Studio backdrop, soft shadows.
"""
import os
import struct
import zlib

W = 1024
H = 1024

# RGB pixel buffer
buf = bytearray(W * H * 3)


def set_px(x, y, r, g, b):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        buf[i] = r
        buf[i + 1] = g
        buf[i + 2] = b


def blend_px(x, y, r, g, b, a):
    """Alpha blend color (r,g,b) with alpha a in [0,1] over buffer."""
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        buf[i] = int(buf[i] * (1 - a) + r * a)
        buf[i + 1] = int(buf[i + 1] * (1 - a) + g * a)
        buf[i + 2] = int(buf[i + 2] * (1 - a) + b * a)


def fill_rect(x0, y0, x1, y1, r, g, b):
    for y in range(max(0, y0), min(H, y1)):
        for x in range(max(0, x0), min(W, x1)):
            set_px(x, y, r, g, b)


def fill_ellipse(cx, cy, rx, ry, r, g, b):
    for y in range(cy - ry, cy + ry + 1):
        if y < 0 or y >= H:
            continue
        dy = (y - cy) / ry if ry else 0
        if abs(dy) > 1:
            continue
        dx = int(rx * (1 - dy * dy) ** 0.5)
        for x in range(cx - dx, cx + dx + 1):
            set_px(x, y, r, g, b)


def blend_ellipse(cx, cy, rx, ry, r, g, b, a):
    for y in range(cy - ry, cy + ry + 1):
        if y < 0 or y >= H:
            continue
        dy = (y - cy) / ry if ry else 0
        if abs(dy) > 1:
            continue
        dx = int(rx * (1 - dy * dy) ** 0.5)
        for x in range(cx - dx, cx + dx + 1):
            blend_px(x, y, r, g, b, a)


def fill_circle(cx, cy, rad, r, g, b):
    fill_ellipse(cx, cy, rad, rad, r, g, b)


def blend_ellipse_soft(cx, cy, rx, ry, r, g, b, a_max):
    """Ellipse with radial alpha falloff - no hard edges."""
    for y in range(cy - ry, cy + ry + 1):
        if y < 0 or y >= H:
            continue
        dy = (y - cy) / ry if ry else 0
        if abs(dy) > 1:
            continue
        dx_max = int(rx * (1 - dy * dy) ** 0.5)
        for x in range(cx - dx_max, cx + dx_max + 1):
            dx = (x - cx) / rx if rx else 0
            d2 = dx * dx + dy * dy
            if d2 < 1:
                blend_px(x, y, r, g, b, a_max * (1 - d2))


# ---- 5x7 bitmap font (only glyphs needed for branding) ----
FONT = {
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["01110", "00100", "00100", "00100", "00100", "00100", "01110"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    " ": ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
}


def draw_text(text, x, y, scale, r, g, b):
    cx = x
    for ch in text:
        glyph = FONT.get(ch, FONT[" "])
        for row_i, row in enumerate(glyph):
            for col_i, bit in enumerate(row):
                if bit == "1":
                    for sy in range(scale):
                        for sx in range(scale):
                            set_px(cx + col_i * scale + sx,
                                   y + row_i * scale + sy, r, g, b)
        cx += 6 * scale


def text_width(text, scale):
    return len(text) * 6 * scale - scale


def draw_drop(cx, cy, r, g, b):
    # teardrop: round body + tapered tip on top
    fill_circle(cx, cy + 4, 7, r, g, b)
    for dy in range(0, 11):
        wdt = max(0, 6 - dy // 2)
        for dx in range(-wdt, wdt + 1):
            set_px(cx + dx, cy - dy, r, g, b)
    # tiny highlight
    set_px(cx - 3, cy + 3, 220, 240, 255)
    set_px(cx - 3, cy + 4, 220, 240, 255)
    set_px(cx - 2, cy + 3, 220, 240, 255)


def render():
    # --- studio backdrop: vertical gradient ---
    for y in range(H):
        t = y / H
        r = int(238 - 26 * t)
        g = int(242 - 24 * t)
        b = int(246 - 18 * t)
        for x in range(W):
            set_px(x, y, r, g, b)
    # floor: slightly darker below floor line
    floor_y = 730
    for y in range(floor_y, H):
        t = (y - floor_y) / (H - floor_y)
        r = int(214 - 18 * t)
        g = int(220 - 18 * t)
        b = int(226 - 16 * t)
        for x in range(W):
            set_px(x, y, r, g, b)
    # floor line highlight
    fill_rect(0, floor_y, W, floor_y + 2, 200, 208, 216)

    # --- soft elliptical shadows (radial falloff, no banding) ---
    blend_ellipse_soft(400, 744, 240, 38, 84, 94, 112, 0.55)
    blend_ellipse_soft(600, 746, 165, 30, 84, 94, 112, 0.55)

    # --- stand: pole + base ---
    fill_rect(392, 430, 408, 712, 120, 130, 145)
    fill_rect(392, 430, 398, 712, 150, 160, 175)  # pole highlight
    fill_ellipse(400, 720, 104, 17, 100, 110, 126)
    fill_ellipse(400, 714, 104, 17, 132, 142, 158)
    fill_ellipse(400, 712, 78, 12, 154, 164, 180)
    fill_ellipse(400, 706, 34, 9, 140, 150, 166)

    # --- cloud device body (union of ellipses) ---
    cloud = (250, 252, 255)
    shade = (205, 218, 232)
    # bottom shade layer slightly lower
    fill_ellipse(512, 372, 230, 78, *shade)
    fill_circle(360, 330, 78, *shade)
    fill_circle(470, 290, 100, *shade)
    fill_circle(600, 300, 92, *shade)
    fill_circle(680, 340, 66, *shade)
    # main white body
    fill_ellipse(512, 360, 230, 78, *cloud)
    fill_circle(360, 318, 78, *cloud)
    fill_circle(470, 278, 100, *cloud)
    fill_circle(600, 288, 92, *cloud)
    fill_circle(680, 328, 66, *cloud)
    fill_rect(282, 318, 742, 362, *cloud)
    # side shading with soft falloff, inside the cloud silhouette
    blend_ellipse_soft(655, 325, 85, 60, 172, 194, 218, 0.45)
    blend_ellipse_soft(512, 398, 200, 32, 172, 194, 218, 0.45)
    # highlight sheen on upper-left of cloud
    blend_ellipse_soft(432, 264, 95, 36, 255, 255, 255, 0.75)
    blend_ellipse_soft(470, 200, 66, 13, 255, 255, 255, 0.8)

    # --- dial on device body ---
    fill_circle(400, 352, 26, 70, 95, 125)
    fill_circle(400, 352, 21, 140, 170, 205)
    fill_circle(400, 352, 7, 60, 80, 110)
    # dial pointer
    for i in range(0, 14):
        set_px(400 + i // 2, 352 - i, 40, 60, 90)
        set_px(401 + i // 2, 352 - i, 40, 60, 90)
    # tick marks
    for tx, ty in [(400, 330), (378, 352), (422, 352), (385, 335), (415, 335)]:
        fill_circle(tx, ty, 2, 70, 95, 125)
    # small indicator light
    fill_circle(640, 350, 8, 90, 200, 140)
    fill_circle(638, 348, 3, 200, 255, 220)

    # --- brand text on product body ---
    label = "RAINMAKER MINI"
    scale = 2
    tw = text_width(label, scale)
    draw_text(label, 512 - tw // 2, 392, scale, 70, 95, 125)

    # --- raindrops: neat columns from cloud toward plant canopy ---
    drop_cols = [516, 554, 592, 630, 664]
    drop_rows = [458, 498, 538]
    for ri, ry in enumerate(drop_rows):
        for ci, rx in enumerate(drop_cols):
            off = 7 if (ri + ci) % 2 == 0 else -7
            draw_drop(rx + off, ry, 66, 142, 226)
    # two drops just above the leaves, mid-fall
    draw_drop(548, 566, 66, 142, 226)
    draw_drop(640, 566, 66, 142, 226)

    # --- potted plant (the single accessory) ---
    pot_cx = 590
    # leaves first (behind pot rim)
    leaf = (52, 150, 78)
    leaf_dark = (36, 118, 58)
    fill_ellipse(pot_cx - 52, 598, 34, 16, *leaf_dark)
    fill_ellipse(pot_cx + 54, 596, 36, 17, *leaf)
    fill_ellipse(pot_cx - 20, 578, 30, 15, *leaf)
    fill_ellipse(pot_cx + 24, 574, 32, 16, *leaf_dark)
    fill_ellipse(pot_cx, 560, 26, 20, *leaf)
    fill_ellipse(pot_cx - 38, 616, 28, 13, *leaf)
    fill_ellipse(pot_cx + 40, 618, 28, 13, *leaf_dark)
    # stems
    fill_rect(pot_cx - 3, 580, pot_cx + 3, 648, 40, 120, 62)
    fill_rect(pot_cx - 34, 600, pot_cx - 28, 648, 40, 120, 62)
    fill_rect(pot_cx + 30, 598, pot_cx + 36, 648, 40, 120, 62)
    # pot body (trapezoid via rows)
    for y in range(650, 732):
        t = (y - 650) / 82
        half = int(72 - 18 * t)
        r = int(196 - 24 * t)
        g = int(104 - 16 * t)
        b = int(64 - 10 * t)
        for x in range(pot_cx - half, pot_cx + half + 1):
            set_px(x, y, r, g, b)
    # pot rim + soil
    fill_rect(pot_cx - 80, 640, pot_cx + 80, 656, 214, 122, 76)
    fill_rect(pot_cx - 80, 640, pot_cx + 80, 646, 228, 140, 92)
    fill_ellipse(pot_cx, 642, 74, 9, 96, 68, 44)
    # wet-soil sheen + tiny splash rings where rain lands
    blend_ellipse(pot_cx, 641, 60, 6, 140, 110, 80, 0.35)
    for sx in (pot_cx - 44, pot_cx - 8, pot_cx + 30, pot_cx + 56):
        fill_circle(sx, 640, 3, 120, 180, 240)
        fill_circle(sx, 640, 1, 200, 230, 255)
    # pot highlight
    for y in range(658, 728):
        t = (y - 658) / 70
        half = int(72 - 18 * ((y - 650) / 82))
        for x in range(pot_cx - half + 8, pot_cx - half + 24):
            blend_px(x, y, 255, 200, 160, 0.25 * (1 - t * 0.5))


def write_png(path):
    raw = bytearray()
    for y in range(H):
        raw.append(0)  # filter type none
        raw.extend(buf[y * W * 3:(y + 1) * W * 3])
    compressed = zlib.compress(bytes(raw), 9)

    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        c += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        return c

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", compressed)
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


def main():
    render()
    os.makedirs("/output", exist_ok=True)
    write_png("/output/entry.png")


if __name__ == "__main__":
    main()
