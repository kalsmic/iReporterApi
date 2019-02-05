function displayError(dataArray) {

    for (let key in dataArray) {

        if ({}.hasOwnProperty.call(dataArray, key)) {
            let fieldError = document.getElementById(key + "-error");
            fieldError.style.display = "block";
            fieldError.innerHTML = dataArray[key];
        }
    }
}

let authorizationHeader = "Bearer ".concat(localStorage.getItem("token"));

let incidentType = document.getElementById("incident_type");
let incidentTitle = document.getElementById("incident_title");
let incidentComment = document.getElementById("comment");
let incidentlocation = document.getElementById("set_location");
let locationError = document.getElementById("location-error");

incidentTitle.onkeyup = function () {
    let titleError = document.getElementById('title-error');

    if (incidentTitle.value.length < 4) {
        titleError.style.display = "block";
        titleError.innerHTML = "Title must contain atleast 4 characters";
        incidentTitle.setCustomValidity("Invalid record title.");


    } else if (incidentTitle.value.length > 100) {
        titleError.style.display = "block";
        titleError.innerHTML = "Title can not contain more than 100 characters";
        incidentTitle.setCustomValidity("Invalid record title.");

    } else {
        titleError.style.display = "none";
        incidentTitle.setCustomValidity("");

    }


};

incidentComment.onkeyup = function () {
    let commentError = document.getElementById('comment-error');
    if (incidentComment.value.trim().length < 20) {
        incidentComment.setCustomValidity("Invalid comment.");
        commentError.style.display = "block";
        commentError.innerHTML = "Comment should have at least 20 characters";
    } else {
        commentError.style.display = "none";
        incidentComment.setCustomValidity("");
    }
};

incidentComment.onblur = function () {

    if (incidentlocation.value === "") {
        locationError.style.display = "block";
        locationError.innerHTML = "Please pick a location from the map";
        incidentlocation.setCustomValidity("Invalid location Coordinates.");

    } else {
        locationError.style.display = "none";
        incidentlocation.setCustomValidity("");

    }

};

document.getElementById('googleMap').onclick = function () {
    locationError.style.display = "none";
    incidentlocation.setCustomValidity("");

};


function createIncident() {

    let url = "https://ireporterapiv3.herokuapp.com/api/v2/incidents";
    let newIncident = {
        title: incidentTitle.value,
        comment: incidentComment.value,
        location: locationCoordinates,
        type: incidentType.value,

    };

    fetch(url, {
        method: "POST",
        headers: {
            "content-type": "application/json",
            "Authorization": authorizationHeader,
        },
        body: JSON.stringify(newIncident),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.status === 400) {
                //Bad format data
                displayError(data.error);


            } else if (data.status === 401) {
                displayError(data.error);
                window.setTimeout(function () {
                    window.location.replace("../index.html");
                }, 5000);


            } else if (data.status === 201) {
                //on success
                let newRecord = data["data"][0][incidentType.value];
                let successMsg = data["data"][0]["success"];
                let newRecordDetails = `
                       <h3 class="text-green">Successfully ${successMsg} !</h3>

                    <hr>
                    <section class="flex-col-sp-btn border-radius-30p border-round-lg">

                        <h4>${newRecord.title}</h4>
                        <div><b>Description : </b>
                           ${newRecord.comment}
                        </div>
                     
                        <div class="flex-row-sp-btn">
                            <p class="text-blue"><b><i>Created On:</i> </b> ${newRecord.created_on}</p>
                            status: <span class="text-blue">${newRecord.status}</span>
                        </div>
                    </section>

                `;

                document.getElementById('create_record').innerHTML = newRecordDetails;

            }


        })
        .catch((error) => console.log(error));

}

