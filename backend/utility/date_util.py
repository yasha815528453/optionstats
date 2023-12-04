from datetime import date
import datetime

class DateHelper:

    @property
    def today(self):
        return date.today()

    def get_todays_string(self):
        today = self.today

        month = '0' + str(today.month) if today.month < 10 else str(today.month)
        day = '0' + str(today.day) if today.day < 10 else str(today.day)
        year = str(today.year-2000)

        return year + '-' + month + '-' + day

    def get_datetime_delta(self, deltadays):
        return self.today - datetime.timedelta(days=deltadays)


    def get_timestamp(self):
        dt = datetime.datetime.now()
        return str(dt.year)+'-'+str(dt.month)+'-'+str(dt.day)+' '+str(dt.hour)+':'+str(dt.minute)
