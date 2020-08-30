import random as rand
from datetime import datetime, timedelta


class WorkbenchHelper:
    @staticmethod
    def get_datetime_now_to_nearest_sec():
        now = datetime.now()
        return now - timedelta(microseconds=now.microsecond)

    @staticmethod
    def get_float_with_variation(
        mid_point: float = 5, max_variation: float = 0.5, decimal_places: int = 2
    ) -> float:
        variation = rand.random() * max_variation * 2
        return round(mid_point - max_variation + variation, decimal_places)
