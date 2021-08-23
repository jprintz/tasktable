from bottle import route, run, template, static_file
import json

tasksFile = open ('database.json','r')
tasks = json.loads(tasksFile.read())

@route('/')
def index():
    return template('templates/tasktable.tpl', tasks)

@route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./static')

run(host='0.0.0.0', port=8080, debug='true', reloader='true')