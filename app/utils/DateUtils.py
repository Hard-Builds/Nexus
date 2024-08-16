from datetime import datetime


class DateUtils:
    @staticmethod
    def get_current_timestamp():
        current_time = datetime.utcnow()
        return current_time
