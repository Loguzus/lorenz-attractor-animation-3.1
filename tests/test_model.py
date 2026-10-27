import unittest
from src.models.animation_model import LorenzAttractorModel


class TestLorenzModel(unittest.TestCase):
    def test_initial_state(self):
        model = LorenzAttractorModel()
        self.assertEqual((model.x, model.y, model.z), (0.0, 0.0, 0.1))


if __name__ == "__main__":
    unittest.main()
