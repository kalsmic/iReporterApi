var formData = new FormData();
var fileField = document.querySelector("input[type='file']");

var previewImage = function (event) {
    var output = document.getElementById('myImg');
    output.src = URL.createObjectURL(event.target.files[0]);
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
            if (response.status == 200) {
                uploadProgress.style.display = 'none';
                document.getElementById("myImg").src = '';
                document.getElementById("image").value = '';
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
