import os
from manim import *
from icecream import ic
import pandas as pd
import ast


df = pd.read_csv("./data/data_80_embeddings_PCA.csv")
# ic(df.head(1))


def load_data(path: str = "./data/data_80_embeddings_PCA.csv") -> pd.Series:
    df = pd.read_csv(path)
    return df["PCA_2D"].apply(lambda x: ast.literal_eval(x))


def generate_dots(ax: Axes, dots: pd.Series):
    finance = [
        Dot(point=ax.c2p(x, y), color="#b00412", fill_opacity=0.5).set_stroke(
            color="#b00412", width=1
        )
        for x, y in dots.values[:20]
    ]
    animal = [
        Dot(point=ax.c2p(x, y), color="#e85a02", fill_opacity=0.5).set_stroke(
            color="#e85a02", width=1
        )
        for x, y in dots.values[20:40]
    ]
    sport = [
        Dot(point=ax.c2p(x, y), color="#00947b", fill_opacity=0.5).set_stroke(
            color="#00947b", width=1
        )
        for x, y in dots.values[40:60]
    ]
    food = [
        Dot(point=ax.c2p(x, y), color="#00a6ff", fill_opacity=0.5).set_stroke(
            color="#00a6ff", width=1
        )
        for x, y in dots.values[60:]
    ]
    return VGroup(*finance), VGroup(*animal), VGroup(*sport), VGroup(*food)


class Embeddings2D(Scene):
    def construct(self):
        ax = Axes(
            x_range=[-0.2, 0.4, 0.1],
            y_range=[-0.3, 0.4, 0.1],
            axis_config={
                "include_tip": False,
                "include_numbers": True,
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
        )
        self.add(ax, x_label, y_label)  # title

        finance, animal, sport, food = generate_dots(ax, load_data())
        self.add(finance, animal, sport, food)

        financeL = (
            MathTex("finance")  # , color="#ff2f1c"
            .next_to(finance.get_center(), UP * 2)
            .scale(0.6)
        )
        animalL = (
            MathTex("animal")  # , color="#ff9d00"
            .next_to(animal.get_center(), DOWN * 2.5 + LEFT * 1.5)
            .scale(0.6)
        )
        sportL = (
            MathTex("sport")  # , color="#00ffbb"
            .next_to(sport.get_center(), DOWN * 2.5 + LEFT * 1.5)
            .scale(0.6)
        )
        foodL = (
            MathTex("food")  # , color="#00d0ff"
            .next_to(food.get_center(), UP * 2.5)
            .scale(0.6)
        )
        self.add(financeL, animalL, sportL, foodL)

        # self.wait(5)


if __name__ == "__main__":
    os.system(
        r"manim -pql -v WARNING  --disable_caching --format=png -o Embeddings2D.png embeddings_2D.py Embeddings2D"
    )
