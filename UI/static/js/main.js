let authorizationHeader = "Bearer ".concat(localStorage.getItem("iReporterToken"));

if (localStorage.getItem('iReporterToken')) {

    getUserInfo()
} else {
    window.location.replace("../index.html");

}
window.setInterval(getUserInfo, 300000);

function getUserInfo() {
    fetch("https://ireporterapiv3.herokuapp.com/api/v2/auth/secure", {
        method: "POST",
        headers: {
            "content-type": "application/json",
            "Authorization": "Bearer ".concat(localStorage.getItem("iReporterToken")),
        },
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.status === 401) {
                alert(data.error);
                redirectLoggedOut()

            } else if (data.status === 200) {
                //on success
                let userInfo = data["data"][0]["user"];
                let sessionUserName = userInfo["username"];
                let sessionFirstName = userInfo["firstname"];
                let sessionLastName = userInfo["lastname"];
                let sessionIsAdmin = userInfo["is_admin"];
                document.getElementById('sessionUserName').innerHTML = sessionUserName;

                if (sessionIsAdmin) {
                    setElementDisplay(".hideAdmin", "none");
                    setElementDisplay(".showAdmin", "block");
                } else {

                    setElementDisplay(".hideAdmin", "block");
                    setElementDisplay(".showAdmin", "none");

                }
            }


        })
        .catch((error) => console.log(error));

}

function setElementDisplay(elemRef, displayPropety) {
    Array.from(document.querySelectorAll(elemRef))
        .forEach(function (elem) {
            elem.style.display = displayPropety
        });

}


function logOut() {

    fetch("https://ireporterapiv3.herokuapp.com/api/v2/auth/logout", {
        method: "POST",
        headers: {
            "content-type": "application/json",
            "Authorization": "Bearer ".concat(localStorage.getItem("iReporterToken")),
        },
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.status === 200) {
                alert(data['data'][0].success);
                redirectLoggedOut()
            } else if (data.status === 401) {
                localStorage.removeItem('iReporterToken');
                alert(data.error);
                redirectLoggedOut()

            }


        })
        .catch((error) => console.log(error));

}

function redirectLoggedOut() {
    localStorage.removeItem('iReporterToken');
    window.location.replace("../index.html");

}