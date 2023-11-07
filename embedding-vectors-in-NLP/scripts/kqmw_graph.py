import os
from manim import *
from icecream import ic


class KQMWGraph(Scene):
    def construct(self):
        y_ran = [0, 6, 1]
        ax, ax2 = [
            Axes(
                x_range=x,
                y_range=y_ran,
                axis_config={
                    "include_tip": False,
                    "include_numbers": False,
                    "include_ticks": False,
                    "color": "#bababa",
                },
            )
            for x in ([0, 10, 1], [-5, 5, 1])
        ]

        title = Text("Word relationships").scale(0.65).next_to(ax, UP)
        labels = ax.get_axis_labels(
            x_label="\\text{ gender}", y_label="\\text{ royalty}"
        ).set_color("#bababa")
        labels2 = ax2.get_axis_labels(
            x_label="\\text{ gender}", y_label="\\text{ royalty}"
        ).set_color("#bababa")

        self.play(FadeIn(ax), FadeIn(title), FadeIn(labels))

        name_pos = RIGHT + UP * 0.5
        coords = [
            [2, 2, "#e80000", "man"],
            [1.5, 4.5, "#8a0000", "king"],
            [3.5, 2, "#03d7fc", "woman"],
            [3, 4.5, "#028299", "queen"],
        ]
        points = [
            {
                "p": Dot(point=ax.c2p(x, y), color=c),
                "p2": Dot(point=ax2.c2p(x, y), color=c),
                "label": l,
                "color": c,
            }
            for x, y, c, l in coords
        ]
        for point_pair in points:
            point_pair["l"] = (
                Text(point_pair["label"]).scale(0.4).next_to(point_pair["p"], name_pos)
            )
            point_pair["l2"] = (
                Text(point_pair["label"])
                .scale(0.4)
                .next_to(point_pair["p2"], name_pos + [-0.25, -0.25, 0])
            )
            a = Arrow(
                stroke_width=3,
                max_tip_length_to_length_ratio=0.1,
                color=point_pair["color"],
            )
            point_pair["a"] = a.put_start_and_end_on(
                ax.coords_to_point([0, 0, 0]).T[0], point_pair["p"].get_center()
            )
            a = Arrow(
                stroke_width=3,
                max_tip_length_to_length_ratio=0.1,
                color=point_pair["color"],
            )
            point_pair["a2"] = a.put_start_and_end_on(
                ax2.coords_to_point([0, 0, 0]).T[0], point_pair["p2"].get_center()
            )

        def get_elems(point_list: list[dict], i: int):
            return (
                points[i]["p"],
                points[i]["l"],
                points[i]["a"],
                points[i]["p2"],
                points[i]["l2"],
                points[i]["a2"],
            )

        m, ml, ma, m2, ml2, ma2 = get_elems(points, 0)
        k, kl, ka, k2, kl2, ka2 = get_elems(points, 1)
        w, wl, wa, w2, wl2, wa2 = get_elems(points, 2)
        q, ql, qa, q2, ql2, qa2 = get_elems(points, 3)

        self.play(
            LaggedStart(
                *[Write(elem) for elem in [m, ml, k, kl, w, wl, q, ql]], lag_ratio=0.2
            )
        )
        self.play(
            LaggedStart(*[Write(elem) for elem in [ma, ka, wa, qa]], lag_ratio=0.2)
        )

        dots = VGroup(m, k, w, q)
        dot_labels = VGroup(ml, kl, wl, ql)

        self.play(FadeOut(dots), dot_labels.animate.shift([-0.2, -0.2, 0]))

        # ----- 2 -----
        ic(labels)
        self.play(
            FadeOut(title),
            *[
                Transform(first, second)
                for first, second in [
                    (ax, ax2),
                    (labels, labels2),
                    (ml, ml2),
                    (kl, kl2),
                    (wl, wl2),
                    (ql, ql2),
                    (ma, ma2),
                    (ka, ka2),
                    (wa, wa2),
                    (qa, qa2),
                ]
            ]
        )

        king_minus_man = ax.p2c(k.get_center()) - ax.p2c(m.get_center())
        kmm_dot = Dot(ax.c2p(king_minus_man[0], king_minus_man[1]), color=YELLOW)

        arrow_kmm = Arrow(
            stroke_width=3, max_tip_length_to_length_ratio=0.1, color=YELLOW
        )
        arrow_kmm.put_start_and_end_on(
            ax2.coords_to_point([0, 0, 0]).T[0], kmm_dot.get_center()
        )
        eq_kmm = (
            MathTex("king - man", color=GREEN).next_to(kmm_dot, LEFT * 0.05).scale(0.6)
        )
        self.play(Write(arrow_kmm))
        self.play(Write(eq_kmm))

        dashed_lines = []
        for start, end in [(kmm_dot, k2), (m2, k2), (kmm_dot, q2), (w2, q2)]:
            dashed_line = DashedLine(
                color=GREEN, dash_length=0.075, stroke_width=2, dashed_ratio=0.5
            )
            dashed_line.put_start_and_end_on(start.get_center(), end.get_center())
            dashed_lines.append(dashed_line)

        self.play(*[Write(dashed) for dashed in dashed_lines])

        eq = (
            MathTex("king - man + woman = queen")
            .move_to(LEFT * 3.3 + UP * 2)
            .scale(0.7)
        )
        eq2 = (
            MathTex("(1.5, 4.5) - (2, 2) + (3.5, 2) = (3, 4.5)")
            .next_to(eq, DOWN)
            .scale(0.7)
        )

        eq_group = VGroup(eq, eq2)
        self.play(FadeIn(eq_group[0]), Write(eq_group[1]))
        self.play(Circumscribe(eq_group))
        self.wait(5)
        self.play(*[FadeOut(mob) for mob in self.mobjects])


if __name__ == "__main__":
    os.system(
        r"manim -pql -v WARNING  --disable_caching --format=gif -o kqmw_graph.gif kqmw_graph.py KQMWGraph"
    )
