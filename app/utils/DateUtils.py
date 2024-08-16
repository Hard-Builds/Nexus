from datetime import datetime


class DateUtils:
    @staticmethod
    def get_current_epoch():
        create_current_time = datetime.utcnow()
        current_time_epoch = int(
            (create_current_time - datetime(1970, 1, 1)).total_seconds())
        return current_time_epoch

    @staticmethod
    def get_current_timestamp():
        current_time = datetime.utcnow()
        return current_time
