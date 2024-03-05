from flask import Flask, render_template, request, jsonify
import json
import time
import sys
from configparser import ConfigParser
import os
from datetime import datetime,timedelta
import random
from random import randint
from threading import Thread
import logging
import subprocess


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


config = ConfigParser()

host = ''
app = Flask(__name__)

def init_settings():
    
    config.add_section('main')
    config.set('main','start_output_on_device_start','false')
    config.set('main', 'upcs_to_select_settings', '0')
    config.set('main', 'random_scans_per_day_settings', '{"min":"1","max":"10"}')
    config.set('main', 'random_interval_settings', '{"min":"1","max":"9999"}')
    config.set('main','items','')
    config.set('main','last_run_time','')
    config.set('main','next_run_time','')

    with open('config.ini', 'w') as f:
        config.write(f)
    
    config.read('config.ini') 
    return()

    
args = [x.upper() for x in sys.argv]
print(args)

try:
    for arg in args:
        if "--HOST" in arg:
            index = args.index("--HOST")
            host = args[index+1]
except:
    pass

NULL_CHAR = chr(0)

def write_to_log(log):
    if log:
        log = f'{datetime.now()} {log}\n'
    with open('log.log', 'a') as f:
        f.write(log)

# Define the function to send the HID report
def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

def save_items(items):
    while("" in items):
        items.remove("")
    config.set('main','items',",".join(items))
    with open('config.ini', 'w') as f:
        config.write(f)

def load_items():
    global items
    items = config.get('main','items').split(',')
    while("" in items):
        items.remove("")
    return items

def update_log():
    try:
        with open('log.log', 'r') as log_file:
            logs = log_file.read()
    except:
        write_to_log('')
        logs = ''
    return(logs)

def run():
    print('task run')

def update():
    config.read('config.ini')
    try:
        last_run = config.get('main','last_run_time')
        next_run = config.get('main','next_run_time')
    except:
        init_settings()
    last_run = config.get('main','last_run_time')
    next_run = config.get('main','next_run_time')
    if not last_run:
        last_run = datetime.now()
      
    if not next_run or datetime.strptime(next_run, '%Y-%m-%d %H:%M:%S.%f') < datetime.now():
        run()
        interval = json.loads(config.get('main', 'random_interval_settings'))
        interval['min'] = int(interval['min'])
        interval['max'] = int(interval['max'])
        interval = random.randint(interval['min'],interval['max'])
        
        next_run_time = datetime.now() + timedelta(seconds=interval)
        print(f'Next run at {next_run_time}')
        config.set('main','last_run_time',str(datetime.now()))
        config.set('main','next_run_time',next_run_time.strftime('%Y-%m-%d %H:%M:%S.%f'))
        with open('config.ini', 'w') as f:
            config.write(f)
        write_to_log(f'Task ran. Next runtime {next_run_time}')
    
def task_daemon():
    global is_running
    try:    
        config.read('config.ini')  
    except:
        init_settings()

    if config.get('main','start_output_on_device_start') == 'true':
       
        is_running = 1
    else:
       
        is_running = 0
    
    while 1:
        if is_running == 1:
            update()
        #print('ran')
        time.sleep(1)

@app.route('/update_script')        
def update_script():
    write_to_log("updating system.....")
    subprocess.call(['sh', '/usr/bin/scanner_pi/update.sh'])
    return jsonify({'message': 200})
            
@app.route('/')
def index():
    global logs
    
    logs = update_log()
    
    start_output,upcs_to_select_min, random_scans_per_day_min, random_scans_per_day_max, random_interval_min, random_interval_max = load_settings()
    return render_template('index.html', is_running=is_running,items=load_items(),logs=logs,start_output=start_output,upcs_to_select_min=upcs_to_select_min, random_scans_per_day_min=random_scans_per_day_min, random_scans_per_day_max=random_scans_per_day_max, random_interval_min=random_interval_min, random_interval_max=random_interval_max)

@app.route('/toggle_running', methods=['POST'])
def toggle_running():
    global is_running
    is_running = 1 - is_running  # Toggle the value between 0 and 1
    if is_running:
        write_to_log('Started output')
    else:
        write_to_log('Stopped Output')
    
    return jsonify({'is_running': is_running})

@app.route('/get_logs')
def get_logs():
    with open('log.log', 'r') as log_file:
        logs = log_file.read()
    return jsonify({'logs': logs})

@app.route('/clear_config',methods=['POST'])
def clear_config():
    global config
    

    #config = ConfigParser()
    config.clear()
    with open('config.ini', 'w') as f:
            config.write(f)
    init_settings()
    write_to_log('reset config')
    
    
    return jsonify({'message': 200})

@app.route('/clear_log',methods=['POST'])
def clear_log():
    
    try:
        os.remove('log.log')
    except:
        pass
    
    write_to_log('')  
    
    return jsonify({'message': 200})

# Define the route to handle the HID report generation
@app.route('/generate_hid_report', methods=['POST'])
def generate_hid_report():
    string = request.form['input_string']
    print('waiting 3 seconds...')
    time.sleep(3)
    print(string)
    for x in [*string]:
        if int(x) == 0:
            write_report(NULL_CHAR*2+chr(39)+NULL_CHAR*5)
            write_report(NULL_CHAR*8)
        else:
            x = 29+int(x)
            write_report(NULL_CHAR*2+chr(x)+NULL_CHAR*5)
            write_report(NULL_CHAR*8)

    write_report(NULL_CHAR*2+chr(40)+NULL_CHAR*5)
    write_report(NULL_CHAR*8)
    return jsonify({'message': 200})

@app.route('/add_item', methods=['POST'])
def add_item():
    write_to_log('add_item')
    items = load_items()
    items_to_add = request.form['items'].split(',')
    print(items_to_add)
    items.extend(items_to_add)
    save_items(items)
    return jsonify({'message': 'Items added successfully'})

@app.route('/remove_selected_items', methods=['POST'])
def remove_selected_items():
    global items
    indexes = list(map(int, json.loads(request.form['indexes'])))
    indexes.sort(reverse=True)  # Remove items in reverse order to avoid index issues
    for index in indexes:
        del items[index]
    save_items(items)
    return jsonify({'message': 'Items removed successfully'})

@app.route('/save_settings', methods=['POST'])
def save_settings():
    start_output = request.form['start_output']
    print(start_output)
    
    print(type(start_output))
    upcs_to_select_min = str(request.form['upcs_to_select_min'])
    random_scans_per_day_min = str(request.form['random_scans_per_day_min'])
    random_scans_per_day_max = str(request.form['random_scans_per_day_max'])
    random_interval_min = str(request.form['random_interval_min'])
    random_interval_max = str(request.form['random_interval_max'])
    
    config.set('main','start_output_on_device_start',start_output)
    save_upcs_to_select_settings(upcs_to_select_min)
    save_random_scans_per_day_settings(random_scans_per_day_min, random_scans_per_day_max)
    save_random_interval_settings(random_interval_min, random_interval_max)
    write_to_log('Saved Settings')
    return jsonify({'message': 'Settings saved successfully'})

def save_upcs_to_select_settings(min_val):
    config.set('main', 'upcs_to_select_settings', min_val)
    with open('config.ini', 'w') as f:
        config.write(f)

def save_random_scans_per_day_settings(min_val, max_val):
    values = {'min': min_val, 'max': max_val}
    config.set('main', 'random_scans_per_day_settings', json.dumps(values))
    with open('config.ini', 'w') as f:
        config.write(f)

def save_random_interval_settings(min_val, max_val):
    values = {'min': min_val, 'max': max_val}
    config.set('main', 'random_interval_settings', json.dumps(values))
    with open('config.ini', 'w') as f:
        config.write(f)

def load_settings():
    config.read('config.ini') 
    try:
        start_output = config.get('main','start_output_on_device_start')
    except:
        init_settings()
        start_output = config.get('main','start_output_on_device_start')
    
    if start_output == 'true':
        start_output = True
    else:
        start_output = False
    upcs_to_select_min = int(config.get('main', 'upcs_to_select_settings'))
    random_scans_per_day_values = json.loads(config.get('main', 'random_scans_per_day_settings'))
    random_interval_values = json.loads(config.get('main', 'random_interval_settings'))
    random_scans_per_day_min = random_scans_per_day_values['min']
    random_scans_per_day_max = random_scans_per_day_values['max']
    random_interval_min = random_interval_values['min']
    random_interval_max = random_interval_values['max']
    return start_output,upcs_to_select_min, random_scans_per_day_min, random_scans_per_day_max, random_interval_min, random_interval_max

@app.route('/test')
def test():
    selected_upcs = {}
    random_scans = json.loads(config.get('main', 'random_scans_per_day_settings'))
    upcs_to_select = config.get('main', 'upcs_to_select_settings')
    for x in range(0,int(upcs_to_select)):
        upcs = load_items()
        upc = random.choice(upcs)
        upcs.remove(upc)
        selected_upcs[upc] = random.randint(int(random_scans['min']),int(random_scans['max']))
    print(selected_upcs)
    write_to_log(f'Selected barcodes and the selection limit value: {selected_upcs}')    
    return jsonify({'message': 'Settings saved successfully'})

if __name__ == '__main__':
    
    thread = Thread(target=task_daemon,daemon=True)
    thread.start()
    
    if host:
        app.run(debug=True, host=host)
    else:
        app.run(debug=True, host="0.0.0.0")
