from flask import Flask, render_template, request, jsonify
import json
import time
import sys
from configparser import ConfigParser
import os
config = ConfigParser()

host = ''
app = Flask(__name__)

if os.path.exists('config.ini') == False:
    config.add_section('main')
    
    config.set('main', 'items_per_run_settings', '{"min":1,"max":5}')
    config.set('main', 'repeat_times_settings', '{"min":1,"max":5}')
    config.set('main','items','')
    

    with open('config.ini', 'w') as f:
        config.write(f)
           
config.read('config.ini')  
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



def save_settings(key, min_val, max_val):
    values = {'min':min_val,'max':max_val}
    config.set('main', key, json.dumps(values))
    
    with open('config.ini', 'w') as f:
        config.write(f)


def load_settings(key):
    values = json.loads(config.get('main',key))
    return values['min'],values['max']
        


@app.route('/')
def index():
    items_per_run_min, items_per_run_max = load_settings("items_per_run_settings")
    repeat_times_min, repeat_times_max = load_settings("repeat_times_settings")
    return render_template('index.html', items=load_items(), items_per_run_min=items_per_run_min, items_per_run_max=items_per_run_max,
                           repeat_times_min=repeat_times_min, repeat_times_max=repeat_times_max)



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
    items = load_items()
    item = request.form['item']
    items.append(item)
    save_items(items)
    return jsonify({'message': 'Item added successfully'})

@app.route('/remove_selected_items', methods=['POST'])
def remove_selected_items():
    global items
    indexes = list(map(int, json.loads(request.form['indexes'])))
    indexes.sort(reverse=True)  # Remove items in reverse order to avoid index issues
    for index in indexes:
        del items[index]
    save_items(items)
    return jsonify({'message': 'Items removed successfully'})

@app.route('/save_items_per_run', methods=['POST'])
def save_items_per_run():
    min_val = int(request.form['min'])
    max_val = int(request.form['max'])
    save_settings("items_per_run_settings", min_val, max_val)
    return jsonify({'message': 'Settings saved successfully'})

@app.route('/save_repeat_times', methods=['POST'])
def save_repeat_times():
    min_val = int(request.form['min'])
    max_val = int(request.form['max'])
    save_settings("repeat_times_settings", min_val, max_val)
    return jsonify({'message': 'Settings saved successfully'})

if __name__ == '__main__':
    if host:
        app.run(debug=True,host=host)
    else:
        app.run(debug=True,host="0.0.0.0")
