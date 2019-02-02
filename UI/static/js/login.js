// document.forms["login-form"].onsubmit =
function login () {

    let url = "https://ireporterapiv3.herokuapp.com/api/v2/auth/login";
    let userCredentials = {
        username: username.value,
        password: password.value
    };

    fetch(url, {
        method: "POST",
        headers: {
            "content-type": "application/json",
        },
        body: JSON.stringify(userCredentials),
    })
        .then(response => response.json())
        .then((data) => {
            if (data.status === 401) {
                // Invalid credentials
                document.getElementById("success").style.display = "none";
                document.getElementById("error").style.display = "block";
                document.getElementById("error").innerHTML = data.error;


            } else if (data.status === 200) {
                //on success
                document.getElementById("error").style.display = "none";
                document.getElementById("success").style.display = "block";
                document.getElementById("success").innerHTML = data["data"][0].success;
                localStorage.setItem("token", data["data"][0].token);


                let redirectUrl = data["data"][0].url;

                window.setTimeout(function () {
                    window.location.replace(redirectUrl);
                }, 5000);

            }


        })
        .catch((error) => console.log(error))

};
