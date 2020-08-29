from datetime import datetime, timedelta


class WorkbenchHelper:
    @staticmethod
    def GetDatetimeNowToNearestSecond():
        now = datetime.now()
        now_rounded = now - timedelta(microseconds=now.microsecond)
        return now_rounded
