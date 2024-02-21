from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

def save_items(filename, items):
    with open(filename, 'w') as f:
        json.dump(items, f)

def load_items(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

items_file = "items.json"
items = load_items(items_file)

def save_settings(filename, min_val, max_val):
    with open(filename, 'w') as f:
        f.write(f"{min_val},{max_val}")

def load_settings(filename):
    try:
        with open(filename, 'r') as f:
            min_val, max_val = map(int, f.read().split(","))
            return min_val, max_val
    except FileNotFoundError:
        return 1, 5  # Default values

items_per_run_min, items_per_run_max = load_settings("items_per_run_settings.txt")
repeat_times_min, repeat_times_max = load_settings("repeat_times_settings.txt")

@app.route('/')
def index():
    return render_template('index.html', items=items, items_per_run_min=items_per_run_min, items_per_run_max=items_per_run_max,
                           repeat_times_min=repeat_times_min, repeat_times_max=repeat_times_max)

@app.route('/add_item', methods=['POST'])
def add_item():
    global items
    item = request.form['item']
    items.append(item)
    save_items(items_file, items)
    return jsonify({'message': 'Item added successfully'})

@app.route('/remove_selected_items', methods=['POST'])
def remove_selected_items():
    global items
    indexes = list(map(int, json.loads(request.form['indexes'])))
    indexes.sort(reverse=True)  # Remove items in reverse order to avoid index issues
    for index in indexes:
        del items[index]
    save_items(items_file, items)
    return jsonify({'message': 'Items removed successfully'})

@app.route('/save_items_per_run', methods=['POST'])
def save_items_per_run():
    min_val = int(request.form['min'])
    max_val = int(request.form['max'])
    save_settings("items_per_run_settings.txt", min_val, max_val)
    return jsonify({'message': 'Settings saved successfully'})

@app.route('/save_repeat_times', methods=['POST'])
def save_repeat_times():
    min_val = int(request.form['min'])
    max_val = int(request.form['max'])
    save_settings("repeat_times_settings.txt", min_val, max_val)
    return jsonify({'message': 'Settings saved successfully'})

if __name__ == '__main__':
    app.run(debug=True,host='192.168.1.72')
