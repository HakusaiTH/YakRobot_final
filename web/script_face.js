alert("robot online complet!");
console.log("robot online");

const firebaseConfig = {
    apiKey: "AIzaSyAfm-wnbuOAVQESBQASW6iyULVu6-Epr3M",
    authDomain: "my-robot-9fdff.firebaseapp.com",
    databaseURL: "https://my-robot-9fdff-default-rtdb.asia-southeast1.firebasedatabase.app",
    projectId: "my-robot-9fdff",
    storageBucket: "my-robot-9fdff.appspot.com",
    messagingSenderId: "989347540267",
    appId: "1:989347540267:web:cfbfa6664cc4e5d2f0e96e",
    measurementId: "G-LXEWXSLQC5"
};

firebase.initializeApp(firebaseConfig);

var database = firebase.database();
var storage = firebase.storage();

const faceImg = document.getElementById("face_img");
const audio = new Audio();

var first_talk = true;

function door_fun() {   
    alert("Moorning!");
    var alertRef = database.ref("/room/A1/Robot/robot_status/alert");
    alertRef.set("OFF");
    playAlertAudio(); 
}

function playAlertAudio() {
    var alertAudioRef = storage.ref("/audio/alert.mp3");

    alertAudioRef.getDownloadURL().then(function (url) {
        console.log("Alert Audio URL:", url);
        audio.src = url;
        audio.play();
    }).catch(function (error) {
        console.error("Error fetching alert audio:", error);
    });
}

function checkAlertTime() {
    var alertRef = database.ref("/room/A1/Robot/robot_status/alert");
    alertRef.on("value", function (snapshot) {
        var alertTime = snapshot.val();
        
        if (alertTime !== "OFF") {
            var formattedAlertTime = alertTime.replace(' ', 'T'); 
            var alertDateTime = new Date(formattedAlertTime);
            var currentDateTime = new Date();

            console.log("current", currentDateTime, "alert", alertDateTime);
            if (
                currentDateTime.getFullYear() === alertDateTime.getFullYear() &&
                currentDateTime.getMonth() === alertDateTime.getMonth() &&
                currentDateTime.getDate() === alertDateTime.getDate() &&
                currentDateTime.getHours() === alertDateTime.getHours() &&
                currentDateTime.getMinutes() === alertDateTime.getMinutes() &&
                currentDateTime.getSeconds() === alertDateTime.getSeconds()
            ) {
                door_fun();
            }
        }
    });
}

function main() {
    checkAlertTime();
    var ref = database.ref("/room/A1/Robot/robot_status/sentiment");
    ref.once("value", function (snapshot) {
        var data = snapshot.val();
        if (data == "N") {
            faceImg.src = "/img/N_0.gif";
        } else {
            faceImg.src = `/img/${data}.png`;
        }
    });
    var talkStatusRef = database.ref("/room/A1/Robot/robot_status/talk_status");
    talkStatusRef.once("value", function (snapshot) {
        var talkStatus = snapshot.val();
        if (talkStatus === true) {
            setTimeout(playAudio, 100);
            talkStatusRef.set(false);
        }
    });

    var doorStatusRef = database.ref("/room/A1/Robot/door_status/sta");
    doorStatusRef.once("value", function (snapshot) {
        var doorStatus = snapshot.val();
        if (doorStatus === "ON") {

            document.getElementById("door_conten").style.display = "inline-block";
            playDoorAudio();

            var imgUrlRef = database.ref("/room/A1/Robot/door_status/img_url");
            imgUrlRef.once("value", function (urlSnapshot) {
                var imageUrl = urlSnapshot.val();
                console.log("Door Status: Open");
                console.log("Door Image URL:", imageUrl);

                document.getElementById("door_img").src = imageUrl;
                doorStatusRef.set("OFF");
            });
        }
    });
}

function playDoorAudio() {
    var doorAudioRef = storage.ref("/audio/door.mp3");

    doorAudioRef.getDownloadURL().then(function (url) {
        console.log("Door Audio URL:", url);
        audio.src = url;
        audio.play();
    }).catch(function (error) {
        console.error("Error fetching door audio:", error);
    });
}

function playAudio() {
    if (first_talk){
        var audioRef = storage.ref("/audio/first.mp3");
    }
    else{
        var audioRef = storage.ref("/audio/output.mp3");
    }

    audioRef.getDownloadURL().then(function (url) {
        console.log("Audio URL:", url);
        audio.src = url;
        audio.play();
    }).catch(function (error) {
        console.error("Error fetching audio:", error);
    });

    first_talk = false;
}

main();
setInterval(main, 1000);

document.getElementById("ennable_sound").addEventListener('click', function () {
    document.getElementById("content").style.display = "inline-block";
    document.getElementById("ennable_sound").style.display = "none";
    playAudio();
});

document.getElementById("exit").addEventListener('click', function () {
    document.getElementById("door_conten").style.display = "none";
});
