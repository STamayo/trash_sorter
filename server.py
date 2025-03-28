from flask import Flask, jsonify
import serial
import serial.tools.list_ports
from flask_cors import CORS
import time
import video_processing
import threading

current_type = -1
current_type_lock = threading.Lock()

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests
# Open serial connection (update 'COM4' if needed)
ser = None


@app.route('/data')
def get_sensor_data():
        ser.reset_input_buffer()
        data = ser.readline().decode('utf-8').strip()

        with current_type_lock:
                waste_type = current_type

        return jsonify({"sensor_value": data, "waste_type": waste_type})


def update_type(typ):
        global current_type
        new_type = typ.get_type()

        if current_type != new_type:
                print(f'sending {new_type} to serial')
                ser.write(bytes([255 if new_type == -1 else new_type]))
                with current_type_lock:
                        current_type = new_type


if __name__ == '__main__':

        ser = serial.Serial('COM6', 9600, timeout=1)
        print([comport.device for comport in serial.tools.list_ports.comports()])
        typ = video_processing.TrashType()

        t2 = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5000, 'debug': False}, daemon=True)

        t1 = threading.Thread(target=video_processing.start_video, args=(typ,), daemon=True)
        
        t2.start()
        t1.start()

        while True:
                update_type(typ)
                                        
                time.sleep(0.2)

        
        
        

        
