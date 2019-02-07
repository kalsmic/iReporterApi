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
                document.getElementById("incident_status");
                document.getElementById("incident_status").innerHTML = incident.status;
                document.getElementById("created_by").innerHTML = `
                    <img class="bg-blue  img-circle-small" src="../static/img/profile-pics/user1.png">${incident.owner}
                `;

                document.getElementById("incident_status").innerHTML = `<b>status: <i>${incident.status}</i></b>`;
                //Hide the edit comment button if status is not draft
                if (incident.status !== "Draft") {
                    document.getElementById('editCommentBtn').style.display = 'none';
                }
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

function updateComment() {
    newComment = document.getElementById('incident_comment').innerHTML;

    incidentType = params.get('type');
    incidentId = params.get('id');
    let url = "https://ireporterapiv3.herokuapp.com/api/v2/".concat(incidentType, "/", incidentId, "/comment");

    newComment = document.getElementById('incident_comment').innerHTML;
    fetch(url, {
        method: "PATCH",
        headers: {
            "content-type": "application/json",
            "Authorization": authorizationHeader,
        },
        body: JSON.stringify({"comment": newComment})

    })
        .then((response) => response.json())
        .then((data) => {
            if (data.status === 200) {
                document.getElementById('updateCommentBtn').style.display = 'none';
                document.getElementById('cancelEditCommentBtn').style.display = 'none';
                document.getElementById('editCommentBtn').style.display = 'none';
                newComment.innerHTML = data['data'][0].comment;
                document.getElementById('commentMessage').style.display = 'block';

                document.getElementById('commentMessage').innerHTML = data['data'][0].success;
                window.setTimeout(function () {
                    document.getElementById('commentMessage').style.display = 'none';
                    document.getElementById('editCommentBtn').style.display = 'block';

                }, 3000);
                //    remove original comment content from memory
                sessionStorage.removeItem('originalContent');

            } else if (data.status === 400) {
                document.getElementById('commentError').style.display = 'block';

                document.getElementById('commentError').innerHTML = data.error;
                window.setTimeout(function () {
                    document.getElementById('commentError').style.display = 'none';
                    document.getElementById('editCommentBtn').style.display = 'block';
                    document.getElementById('incident_comment').innerHTML = sessionStorage.getItem('originalContent');

                }, 3000);
            } else if (data.status === 401) {
                // if session is expired
                alert(data.error);
                window.setTimeout(function () {
                    localStorage.removeItem('iReporterToken');

                }, 3000);

            }
        })
        .catch((error) => console.log(error.json()));
}


displayUpdateFields("incident_comment", "updateCommentBtn", "cancelEditCommentBtn", "editCommentBtn");


function displayUpdateFields(incidentFieldId, updateButtonId, cancelButtonId, editButtonId) {
    let incidentField = document.getElementById(incidentFieldId);
    let updateField = document.getElementById(updateButtonId);
    let cancelEditField = document.getElementById(cancelButtonId);
    let editField = document.getElementById(editButtonId);

    editField.onclick = function () {
        sessionStorage.setItem('originalContent', incidentField.innerHTML);
        incidentField.contentEditable = true;
        updateField.style.display = 'block';
        cancelEditField.style.display = 'block';
        editField.style.display = 'none';

    };

    cancelEditField.onclick = function () {

        incidentField.contentEditable = false;
        incidentField.innerHTML = sessionStorage.getItem('originalContent');
        sessionStorage.removeItem('originalContent');
        updateField.style.display = 'none';
        cancelEditField.style.display = 'none';
        editField.style.display = 'block';

    };

    updateField.onclick = function () {
        incidentField.contentEditable = false;
        updateField.style.display = 'none';
        cancelEditField.style.display = 'none';
        editField.style.display = 'block';

    }


}


document.getElementById('updateCommentBtn').onclick = updateComment;