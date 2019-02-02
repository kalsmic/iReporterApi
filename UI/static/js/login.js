// document.getElementById("login-form").onsubmit=function() {
//     var userName = document.getElementById("userName").value;
//     if (userName =="admin") {
//
//     window.location.replace("./UI/admin/profile.html");
//     return false;
//     }else{
//         window.location.replace("./UI/user/profile.html");
//         return false;
//     }
//
//
//
//
// function displayError(dataArray) {
//     for (let key in dataArray) {
//
//         let fieldError = document.getElementById(key + '-error');
//         fieldError.style.display = 'block';
//         fieldError.innerHTML = dataArray[key];
//
//     }
// }

document.getElementById("login-form").onsubmit = function () {


    let url = 'http://127.0.0.1:5000/api/v2/auth/login';
    let userCredentials = {
        username: username.value,
        password: password.value
    };

    fetch(url, {
        method: 'POST',
        headers: {
            'content-type': "application/json",
        },
        body: JSON.stringify(userCredentials),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.status === 401) {
                // Invalid credentials
                // // displayError(data.error);
                let error = document.getElementById('error');
                error.style.display = 'block';
                error.innerHTML = data.error;
                console.log(data.error);


            } else if (data.status === 200) {
                //on success
                console.log(JSON.stringify(data));
                console.log(data['data'][0].success);
                console.log(data['data'][0].token);
                localStorage.setItem("token",data['data'][0].token);
                let redirectUrl = data['data'][0].url;

                // document.getElementById('message').style.display = "block";
                // document.getElementById('message').innerHTML = data['data'][0].success;
                // window.setTimeout(function () {
                    // window.location.replace("../index.html");
                    // window.location.replace("redirectUrl);
                //
                // }, 5000);
                // window.location.replace("./UI/user/profile.html");


            }


        })
        .catch((error) => console.log(error))

}
