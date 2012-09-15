from bottle import route, run
from ezodf import opendoc
import json

arkusz = "/home/hafron/dev/pomodoro_planner/plan_tygodnia.ods"

ods = opendoc(arkusz)
sheets = ods.sheets
plan = sheets['Plan']
conf = sheets['Konfiguracja']
export_data = {'config': {
			 'pomodoro_length': conf['D6'].value,
			 'short_break_length': conf['D7'].value,
			 'long_break_length': conf['D9'].value,
			 }, 'pomodoros':{}}
week_days = ['pon', 'wt', 'sr', 'czw', 'pt', 'sb', 'nd']

i=2
k=0
while i <= 20:
    j=1
    empty_combo=0 # ile pustych elementów pod rząd
    export_data['pomodoros'][week_days[k]] = []
    while empty_combo < 2:
        if plan[j, i].value == None:
            empty_combo+=1
        else:
            if empty_combo > 0:
                export_data['pomodoros'][week_days[k]].append('long_break')
                empty_combo=0
            export_data['pomodoros'][week_days[k]].append(plan[j, i].value)
        j+=1
    i+=3
    k+=1


@route('/:action')
def index(action):
    if action == 'sync':
       return json.dumps(export_data)

run(host='localhost', port=8080)
