let params = new URL(location.href).searchParams;
let urlParameter = params.get('type');

if (urlParameter === "red-flags" || urlParameter === "interventions") {
    getIncident(urlParameter, params.get('id'));
}


function getIncident(incidentType, incidentId) {

    let url = "https://ireporterapiv3.herokuapp.com/api/v2/".concat(incidentType, "/", incidentId);
    console.log(url);

    fetch(url, {
        method: "GET",
        headers: {
            "content-type": "application/json",
            "Authorization": authorizationHeader,
        },
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.status === 401) {
                window.setTimeout(function () {
                    window.location.replace("../index.html");
                }, 5000);


            } else if (data.status === 200) {
                //on success
                let incident = data["data"][0];
                document.getElementById("created_on").innerHTML = `
                    <b><i>Date:</i> </b> ${incident.created_on}`;
                document.getElementById("incident_title").innerHTML = incident.title;
                document.getElementById("incident_type").innerHTML = "View " + incident.type + " Details page";
                document.getElementById("incident_comment").innerHTML = incident.comment;
                document.getElementById("incident_status").innerHTML = incident.status;
                document.getElementById("created_by").innerHTML = `
                    <img class="bg-blue  img-circle-small" src="../static/img/profile-pics/user1.png">${incident.owner}
                `;
                document.getElementById("incident_status").innerHTML = `<b>status: <i>${incident.status}</i></b>`;
                let locationCoords = incident.location.replace('(', '').replace(')', '').split(",");
                let latitude = locationCoords[0];
                let longitude = locationCoords[1];
                displayMap([latitude, longitude]);

            }
            if (data.status === 400 || data.status === 404) {
                let output = `
                      <h3 class="text-red">Error getting record</h3>
                       <hr>
                
                    <section class="flex-col-sp-btn border-radius-30p border-round-lg">                     

                        <h2 class="text-red"> ${data.error} !</h2>
                          
                    </section>
                `;
                document.getElementById('incidents_output').innerHTML = output;


            }


        })
        .catch((error) => console.log(error));


}
