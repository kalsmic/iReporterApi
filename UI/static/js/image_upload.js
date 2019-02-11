
var formData = new FormData();
var fileField = document.querySelector("input[type='file']");

var previewImage = function(event) {
    var output = document.getElementById('myImg');
    output.src = URL.createObjectURL(event.target.files[0]);
};
function uploadImage(){
    formData.append('image', fileField.files[0]);
    let url = "https://ireporterapiv3.herokuapp.com/api/v2/".concat( params.get('type'), "/",  params.get('id'),'/addImage');


    fetch(url, {
        method: 'PATCH',
        // mode: "no-cors", // no-cors, cors, *same-origin
        body: formData,
        headers: {
            "content-type": "application/json",
            "Authorization": authorizationHeader,
        },
    })
        .then(response => response.json())
        .then(response => console.log(JSON.stringify(response)))
        .catch(error => console.error('Error:', error));

}
