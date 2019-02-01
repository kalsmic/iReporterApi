let confirmPassword = document.getElementById("confirm_password");
let password = document.getElementById("password");
let firstName = document.getElementById("firstname");
let lastName = document.getElementById("lastname");
let otherNames = document.getElementById("othernames");
let email = document.getElementById("email");
let userName = document.getElementById("username");
let phoneNumber = document.getElementById("phoneNumber");


function validatePassword () {
    let confirmPasswordError = document.getElementById('confirm_pass-error');
    if (password.value != confirmPassword.value) {
        confirmPasswordError.style.display = "block";
        confirmPasswordError.innerHTML = "Passwords Do not  match";
    }
    else{
        confirmPasswordError.style.display = "none";
    }

}
password.onkeyup = validatePassword;
confirmPassword.onkeyup = validatePassword;

    function displayError(dataArray) {
    for (let key in dataArray) {

        let fieldError = document.getElementById(key + '-error');
        fieldError.style.display = 'block';
        fieldError.innerHTML = dataArray[key]

    }
}

function signUpAccount() {
    let fields =  {
        "username":userName,
        "password":password

    };

    Object.keys(fields).map(function (key, index) {
        if (fields[key].isEmpty()) {
            document.getElementById((key +"-error").style.display = "block";
            document.getElementById((key +"-error").innerHTML = "empty";

        }

    });

    let url = 'http://127.0.0.1:5000/api/v2/auth/signup';
    let newUser = {
        firstname: firstName.value,
        lastname: lastName.value,
        othernames: otherNames.value,
        email: email.value,
        password: password.value,
        username: userName.value,
        phoneNumber: phoneNumber.value
    };

    fetch(url, {
        method: 'POST',
        headers: {
            'content-type': "application/json",
        },
        body: JSON.stringify(newUser),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.status === 400) {
                //Bad format data
                displayError(data.error);

            } else if (data.status === 409) {
                //Duplicate username, email or phone number
                displayError(data.error);

            } else if (data.status === 201) {
                //on successs

                document.getElementById('message').style.display = "block";
                document.getElementById('message').innerHTML = data['data'][0].success;
                window.setTimeout(function () {
                    window.location.replace("../index.html");
                }, 5000);

            }


        })
        .catch((error) => console.log(error))

}
