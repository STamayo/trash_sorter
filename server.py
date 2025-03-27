from flask import Flask, jsonify
import serial
import serial.tools.list_ports
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # Allow cross-origin requests
# Open serial connection (update 'COM4' if needed)
ser = None

@app.route('/data')
def get_sensor_data():
        ser.reset_input_buffer()
        data = ser.readline().decode('utf-8').strip()
        return jsonify({"sensor_value": data})

if __name__ == '__main__':
    ser = serial.Serial('COM4')
    print([comport.device for comport in serial.tools.list_ports.comports()])
    app.run(host='0.0.0.0', port=5000, debug=False)
