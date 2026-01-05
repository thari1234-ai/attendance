const video = document.getElementById("video");

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    });

function capture() {
    const name = document.getElementById("name").value;
    if (!name) {
        alert("Enter name first!");
        return;
    }

    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext("2d").drawImage(video, 0, 0);

    const image = canvas.toDataURL("image/jpeg");

    fetch("/capture", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: name, image: image })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("status").innerText =
            "Marked: " + data.name + " at " + data.time;
    });
}
