// Handle drag and drop into a dropzone_element div:
// send the files as a POST request to the server
"use strict";

// Only start once the DOM tree is ready
if (document.readyState === "complete") {
    createDropzoneMethods();
} else {
    document.addEventListener("DOMContentLoaded", createDropzoneMethods);
}

function createDropzoneMethods() {
    let dropzone = document.getElementById("dropzone_element");

    dropzone.ondragover = function () {
        this.className = "dropzone dragover";
        return false;
    }

    dropzone.ondragleave = function () {
        this.className = "dropzone";
        return false;
    }

    dropzone.ondrop = function (e) {
        console.log("Dropping")
        // Stop browser from simply opening that was just dropped
        e.preventDefault();
        // Restore original dropzone appearance
        this.className = "dropzone";

        upload_files(e.dataTransfer.files)
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function upload_files(files) {
    var data = new FormData();
    var csrftoken = getCookie('csrftoken');
    console.log("Dropped " + String(files.length) + " files.");
    for (let i = 0; i < files.length; i++) {
        data.append("img", files[i]);
    }
    $.ajax({
        headers: { 'X-CSRFToken': csrftoken },
        url: "upload_handler",
        processData: false,
        contentType: false,
        type: 'POST',
        data: data,
    }).done(function (data) {
        let upload_results = document.getElementById("upload_results_element");
        upload_results.innerHTML = data;
    });
}