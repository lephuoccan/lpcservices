import threading
import requests
from flask import Flask, request, jsonify
import time
import logging
import json
import os

app = Flask(__name__)

# Load configuration from config.json
config_path = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_path, 'r') as config_file:
    config = json.load(config_file)
    api_url = config['api_url']

logging.basicConfig(level=logging.DEBUG)

def check_ports_loop():
    next_check_time = {}
    while True:
        try:
            response = requests.get(f"{api_url}/api/v1/status?proxy=all")
            response.raise_for_status()
            data = response.json()
            logging.debug("Received data: %s", data)
        except requests.exceptions.RequestException as e:
            logging.error("Error fetching status: %s", e)
            time.sleep(11)
            continue

        if 'data' in data:
            current_time = time.time()
            for port_data in data['data']:
                port = port_data.get('port')
                if port == 1000:  # Bỏ qua port 1000
                    continue
                if port_data.get('status') == 'NO_DEVICE':
                    continue
                if port in next_check_time and current_time < next_check_time[port]:
                    continue
                if port_data.get('usb_status') == 'RESETING':
                    next_check_time[port] = current_time + 11
                    continue
                if port_data.get('usb_status') != 'CONNECTED':
                    try:
                        requests.get(f"{api_url}/api/v1/reset?proxy={port}")
                        logging.info("Resetting port %s", port)
                    except requests.exceptions.RequestException as e:
                        logging.error("Error resetting port %s: %s", port, e)
                    next_check_time[port] = current_time + 11
                    time.sleep(1)
        time.sleep(11)

@app.route('/lpcapi/status', methods=['GET'])
def get_usb_status():
    proxy_port = request.args.get('port', type=int)
    if proxy_port is None:
        return jsonify({"error": "Missing parameter 'port'"}), 400
    
    try:
        response = requests.get(f"{api_url}/api/v1/status?proxy={proxy_port}")
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        logging.error("Error fetching status for port %s: %s", proxy_port, e)
        return jsonify({"error": "Failed to fetch status"}), 500

    if 'data' in data and 'usb_status' in data['data']:
        usb_status = data['data']['usb_status']
        return jsonify({"port": proxy_port, "usb_status": usb_status})
    
    return jsonify({"error": "No USB status found"}), 404

if __name__ == '__main__':
    port_check_thread = threading.Thread(target=check_ports_loop, daemon=True)
    port_check_thread.start()
    app.run(host='0.0.0.0', port=8080, debug=True)
