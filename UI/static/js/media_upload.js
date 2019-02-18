let imageFormData = new FormData();
let imageFileField = document.querySelector("#image");
let imageError = document.getElementById("image_error");

let videoFormData = new FormData();
let videoFileField = document.querySelector("#video");
let videoError = document.getElementById("video_error");

//uploaded image preview and file size validation
imageFileField.onchange = function () {
    let fileSize = imageFileField.files[0].size / 1024 / 1024;

    let imageUploadButton = document.getElementById("upload_image");
    let output = document.getElementById('myImg');


    if (fileSize > 2) {
        imageError.style.display = 'block';
        imageError.innerHTML = 'Maximum allowed image size is 2 MB';
        imageUploadButton.disabled = true;
        output.src = "";


    } else {
        imageError.style.display = 'none';
        imageUploadButton.disabled = false;
        output.src = URL.createObjectURL(imageFileField.files[0]);


    }

};

//uploaded video preview and file size validation
videoFileField.onchange = function () {
    let fileSize = videoFileField.files[0].size / 1024 / 1024;

    let videoUploadButton = document.getElementById("upload_video");
    let videoPreview = document.getElementById('myVideo');


    if (fileSize > 10) {
        videoError.style.display = 'block';
        videoError.innerHTML = 'Maximum allowed video size is 10 MB';
        videoUploadButton.disabled = true;
        videoPreview.src = "";
        videoPreview.style.display = "none";


    } else {
        videoError.style.display = 'none';
        videoUploadButton.disabled = false;
        videoPreview.style.display = "block";

        videoPreview.src = URL.createObjectURL(videoFileField.files[0]);


    }

};


let clearImagePreview = function () {
    document.getElementById("myImg").src = '';
    imageFileField.value = '';

};

let clearVideoPreview = function () {
    document.getElementById("myVideo").src = '';
    videoFileField.value = '';

};


function uploadImage() {
    imageFormData.append('image', imageFileField.files[0]);

    let url = "https://ireporterapiv3.herokuapp.com/api/v2/".concat(params.get('type'), "/", params.get('id'), '/addImage');

    let uploadProgress = document.getElementById('progress_img');
    uploadProgress.style.display = 'block';

    fetch(url, {
        method: 'PATCH',
        body: imageFormData,
        headers: {
            "Authorization": authorizationHeader,
        },
    })
        .then(response => response.json())
        .then(response => {
            if (response.status === 200) {
                uploadProgress.style.display = 'none';
                clearImagePreview();
                retrieveImage(response.data[0].imageName)
            }
        })
        .catch(error => console.error('Error:', error));

}

function retrieveImage(imageName) {
    let url = "https://ireporterapiv3.herokuapp.com/api/v2/incidents/images/" + imageName;
    fetch(url,
        {
            method: 'GET',
            headers: {
                "Authorization": authorizationHeader,
            },
        }
    ).then(response => response.blob())
        .then(image => {
                imageUrl = URL.createObjectURL(image);
                var node = document.createElement("img");
                node.src = imageUrl;
                document.getElementById("serve_images").appendChild(node);

            }
        )
}


function uploadVideo() {
    videoFormData.append('video', videoFileField.files[0]);

    let url = "https://ireporterapiv3.herokuapp.com/api/v2/".concat(params.get('type'), "/", params.get('id'), '/addVideo');

    let videoUploadProgress = document.getElementById('progress_video');
    videoUploadProgress.style.display = 'block';

    fetch(url, {
        method: 'PATCH',
        body: videoFormData,
        headers: {
            "Authorization": authorizationHeader,
        },
    })
        .then(response => response.json())
        .then(response => {
            if (response.status === 200) {
                videoUploadProgress.style.display = 'none';
                document.getElementById('myVideo').style.display = 'none';
                videoFileField.value = '';

                clearImagePreview();
                retrieveVideo(response.data[0].videoName)
            }
        })
        .catch(error => console.error('Error:', error));

}

function retrieveVideo(videoName) {
    let url = "https://ireporterapiv3.herokuapp.com/api/v2/incidents/videos/" + videoName;
    fetch(url,
        {
            method: 'GET',
            headers: {
                "Authorization": authorizationHeader,
            },
        }
    ).then(response => response.blob())
        .then(video => {


                let videoUrl = URL.createObjectURL(video);
                var node = document.createElement("video");
                node.src = videoUrl;
                node.controls = true;
                node.width = 320;
                node.height = 240;

                document.getElementById("serve_videos").appendChild(node);


            }
        )
}
