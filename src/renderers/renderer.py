"""Модуль отрисовки двумерной проекции аттрактора Лоренца."""

import tkinter as tk
from src.models.animation_model import LorenzAttractorModel


class LorenzRenderer:
    """Класс отрисовки траектории и текущей точки аттрактора на Canvas."""

    PALETTE = ("#1e3a8a", "#2563eb", "#06b6d4", "#10b981", "#f59e0b", "#ef4444")

    def __init__(self, canvas: tk.Canvas, model: LorenzAttractorModel) -> None:
        """Инициализирует отрисовщик."""
        self.canvas = canvas
        self.model = model

    def render(self) -> None:
        """Перерисовывает траекторию фазового портрета."""
        self.canvas.delete("all")
        width = int(self.canvas.winfo_width() or 700)
        height = int(self.canvas.winfo_height() or 600)
        cx, cy = width / 2.0, height / 2.0

        self.canvas.create_line(0, cy, width, cy, fill="#1e293b", dash=(4, 4))
        self.canvas.create_line(cx, 0, cx, height, fill="#1e293b", dash=(4, 4))

        trail = self.model.trail
        if len(trail) >= 2:
            chunk_size = max(2, len(trail) // len(self.PALETTE))
            for idx in range(len(self.PALETTE)):
                start = idx * chunk_size
                end = min(len(trail), (idx + 1) * chunk_size + 1)
                segment = trail[start:end]
                if len(segment) >= 2:
                    coords: list[float] = []
                    for pt in segment:
                        sx, sy = self.model.project_point(pt, cx, cy)
                        coords.extend((sx, sy))
                    self.canvas.create_line(*coords, fill=self.PALETTE[idx], width=2, smooth=True)

        hx, hy = self.model.project_point((self.model.x, self.model.y, self.model.z), cx, cy)
        r = 5
        self.canvas.create_oval(hx - r, hy - r, hx + r, hy + r, fill="#ffffff", outline="#ef4444", width=2)
