//light up button
const button = document.getElementById('toggle-btn');
const light1 = document.querySelector('.light1');
const light2 = document.querySelector('.light2');
const light3 = document.querySelector('.light3');

button.addEventListener('click', () => {
light1.classList.toggle('active');
light2.classList.toggle('active');
light3.classList.toggle('active');
});



const video = document.getElementById('webcam');

// Request permission to use the webcam and stream it
navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => { // Assign the stream to the video element's source
        video.srcObject = stream;
    })
    .catch((error) => {
        console.error('Error accessing webcam: ', error);
    });



    async function fetchData() {
        try {
            const response = await fetch('http://127.0.0.1:5000/data');  // Fetch from Flask server
            const data = await response.json();     // Convert response to JSON
            const val = parseInt(data.sensor_value, 10);
            if(val > 200){  //change this value
                document.getElementById("sensorValue").innerText = "Full";
            }
            else if(val <= 200){
                document.getElementById("sensorValue").innerText = "Normal";
            }
            
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    }
    
    // Fetch data every second
    setInterval(fetchData, 1000);
    