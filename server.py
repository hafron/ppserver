from bottle import route, run
from ezodf import opendoc
import json
import datetime

def calc_time_to_object(time):
    return datetime.time(int(time[2:4]), int(time[5:7]), int(time[8:10]))

arkusz = "/home/hafron/dev/pomodoro_planner/plan_tygodnia.ods"

ods = opendoc(arkusz)
sheets = ods.sheets
plan = sheets['Plan']
conf = sheets['Konfiguracja']
export_data = {'config': {
			 'pomodoro_length': str(calc_time_to_object(conf['D6'].value)),
			 'short_break_length': str(calc_time_to_object(conf['D7'].value)),
			 'long_break_length': str(calc_time_to_object(conf['D9'].value)),
			 }, 'pomodoros':{}}
week_days = ['pon', 'wt', 'sr', 'czw', 'pt', 'sb', 'nd']


i=2
k=0
last_end_date=''
start_date=''
while i <= 20:
    j=1
    empty_combo=0 # ile pustych elementów pod rząd
    export_data['pomodoros'][week_days[k]] = []
    while empty_combo < 2:
        if plan[j, i].value == None:
            empty_combo+=1
        else:
            start_date = plan[j, i-2].value
            if empty_combo > 0:
                export_data['pomodoros'][week_days[k]].append('#long_break')
                empty_combo=0
            if len(export_data['pomodoros'][week_days[k]]) > 0 and \
               last_end_date != '' and \
               export_data['pomodoros'][week_days[k]][-1] != '#long_break' and \
               start_date != last_end_date:
                export_data['pomodoros'][week_days[k]].append('#short_break')
            export_data['pomodoros'][week_days[k]].append(plan[j, i].value)
            last_end_date = plan[j, i-1].value
        j+=1
    i+=3
    k+=1


@route('/:action')
def index(action):
    if action == 'sync':
       return json.dumps(export_data)

run(host='localhost', port=8080)
