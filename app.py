from flask import Flask, request, jsonify, render_template, redirect, url_for
import json

app = Flask(__name__)


# Đường dẫn đến file JSON
JSON_FILE = 'gas_stations.json'

# Đọc dữ liệu từ file JSON
def read_gas_stations():
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# Ghi dữ liệu vào file JSON
def write_gas_stations(data):
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():

    return render_template('index.html', gas_stations=read_gas_stations())

@app.route('/list')
def list_gas_station():
    gas_stations = read_gas_stations()
    return render_template('list_station.html', gas_stations=gas_stations)

@app.route('/add', methods=['GET', 'POST'])
def add_gas_station():
    if request.method == 'POST':
        new_station = {
            "name": request.form['name'],
            "lat": float(request.form['lat']),
            "lng": float(request.form['lng'])
        }
        gas_stations = read_gas_stations()
        gas_stations.append(new_station)
        write_gas_stations(gas_stations)
        return redirect(url_for('list_gas_station'))
    return render_template('add_station.html')

@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit_gas_station(index):
    gas_stations = read_gas_stations()
    if request.method == 'POST':
        gas_stations[index] = {
            "name": request.form['name'],
            "lat": float(request.form['lat']),
            "lng": float(request.form['lng'])
        }
        write_gas_stations(gas_stations)
        return redirect(url_for('list_gas_station'))
    return render_template('edit_station.html', gas_station=gas_stations[index], index=index)

@app.route('/delete/<int:index>', methods=['GET', 'POST'])
def delete_gas_station(index):
    gas_stations = read_gas_stations()
    if request.method == 'POST':
        gas_stations.pop(index)
        write_gas_stations(gas_stations)
        return redirect(url_for('list_gas_station'))
    return render_template('delete_station.html', gas_station=gas_stations[index], index=index)

@app.route('/search', methods=['POST'])
def search():
    keywords = request.json.get('keywords', [])
    gas_stations = read_gas_stations()
    results = [station for station in gas_stations if any(keyword.lower() in station['name'].lower() for keyword in keywords)]
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
