//light up button
const button = document.getElementById('toggle-btn');
const light1 = document.querySelector('.light1');
const light2 = document.querySelector('.light2');
const light3 = document.querySelector('.light3');




const video = document.getElementById('webcam');

// // Request permission to use the webcam and stream it
// navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => { // Assign the stream to the video element's source
//         video.srcObject = stream;
//     })
//     .catch((error) => {
//         console.error('Error accessing webcam: ', error);
//     });



    function updateImage() {
        video.src = '../images/current.jpg?' + new Date().getTime();
    }

    async function fetchData() {
        try {
            const response = await fetch('http://127.0.0.1:5000/data');  // Fetch from Flask server
            const data = await response.json();     // Convert response to JSON
            const val1 = parseInt(data.sensor_value, 10);
            if(val1 > 200){  //change this value
                document.getElementById("sensorValue").innerText = "Full";
            }
            else if(val1 <= 200){
                document.getElementById("sensorValue").innerText = "Normal";
            }
            
            //checking waste type
            const val2 = parseInt(data.waste_type, 10);
            if(val2 == -1){ //nothing detected
                light1.classList.remove('active');
                light2.classList.remove('active');
                light3.classList.remove('active');
            }
            else if(val2 == 0){ //compost detected
                light1.classList.remove('active');
                light2.classList.remove('active');
                light3.classList.add('active');
            }
            else if(val2 == 1){ //trash detected
                light1.classList.add('active');
                light2.classList.remove('active');
                light3.classList.remove('active');
            }
            else if(val2 == 2){ //recycle detected
                light1.classList.remove('active');
                light2.classList.add('active');
                light3.classList.remove('active');
            }
            
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    }
    
    // Fetch data every second
    setInterval(fetchData, 1000);
    setInterval(updateImage, 100);
    