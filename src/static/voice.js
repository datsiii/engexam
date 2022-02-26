const URL = '/voice';
let div = document.createElement('div');
div.id = 'messages';
let start = document.createElement('button');
start.id = 'start';
start.innerHTML = 'Start';
let stop = document.createElement('button');
stop.id = 'stop';
stop.innerHTML = 'Stop';
let control = document.createElement('div');
control.id = 'control';

document.body.appendChild(div);
document.body.appendChild(start);
document.body.appendChild(stop);
document.body.appendChild(control);
navigator.mediaDevices.getUserMedia({ audio: true})
    .then(stream => {
        const mediaRecorder = new MediaRecorder(stream);

        document.querySelector('#start').addEventListener('click', function(){
            document.querySelector('#control').innerHTML = 'Recording...';
            mediaRecorder.start();
        });
        let audioChunks = [];
        mediaRecorder.addEventListener("dataavailable",function(event) {
            document.querySelector('#control').innerHTML = 'Recognizing...';
            audioChunks.push(event.data);
        });

        document.querySelector('#stop').addEventListener('click', function(){
            mediaRecorder.stop();
        });

        mediaRecorder.addEventListener("stop", function() {
            const audioBlob = new Blob(audioChunks, {
                mimeType: 'audio/wav; codecs = psm'
            });

            let fd = new FormData();
            fd.append('voice', audioBlob);
            sendVoice(fd);
            audioChunks = [];
        });
    });

async function sendVoice(form) {
    let promise = await fetch(URL, {
        method: 'POST',
        body: form});
    if (promise.ok) {
        let response =  await promise.json();

        console.log(response);
//        let audio = document.createElement('audio');
//        audio.src = response.data;
//        audio.controls = true;
//        audio.autoplay = true;
//        document.querySelector('#messages').appendChild(audio);
        response.data.forEach(element => {
            message = document.createElement('p')
            message.innerHTML = element.text
            document.querySelector('#messages').appendChild(message)
        })

        document.querySelector('#control').innerHTML = ""
    }
}