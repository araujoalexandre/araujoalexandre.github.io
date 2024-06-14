from dataclasses import dataclass
from collections import defaultdict
import yaml
from jinja2 import Template
from yaml import Loader
from datetime import datetime, timedelta


@dataclass
class Event:
    category = None
    desc = None
    link = None                                                                                                               
    def __init__(self, event_data):
        for k, v in event_data.items():
            setattr(self, k, v)
        self.date1 = self.date.strftime('%Y-%m-%d')
        self.date2 = self.date.strftime('%b. %d, %Y')
          
 
class Week:
    def __init__(self, id, date, event=None):
        self.id = id
        self.date = date
        self.event = event # we assume only max one event per week 

class LifeInWeeks:
    def __init__(self, start_year, start_month, start_day, events):
        self.start_year = start_year
        weekday = datetime(start_year, start_month, start_day).weekday()
        self.start_date = datetime(start_year, start_month, start_day-weekday)

        week_date = self.start_date
        self.weeks = defaultdict(list)
        # for year in range(self.start_year, self.start_year+101):
        #     week_id = 0
        #     week_date_next_year = datetime(week_date.year+1, week_date.month, week_date.day)
        #     # print(week_date_next_year)
        #     diff_days = timedelta(days=(week_date_next_year - week_date).days)
        #     # print(diff_days)
        #     stop = week_date + diff_days
        #     print(week_date)
        #     while week_date < stop:
        #       week_event = events.get(week_date, None)
        #       week = Week(week_id, week_date, event=week_event)
        #       self.weeks[year].append(week)
        #       week_date = week_date + timedelta(days=7)
        #       week_id += 1
        age = -1
        while True:
            if week_date <= datetime(week_date.year, 9, 22) < week_date + timedelta(days=7):
                week_id = 0
                age += 1
            else:
                week_id = 1
            week_event = events.get(week_date, None)
            week = Week(week_id, week_date, event=week_event)
            self.weeks[age].append(week)
            week_date = week_date + timedelta(days=7)
            if age > 101: break

        # for year in self.weeks.keys():
        #     print(year, len(self.weeks[year]))
        



def main():

    with open('_data/life-in-weeks.yml') as f:
        events_data = next(yaml.load_all(f, Loader=Loader))

    # process events
    events = {}
    for event_date_str, event_data in events_data.items():
        event_date = datetime.fromisoformat(event_date_str)
        event_date_week = event_date - timedelta(days=event_date.weekday())
        event_data['date'] = event_date
        events[event_date_week] = Event(event_data)

    life = LifeInWeeks(1990, 9, 22, events=events)
    with open('./_layouts/life-in-weeks.html') as f:
        template = Template(f.read())
    html = template.render(life=life)
    with open('life-in-weeks.html', 'w') as f:
        f.write(html)

if __name__ =='__main__':
    main()

