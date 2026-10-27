"""Панель управления со слайдерами параметров аттрактора Лоренца."""

import tkinter as tk
from typing import Callable
from src.models.animation_model import LorenzAttractorModel


class LorenzControlsPanel(tk.Frame):
    """Виджет панели управления параметрами sigma, r, b и проекциями."""

    def __init__(self, parent: tk.Widget, model: LorenzAttractorModel) -> None:
        """Создает слайдеры."""
        super().__init__(parent, bg="#0f172a", padx=12, pady=8)
        self.model = model

        self.sigma_scale = self._create_slider("Параметр σ:", 1.0, 30.0, self.model.sigma, self._on_change)
        self.r_scale = self._create_slider("Параметр r:", 0.5, 60.0, self.model.r, self._on_change)
        self.b_scale = self._create_slider("Параметр b:", 0.2, 10.0, self.model.b, self._on_change)

        btn_frame = tk.Frame(self, bg="#0f172a")
        btn_frame.pack(side=tk.TOP, fill=tk.X, pady=(6, 0))

        self._add_btn(btn_frame, "Пауза (Space)", lambda: setattr(self.model, "is_paused", not self.model.is_paused))
        self._add_btn(btn_frame, "Сброс (R)", self.model.reset)
        self._add_btn(btn_frame, "Сменить проекцию", self._switch_proj)

    def _create_slider(self, label: str, mn: float, mx: float, val: float, cmd: Callable) -> tk.Scale:
        row = tk.Frame(self, bg="#0f172a")
        row.pack(fill=tk.X, pady=2)
        tk.Label(row, text=label, fg="#cbd5e1", bg="#0f172a", width=12, anchor="w").pack(side=tk.LEFT)
        scale = tk.Scale(row, from_=mn, to=mx, resolution=0.1, orient=tk.HORIZONTAL, bg="#0f172a", fg="#fff", command=cmd)
        scale.set(val)
        scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        return scale

    def _add_btn(self, parent: tk.Widget, text: str, cmd: Callable) -> None:
        tk.Button(parent, text=text, command=cmd, bg="#1e293b", fg="#fff", relief=tk.FLAT, padx=8, pady=4).pack(side=tk.LEFT, padx=4)

    def _on_change(self, _v: str) -> None:
        self.model.sigma = float(self.sigma_scale.get())
        self.model.r = float(self.r_scale.get())
        self.model.b = float(self.b_scale.get())

    def _switch_proj(self) -> None:
        order = {"XZ": "XY", "XY": "YZ", "YZ": "XZ"}
        self.model.projection = order[self.model.projection]
