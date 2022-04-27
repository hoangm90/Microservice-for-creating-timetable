import datetime
from typing import Optional

def is_holiday(day: datetime.date):
    # return true if the given day falls into a holiday
    holiday_set = {"23-12", "24-12", "25-12", "26-12", "27-12", "28-12", "29-12", "30-12", "31-12", "1-1",
                    "1-5", "8-5", "5-7", "6-7", "28-9", "28-10", "17-11"}
    day_month = day.strftime("%d") + "-" + day.strftime("%m")
    return (day_month in holiday_set)

def color_to_time(num_color: int, start_date: Optional[dict] = None):
    # from the color, determine the timeslot
    hours = [
        [{"hours": 8, "minutes": 0}, {"hours": 9, "minutes": 30}], 
        [{"hours": 9, "minutes": 50}, {"hours": 11, "minutes": 20}],
        [{"hours": 11, "minutes": 40}, {"hours": 13, "minutes": 10}],
        [{"hours": 14, "minutes": 30}, {"hours": 16, "minutes": 0}],
        [{"hours": 16, "minutes": 20}, {"hours": 17, "minutes": 50}],
    ]

    color_time = []
    # set start date according to the input data, if the start date is not included, set it as October 1, 2021
    if start_date:
        day = datetime.date(start_date["year"], start_date["month"], start_date["day"])
    else:
        day = datetime.date(2021, 10, 1)   
    day -= datetime.timedelta(days = 1)

    for i in range(num_color):
        if i%5 == 0:
            # i%5 = 0 indicates that this timeslot is the first timeslot of the next day
            day += datetime.timedelta(days = 1)

            while day.strftime("%w") == '0' or day.strftime("%w") == '6' or is_holiday(day):
                # increase the day to avoid holiday and weekend
                day += datetime.timedelta(days = 1)
        
        start_time = hours[i%5][0]
        end_time = hours[i%5][1]
        date = {"day": int(day.day), "month": int(day.month), "year": int(day.year)}
        date_code = str(day)
        time_slot = {
            "startTime": start_time,
            "endTime": end_time,
            "dateCode": date_code,
            "date": date,
        }
        
        color_time.append(time_slot)
    return color_time

