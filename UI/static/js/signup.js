let confirmPassword = document.getElementById("confirm_password");
let password = document.getElementById("password");
let firstName = document.getElementById("firstname");
let lastName = document.getElementById("lastname");
let otherNames = document.getElementById("othernames");
let email = document.getElementById("email");
let userName = document.getElementById("username");
let phoneNumber = document.getElementById("phoneNumber");


function validatePasswordStrength() {
    let passwordError = document.getElementById("password-error");

    if (/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)((?!\W+).){8,}$/.test(password.value)) {
        passwordError.style.display = "none";
        password.setCustomValidity("");

    } else {
        passwordError.style.display = "block";
        passwordError.innerHTML = "Password Must contain a Minimum 8 characters" +
            " with atleast one upper case letter, atleast on lower case letter and atleast one number.";
        password.setCustomValidity("Weak Password.");

    }

}

password.onkeyup = validatePasswordStrength;
password.onchange = validatePasswordStrength;

function validatePassword() {
    let confirmPasswordError = document.getElementById("confirm_pass-error");
    if (password.value !== confirmPassword.value) {
        confirmPasswordError.style.display = "block";
        confirmPasswordError.innerHTML = "Passwords Do not  match";
    } else {
        confirmPasswordError.style.display = "none";
    }

}

confirmPassword.onblur = validatePassword;
confirmPassword.onkeyup = validatePassword;


userName.onkeyup = function () {
    let userNameError = document.getElementById("username-error");

    if (/^(?=.*[a-zA-Z0-9])((?!\W+).){5,}$/.test(userName.value)) {
        userNameError.style.display = "none";
        userName.setCustomValidity("");
    } else {
        userNameError.style.display = "block";
        userNameError.innerHTML = "Username must contain atleast five alphabetic characters";
        userName.setCustomValidity("Invalid Username.");

    }

};

firstName.onkeyup = function () {
    let firstNameError = document.getElementById("firstname-error");

    if (/^[a-zA-Z]{3,}$/.test(firstName.value)) {
        firstNameError.style.display = "none";
        firstName.setCustomValidity("");
    } else {
        firstNameError.style.display = "block";
        firstNameError.innerHTML = "First name must contain atleast three alphabetic characters";
        firstName.setCustomValidity("Invalid First Name.");

    }

};

lastName.onkeyup = function () {
    let lastNameError = document.getElementById("lastname-error");

    if (/^[a-zA-Z]{3,}$/.test(lastName.value)) {
        lastNameError.style.display = "none";
        lastName.setCustomValidity("");

    } else {
        lastNameError.style.display = "block";
        lastNameError.innerHTML = "Last name must contain atleast three alphabetic characters";
        lastName.setCustomValidity("Invalid Last name.");
    }

};


otherNames.onkeyup = function () {
    let otherNamesError = document.getElementById("othernames-error");

    if (/^[a-zA-Z]{0,}$/.test(otherNames.value)) {
        otherNamesError.style.display = "none";
        otherNames.setCustomValidity("");

    } else {
        otherNamesError.style.display = "block";
        otherNamesError.innerHTML = "othernames must contain only alphabetic characters if present";
        otherNames.setCustomValidity("Invalid Other names.");

    }

};


phoneNumber.onkeyup = function () {
    let phoneNumberError = document.getElementById("phoneNumber-error");

    if (/^\d{10}/.test(phoneNumber.value)) {
        phoneNumberError.style.display = "none";
        phoneNumber.setCustomValidity("");

    } else {
        phoneNumberError.style.display = "block";
        phoneNumberError.innerHTML = "Phone Number must contain ten digits only";
        phoneNumber.setCustomValidity("Invalid phone number.");

    }

};

function displayError(dataArray) {

    for (let key in dataArray) {

        if ({}.hasOwnProperty.call(dataArray, key)) {
            let fieldError = document.getElementById(key + "-error");
            fieldError.style.display = "block";
            fieldError.innerHTML = dataArray[key];
        }
    }
}

function signUpAccount() {


    let url = "https://ireporterapiv3.herokuapp.com/api/v2/auth/signup";
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
        method: "POST",
        headers: {
            "content-type": "application/json",
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
                //on success

                document.getElementById("message").style.display = "block";
                document.getElementById("message").innerHTML = data["data"][0].success;
                window.setTimeout(function () {
                    window.location.replace("../index.html");
                }, 3000);

            }


        })
        .catch((error) => console.log(error));

}
