from datetime import datetime


class DateUtils:
    @staticmethod
    def get_current_epoch():
        date_time = datetime.utcnow() - datetime(1970, 1, 1)
        seconds = date_time.total_seconds()
        current_time = round(seconds * 1000)
        return current_time

    @staticmethod
    def get_current_timestamp():
        current_time = datetime.utcnow()
        return current_time
