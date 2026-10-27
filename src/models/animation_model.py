"""Модель данных для расчета траектории аттрактора Лоренца."""

from typing import List, Tuple


class LorenzAttractorModel:
    """Математическая модель системы дифференциальных уравнений Лоренца."""

    def __init__(
        self,
        sigma: float = 10.0,
        r: float = 28.0,
        b: float = 8.0 / 3.0,
        dt: float = 0.008,
        max_points: int = 1800,
    ) -> None:
        """Инициализирует начальное состояние (1; 1; 5) и параметры системы."""
        self.sigma = sigma
        self.r = r
        self.b = b
        self.dt = dt
        self.max_points = max_points

        self.x = 1.0
        self.y = 1.0
        self.z = 5.0
        self.is_paused = False
        self.projection = "XZ"  # Доступные проекции: "XZ", "XY", "YZ"
        self.trail: List[Tuple[float, float, float]] = [(self.x, self.y, self.z)]

    def step(self) -> None:
        """Выполняет один шаг интегрирования методом Рунге-Кутты 4-го порядка."""
        if self.is_paused:
            return

        def derivatives(x: float, y: float, z: float) -> Tuple[float, float, float]:
            dx = self.sigma * (y - x)
            dy = x * (self.r - z) - y
            dz = x * y - self.b * z
            return dx, dy, dz

        dt = self.dt
        k1x, k1y, k1z = derivatives(self.x, self.y, self.z)
        k2x, k2y, k2z = derivatives(
            self.x + 0.5 * dt * k1x, self.y + 0.5 * dt * k1y, self.z + 0.5 * dt * k1z
        )
        k3x, k3y, k3z = derivatives(
            self.x + 0.5 * dt * k2x, self.y + 0.5 * dt * k2y, self.z + 0.5 * dt * k2z
        )
        k4x, k4y, k4z = derivatives(
            self.x + dt * k3x, self.y + dt * k3y, self.z + dt * k3z
        )

        self.x += (dt / 6.0) * (k1x + 2 * k2x + 2 * k3x + k4x)
        self.y += (dt / 6.0) * (k1y + 2 * k2y + 2 * k3y + k4y)
        self.z += (dt / 6.0) * (k1z + 2 * k2z + 2 * k3z + k4z)

        self.trail.append((self.x, self.y, self.z))
        if len(self.trail) > self.max_points:
            self.trail.pop(0)

    def project_point(
        self, point: Tuple[float, float, float], center_x: float, center_y: float, scale: float = 9.5
    ) -> Tuple[float, float]:
        """Преобразует 3D-координаты в 2D-экранные."""
        x, y, z = point
        if self.projection == "XY":
            return center_x + x * scale, center_y - y * scale
        if self.projection == "YZ":
            return center_x + y * scale, center_y - (z - 25.0) * scale
        return center_x + x * scale, center_y - (z - 25.0) * scale

    def reset(self) -> None:
        """Сбрасывает траекторию в начальную точку."""
        self.x, self.y, self.z = 1.0, 1.0, 5.0
        self.trail = [(self.x, self.y, self.z)]

    def set_preset(self, sigma: float, r: float, b: float) -> None:
        """Устанавливает параметры."""
        self.sigma = sigma
        self.r = r
        self.b = b
        self.reset()
