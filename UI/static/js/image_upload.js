var formData = new FormData();
var fileField = document.querySelector("input[type='file']");

var previewImage = function (event) {
    var output = document.getElementById('myImg');
    output.src = URL.createObjectURL(event.target.files[0]);
};

function uploadImage() {
    formData.append('image', fileField.files[0]);
    let url = "https://ireporterapiv3.herokuapp.com/api/v2/".concat(params.get('type'), "/", params.get('id'), '/addImage');


    fetch(url, {
        method: 'PATCH',
        body: formData,
        headers: {
            "content-type": "application/json",
            "Authorization": authorizationHeader,
        },
    })
        .then(response => response.json())
        .then(response => {
            if (response.status == 200) {
                uploadProgress.style.display = 'none';
                document.getElementById("myImg").src = '';
                document.getElementById("image").value = '';
                var node = document.createElement("img");
                node.src = "https://ireporterapiv3.herokuapp.com/api/v2/incidents/images/" + response.data[0].imageName;
                document.getElementById("serve_images").appendChild(node);
            }
        })
        .catch(error => console.error('Error:', error));

}
