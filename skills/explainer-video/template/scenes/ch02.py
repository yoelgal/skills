import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import *  # noqa: E402,F403


class Ch02Buckets(Voiced):
    def construct(self):
        self.chapter_title("Ch02Buckets")

        buckets = VGroup(*[node(str(i), None, TEAL, width=1.3, height=1.0) for i in range(6)])
        buckets.arrange(RIGHT, buff=0.3).move_to(DOWN * 1.2)
        fn = node("hash( )", None, PURPLE, width=2.2, height=0.9).move_to(UP * 1.4)

        with self.beat("c2a"):
            self.cue("buckets")
            self.play(LaggedStart(*[FadeIn(b) for b in buckets], lag_ratio=0.1), run_time=0.9)
            self.cue("function")
            self.play(FadeIn(fn, shift=DOWN * 0.2), run_time=0.6)
            self.cue("number")
            name = pill("Gus", BLUE, 24).next_to(fn, LEFT, buff=1.2)
            self.play(FadeIn(name), run_time=0.3)
            self.play(name.animate.move_to(fn), run_time=0.4)
            self.play(FadeOut(name), Indicate(buckets[4], color=GOLD), run_time=min(0.6, max(self.left(), 0.3)))

        with self.beat("c2b"):
            self.cue("hash")
            self.play(self.travel([fn.get_bottom(), buckets[4].get_top()], 0.8), run_time=0.8)
            self.cue("few")
            inside = VGroup(pill("Gus", BLUE, 18), pill("Ivy", BLUE, 18)).arrange(DOWN, buff=0.1)
            inside.next_to(buckets[4], DOWN, buff=0.2)
            self.play(FadeIn(inside, shift=UP * 0.1), run_time=0.5)
            cap = self.caption("one hash, then a few checks", GREEN, 30)
            self.play(Write(cap), run_time=0.9)
        self.clear()
