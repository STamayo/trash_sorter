from flask import Flask, jsonify
import serial
import serial.tools.list_ports
from flask_cors import CORS
import time
import video_processing
import threading

current_type = -1

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests
# Open serial connection (update 'COM4' if needed)
ser = None


@app.route('/data')
def get_sensor_data():
        ser.reset_input_buffer()
        data = ser.readline().decode('utf-8').strip()
        return jsonify({"sensor_value": data, "waste_type": current_type})

if __name__ == '__main__':

        ser = serial.Serial('COM5', 9600, timeout=1)
        print([comport.device for comport in serial.tools.list_ports.comports()])
        typ = video_processing.TrashType()

        t2 = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5000, 'debug': False}, daemon=True)

        t1 = threading.Thread(target=video_processing.start_video, args=(typ,), daemon=True)
        
        t2.start()
        t1.start()

        while True:
                current_type = typ.get_type()
                if (current_type != -1):
                        ser.write(bytes([current_type]))
                        #current type: 0 = compost, 1 = trash, 2 = recycle
 #               print(f's: {current_type}')
                time.sleep(0.2)

        
        
        

        
