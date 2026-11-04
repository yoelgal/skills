"""Shared look, diagram shapes and the narration sync for every chapter scene."""

from __future__ import annotations

import json
import re
import sys
from contextlib import contextmanager
from pathlib import Path

import numpy as np
from manim import *  # noqa: F403

ROOT = Path(__file__).resolve().parent.parent
AUDIO = ROOT / "audio"
sys.path.insert(0, str(ROOT))
from narration import CHAPTERS  # noqa: E402

# Each hue has one meaning for the whole video. Set the meanings in the chapter plan.
BG = "#0E1117"
FG = "#E8E6E3"
DIM = "#7D8590"
FAINT = "#3A404A"
BLUE = "#58C4DD"
TEAL = "#5CD0B3"
GOLD = "#F4C95D"
GREEN = "#83C167"
RED = "#FC6255"
PURPLE = "#B189D6"
ORANGE = "#FF9F5A"
PINK = "#F48FB1"

SANS = "Avenir Next"
MONO = "Menlo"


def T(text: str, size: float = 30, color=FG, weight=NORMAL, **kw) -> Text:
    return Text(text, font=SANS, font_size=size, color=color, weight=weight, **kw)


def M(text: str, size: float = 26, color=FG, **kw) -> Text:
    return Text(text, font=MONO, font_size=size, color=color, **kw)


def fit(mob: Mobject, max_width: float) -> Mobject:
    if mob.width > max_width:
        mob.scale_to_fit_width(max_width)
    return mob


def pill(text: str, color=BLUE, size: float = 24, mono: bool = False, fill_opacity: float = 0.14) -> VGroup:
    label = M(text, size, color) if mono else T(text, size, color)
    box = RoundedRectangle(
        corner_radius=0.16, width=label.width + 0.45, height=label.height + 0.32,
        stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=fill_opacity,
    )
    label.move_to(box)
    return VGroup(box, label)


def node(title: str, sub: str | None = None, color=BLUE, width: float = 2.6, height: float = 1.1,
         size: float = 26) -> VGroup:
    """A component box: a service, a process, an actor."""
    box = RoundedRectangle(
        corner_radius=0.14, width=width, height=height, stroke_color=color, stroke_width=2.5,
        fill_color=color, fill_opacity=0.10,
    )
    t = fit(T(title, size, FG, weight=MEDIUM), width - 0.25)
    if sub:
        s = fit(T(sub, size * 0.62, DIM), width - 0.25)
        VGroup(t, s).arrange(DOWN, buff=0.08).move_to(box)
        return VGroup(box, t, s)
    t.move_to(box)
    return VGroup(box, t)


def cylinder(title: str, color=TEAL, width: float = 2.2, height: float = 1.2, size: float = 24) -> VGroup:
    """A data store."""
    rx, ry = width / 2, 0.16
    body = VGroup(
        Line([-rx, height / 2, 0], [-rx, -height / 2, 0]),
        Line([rx, height / 2, 0], [rx, -height / 2, 0]),
        Arc(radius=1, start_angle=PI, angle=PI).stretch(rx, 0).stretch(ry, 1).shift(DOWN * height / 2),
    ).set_stroke(color, 2.5)
    top = Ellipse(width=width, height=2 * ry).shift(UP * height / 2).set_stroke(color, 2.5)
    fillr = Rectangle(width=width, height=height).set_stroke(width=0).set_fill(color, 0.10)
    t = fit(T(title, size, FG, weight=MEDIUM), width - 0.2).shift(DOWN * 0.08)
    return VGroup(fillr, body, top, t)


def queue_shape(title: str, color=GOLD, width: float = 2.4, height: float = 0.9, size: float = 24) -> VGroup:
    """A queue: a box with slot dividers, title below."""
    box = Rectangle(width=width, height=height).set_stroke(color, 2.5).set_fill(color, 0.08)
    slots = VGroup(*[
        Line(box.get_top() + RIGHT * (x - width / 2), box.get_bottom() + RIGHT * (x - width / 2)).set_stroke(color, 1, 0.35)
        for x in np.linspace(0, width, 7)[1:-1]
    ])
    t = fit(T(title, size, FG, weight=MEDIUM), width - 0.2)
    t.next_to(box, DOWN, buff=0.12)
    return VGroup(box, slots, t)


def arrow(a, b, color=DIM, buff=0.12, sw=3, tip=0.2) -> Arrow:
    return Arrow(a, b, buff=buff, color=color, stroke_width=sw, max_tip_length_to_length_ratio=0.5, tip_length=tip)


def token(color=GOLD, r: float = 0.11) -> VGroup:
    """A thing in motion: a message, a request, a unit of value."""
    halo = Circle(radius=r * 2.0).set_stroke(width=0).set_fill(color, 0.18)
    core = Circle(radius=r).set_stroke(WHITE, 1.2, 0.6).set_fill(color, 1)
    return VGroup(halo, core)


class Bucket(VGroup):
    """A quantity drawn as a vessel with a fill level from -1 to 1. A negative level hangs below the zero line in red."""

    def __init__(self, label: str | Mobject, level: float = 0.0, width: float = 1.3, height: float = 2.2,
                 zero_frac: float = 0.0, color=BLUE, label_size: float = 20, floor: bool = False):
        super().__init__()
        self.w, self.h, self.color = width, height, color
        self.frame = Rectangle(width=width, height=height).set_stroke(color, 2.2)
        self.zero_y_rel = -height / 2 + zero_frac * height
        self.zero_line = Line(LEFT * width / 2, RIGHT * width / 2).shift(UP * self.zero_y_rel)
        self.zero_line.set_stroke(RED if floor else DIM, 4 if floor else 1.5)
        self.level = level
        self.fill = self._fill_for(level)
        lab = label if isinstance(label, Mobject) else T(label, label_size, FG)
        fit(lab, min(max(width * 1.9, lab.width), 3.2))
        lab.next_to(self.frame, DOWN, buff=0.15)
        self.label = lab
        self.add(self.fill, self.frame, self.zero_line, self.label)
        if zero_frac > 0:
            self.add(T("0", 18, DIM).next_to(self.zero_line, LEFT, buff=0.12))

    def _fill_for(self, level: float) -> Rectangle:
        hgt = max(abs(level) * self.h, 0.001)
        c = self.color if level >= 0 else RED
        r = Rectangle(width=self.w - 0.08, height=hgt).set_stroke(width=0).set_fill(c, 0.75 if level >= 0 else 0.6)
        base = self.frame.get_center() + UP * self.zero_y_rel if hasattr(self, "frame") else ORIGIN
        r.move_to(base, aligned_edge=DOWN if level >= 0 else UP)
        return r

    def to_level(self, target: float, run_time: float = 1.0) -> Animation:
        start = self.level

        def upd(m, a):
            self.level = start + (target - start) * a
            m.become(self._fill_for(self.level))

        return UpdateFromAlphaFunc(self.fill, upd, run_time=run_time, rate_func=smooth)


_TIMINGS = json.loads((AUDIO / "timings.json").read_text())
_TITLES = {cls: title for cls, title, _ in CHAPTERS}


def _norm(w: str) -> str:
    return re.sub(r"[^a-z0-9]", "", w.lower())


class Voiced(Scene):
    """A scene whose narration drives its timing.

    with self.beat("c1a"):     # plays c1a.wav from now; at the end, waits out the rest of the beat
        self.cue("bucket")     # waits until the word "bucket" is spoken
        self.play(...)
    """

    PAD = 0.25

    def setup(self):
        self.camera.background_color = BG
        self._beat = None
        self.header = None

    @contextmanager
    def beat(self, key: str, pad: float | None = None):
        info = _TIMINGS[key]
        self.add_sound(str(AUDIO / f"{key}.wav"))
        self._beat = {"key": key, "t0": self.renderer.time, "words": info["words"], "i": 0}
        yield info["duration"]
        elapsed = self.renderer.time - self._beat["t0"]
        rest = info["duration"] + (self.PAD if pad is None else pad) - elapsed
        if rest > 0.02:
            self.wait(rest)
        elif rest < -0.3:
            print(f"[overrun] {key}: visuals ran {-rest:.2f}s past the narration", file=sys.stderr)
        self._beat = None

    def word_time(self, word: str) -> float:
        b = self._beat
        target = _norm(word)
        for j in range(b["i"], len(b["words"])):
            if _norm(b["words"][j][0]).startswith(target):
                b["i"] = j + 1
                return b["t0"] + b["words"][j][1]
        rest = " ".join(w for w, _ in b["words"][b["i"]:])
        raise ValueError(f"cue '{word}' not found in {b['key']} after position {b['i']}: {rest}")

    def cue(self, word: str, lead: float = 0.12):
        dt = self.word_time(word) - lead - self.renderer.time
        if dt > 0.02:
            self.wait(dt)

    def left(self) -> float:
        """Seconds of narration left in the current beat."""
        b = self._beat
        return _TIMINGS[b["key"]]["duration"] - (self.renderer.time - b["t0"])

    def chapter_title(self, cls_name: str, hold: float = 1.0):
        num, _, rest = _TITLES[cls_name].partition(". ")
        n = T(f"Chapter {num}", 28, DIM)
        t = fit(T(rest, 54, FG, weight=MEDIUM), 12.5)
        g = VGroup(n, t).arrange(DOWN, buff=0.3)
        rule = Line(LEFT * 3, RIGHT * 3).set_stroke(BLUE, 2).next_to(g, DOWN, buff=0.35)
        self.play(FadeIn(n, shift=UP * 0.2), Write(t), Create(rule), run_time=1.3)
        self.wait(hold)
        header = T(f"{num} · {rest}", 22, DIM).to_corner(UL, buff=0.4)
        self.play(FadeOut(n), FadeOut(rule), ReplacementTransform(t, header), run_time=0.9)
        self.header = header

    def clear(self, run_time: float = 0.45, keep_header: bool = True):
        mobs = [m for m in self.mobjects if not (keep_header and m is self.header)]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run_time)

    def caption(self, text: str, color=FG, size: float = 30, y: float = -3.25) -> Text:
        return fit(T(text, size, color), 13).move_to([0, y, 0])

    def travel(self, path_points, run_time: float = 1.2, color=GOLD) -> Succession:
        """A token that moves along a polyline, then fades."""
        c = token(color).move_to(path_points[0])
        path = VMobject().set_points_as_corners([np.array(p) for p in path_points])
        return Succession(FadeIn(c, run_time=0.15), MoveAlongPath(c, path, run_time=run_time, rate_func=smooth),
                          FadeOut(c, run_time=0.15))
