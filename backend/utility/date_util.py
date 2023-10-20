from datetime import date
import datetime 

class DateHlper:
    
    def get_todays_string(self):
        today = date.today()
        
        month = '0' + str(today.month) if today.month < 10 else str(today.month)
        day = '0' + str(today.day) if today.day < 10 else str(today.day)
        year = str(today.year-2000)

        return month + '-' + day + '-' + year
    


    