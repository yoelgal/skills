import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import *  # noqa: E402,F403


class Ch01Problem(Voiced):
    def construct(self):
        self.chapter_title("Ch01Problem")

        names = VGroup(*[pill(n, BLUE, 22) for n in ["Ada", "Ben", "Cleo", "Dev", "Eve", "Finn", "Gus", "Hana"]])
        names.arrange(RIGHT, buff=0.18).move_to(UP * 0.6)
        fit(names, 12.5)

        with self.beat("c1a"):
            self.cue("million")
            self.play(LaggedStart(*[FadeIn(n, shift=DOWN * 0.2) for n in names], lag_ratio=0.08), run_time=1.2)
            self.cue("one")
            target = pill("Gus?", GOLD, 26).next_to(names, UP, buff=0.6)
            self.play(FadeIn(target, shift=DOWN * 0.2), run_time=0.5)

        with self.beat("c1b"):
            self.cue("one")
            for n in names[:7]:
                self.play(Indicate(n, color=GOLD, scale_factor=1.15), run_time=0.22)
            self.cue("half")
            cap = self.caption("~500,000 checks on average", GOLD, 30, y=-1.4)
            self.play(Write(cap), run_time=0.9)
        self.clear()
