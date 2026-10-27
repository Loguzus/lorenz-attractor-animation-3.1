"""Главный модуль приложения для работы 3.1."""

import tkinter as tk
from src.models.animation_model import LorenzAttractorModel
from src.renderers.renderer import LorenzRenderer
from src.widgets.controls import LorenzControlsPanel


class AnimationApp:
    """Главное окно приложения аттрактора Лоренца."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Работа 3.1 (Вариант 24) — Аттрактор Лоренца")
        self.root.geometry("800x700")
        self.root.configure(bg="#020617")

        self.model = LorenzAttractorModel()
        self.canvas = tk.Canvas(self.root, bg="#020617", highlightthickness=0)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.controls = LorenzControlsPanel(self.root, self.model)
        self.controls.pack(side=tk.BOTTOM, fill=tk.X)

        self.renderer = LorenzRenderer(self.canvas, self.model)

        self.root.bind("<space>", lambda e: setattr(self.model, "is_paused", not self.model.is_paused))
        self.root.bind("<r>", lambda e: self.model.reset())

    def animate(self) -> None:
        for _ in range(3):
            self.model.step()
        self.renderer.render()
        self.root.after(16, self.animate)

    def run(self) -> None:
        self.animate()
        self.root.mainloop()
