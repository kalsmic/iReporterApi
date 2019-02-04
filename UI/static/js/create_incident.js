let authorizationHeader = "Bearer ".concat(localStorage.getItem("token"));

let incidentType = document.getElementById("incident_type");
let incidentTitle = document.getElementById("incident_title");
let incidentComment = document.getElementById("description");

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
                // displayError(data.error);
                alert(JSON.stringify(data.error));


            } else if (data.status === 401) {
                //Duplicate username, email or phone number
                // displayError(data.error);
                alert("unat");
                window.setTimeout(function () {
                    window.location.replace("../index.html");
                }, 5000);


            } else if (data.status === 201) {
                //on success
                let newRecord = data["data"][0][incidentType.value];
                let successMsg = data["data"][0]["success"];
                console.log(newRecord);
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

