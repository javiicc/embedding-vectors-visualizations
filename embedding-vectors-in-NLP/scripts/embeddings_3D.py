import os
from manim import *
from icecream import ic
import pandas as pd
import ast


df = pd.read_csv("./data/data_80_embeddings_PCA.csv")
# ic(df.head(1))


def load_data(path: str = "./data/data_80_embeddings_PCA.csv") -> pd.Series:
    df = pd.read_csv(path)
    return df["PCA_3D"].apply(lambda x: ast.literal_eval(x))


def generate_dots(ax: Axes, dots: pd.Series):
    finance = [
        Dot3D(point=ax.c2p(x, y, z), color="#b00412", fill_opacity=0.5)
        for x, y, z in dots.values[:20]  # [:3]  # [:20]
    ]
    animal = [
        Dot3D(point=ax.c2p(x, y, z), color="#e85a02", fill_opacity=0.5)
        for x, y, z in dots.values[20:40]  # [20:23]  # [20:40]
    ]
    sport = [
        Dot3D(point=ax.c2p(x, y, z), color="#00947b", fill_opacity=0.5)
        for x, y, z in dots.values[40:60]  # [40:43]  # [40:60]
    ]
    food = [
        Dot3D(point=ax.c2p(x, y, z), color="#00a6ff", fill_opacity=0.5)
        for x, y, z in dots.values[60:]  # [60:63]  # [60:]
    ]
    return VGroup(*finance), VGroup(*animal), VGroup(*sport), VGroup(*food)


class Embeddings3D(ThreeDScene):
    def construct(self):
        ax = ThreeDAxes(
            x_range=[-0.4, 0.4, 0.1],
            y_range=[-0.4, 0.4, 0.1],
            z_range=[-0.4, 0.4, 0.1],
            axis_config={
                "include_tip": False,
                "include_numbers": False,
                "include_ticks": True,
                "color": "#bababa",
                "font_size": 25,
                "tick_size": 0.05,
            },
        )

        title = Text("Embedding clusters → 2 dimensions").scale(0.65)
        title.next_to(ax, UP)

        x_label = (
            ax.get_x_axis_label("\\text{ 1st dim}").set_color("#bababa").scale(0.7)
        )
        y_label = (
            ax.get_y_axis_label("\\text{ 2nd dim}").set_color("#bababa").scale(0.7)
        ).rotate(-PI / 2, axis=[0.0, 0.0, 1.0])
        z_label = (
            ax.get_z_axis_label("\\text{ 3rd dim}").set_color("#bababa").scale(0.7)
        )
        self.add(ax, x_label, y_label, z_label)  # title

        finance, animal, sport, food = generate_dots(ax, load_data())

        self.play(
            LaggedStart(
                *[Write(p) for p in [finance + animal + sport + food]], lag_ratio=0.05
            )
        )

        financeL = (
            MathTex("finance")  # , color="#ff2f1c"
            .next_to(finance.get_center(), UP * 2.5)
            .scale(0.6)
        )
        animalL = (
            MathTex("animal")  # , color="#ff9d00"
            .next_to(animal.get_center(), DOWN * 2.5 + LEFT * 1.5)
            .scale(0.6)
        )
        sportL = (
            MathTex("sport")  # , color="#00ffbb"
            .next_to(sport.get_center(), DOWN * 2.5 + LEFT * 2)
            .scale(0.6)
        )
        foodL = (
            MathTex("food")  # , color="#00d0ff"
            .next_to(food.get_center(), UP * 3)
            .scale(0.6)
        )
        self.play(Write(financeL), Write(animalL), Write(sportL), Write(foodL))

        # animate the move of the camera to properly see the axes
        self.move_camera(phi=75 * DEGREES, theta=1 * DEGREES, zoom=1, run_time=1.5)
        # built-in updater which begins camera rotation
        self.begin_ambient_camera_rotation(rate=0.25)
        # self.play(FadeIn(z_label))
        self.play(
            x_label.animate.rotate(PI / 2, axis=[1.0, 0.0, 0.0]).rotate(
                PI, axis=[0.0, 0.0, 1.0]
            ),
            y_label.animate.rotate(PI / 2, axis=[1.0, 0.0, 0.0]).rotate(
                PI / 2, axis=[0.0, 0.0, 1.0]
            ),
            z_label.animate.rotate(PI, axis=[0.0, 0.0, 1.0]),
            financeL.animate.rotate(PI / 2, axis=[1.0, 0.0, 0.0]).rotate(
                PI, axis=[0.0, 0.0, 1.0]
            ),
            foodL.animate.rotate(PI / 2, axis=[1.0, 0.0, 0.0]).rotate(
                PI, axis=[0.0, 0.0, 1.0]
            ),
            sportL.animate.rotate(PI / 2, axis=[1.0, 0.0, 0.0]).rotate(
                PI, axis=[0.0, 0.0, 1.0]
            ),
            animalL.animate.rotate(PI / 2, axis=[1.0, 0.0, 0.0]).rotate(
                PI, axis=[0.0, 0.0, 1.0]
            ),
        )
        self.wait(4)
        self.play(y_label.animate.rotate(PI, axis=[0.0, 0.0, 1.0]))
        self.wait(6)


if __name__ == "__main__":
    os.system(
        r"manim -pql -v WARNING  --disable_caching --format=mp4 -o Embeddings3D.mp4 embeddings_3D.py Embeddings3D"
    )
