function login() {

    const url = "https://ireporterapiv3.herokuapp.com/api/v2/auth/login";
    const userCredentials = {
        username: username.value,
        password: password.value
    };

    const submitProgress = document.getElementById("submit_progress");
    submitProgress.style.display = 'block';

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
                submitProgress.style.display = 'none';
                document.getElementById("success").style.display = "none";
                document.getElementById("error").style.display = "block";
                document.getElementById("error").innerHTML = data.error;
                window.setTimeout(function () {
                    document.getElementById("error").style.display = "none";

                }, 3000);


            } else if (data.status === 200) {

                //on success
                submitProgress.style.display = 'none';
                document.getElementById("error").style.display = "none";
                document.getElementById("success").style.display = "block";
                document.getElementById("success").innerHTML = data["data"][0].success;
                localStorage.setItem("iReporterToken", data["data"][0].token);

                window.setTimeout(function () {
                    window.location.replace("./incidents/index.html");
                }, 1000);

            }


        })
        .catch((error) => console.log(error))

}