let formData = new FormData();
let imageFileField = document.getElementById("image");
let imageError = document.getElementById("image_error");

let previewImage = function (event) {
    let output = document.getElementById('myImg');
    output.src = URL.createObjectURL(event.target.files[0]);

};

imageFileField.onchange = function () {
    let fileSize = imageFileField.files[0].size / 1024 / 1024;
    let imageUploadButton = document.getElementById("upload_image");
    if (fileSize > 2) {
        imageError.style.display = 'block';
        imageError.innerHTML = 'Maximum allowed image size is 2 MB';
        imageUploadButton.disabled = true;

    } else {
        imageError.style.display = 'none';
        imageUploadButton.disabled = false;

    }

};

let clearImagePreview = function () {
    document.getElementById("myImg").src = '';
    imageFileField.value = '';

};


function uploadImage() {
    formData.append('image', fileField.files[0]);

    let url = "https://ireporterapiv3.herokuapp.com/api/v2/".concat(params.get('type'), "/", params.get('id'), '/addImage');

    let uploadProgress = document.getElementById('progres_img');
    uploadProgress.style.display = 'block';

    fetch(url, {
        method: 'PATCH',
        body: formData,
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
