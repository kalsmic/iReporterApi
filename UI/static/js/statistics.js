let url = "https://ireporterapiv3.herokuapp.com/api/v2/statistics";

fetch(url, {
    method: "GET",
    headers: {
        "content-type": "application/json",

        "Authorization": "Bearer ".concat(authorizationHeader)
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
            let incidents = data["data"][0]["statistics"];
            document.getElementById('red-flags').innerHTML = `
                <h3 class="text-red">
                    <i class="fa fa-flag text-lred" aria-hidden="true">&nbsp;</i>
                        Red-flags (${incidents['red-flags']['total']})
                </h3>
                <div class="dashboard-items">
                    <div class="dash bg-lyellow text-orange">
                        <div class="dash-stat bg-orange">${incidents['red-flags']['draft']}
                        </div>
                    <div>Draft</div>
                    </div>
                    <div class="dash bg-lblue text-blue">
                    <div class="dash-stat bg-blue">${incidents['red-flags']['under_investigations']}</div>
                    <div> Under Investigation</div>
                </div>
                <div class="dash bg-lgreen text-green">
                    <div class="dash-stat bg-green">${incidents['red-flags']['resolved']}</div>
                    <div>Resolved</div>
                    </div>
                    <div class="dash bg-pink text-red">
                      <div class="dash-stat bg-red">${incidents['red-flags']['rejected']}</div>
                      <div>Rejected</div>
                    </div>
                </div>
            `;
            document.getElementById('interventions').innerHTML = `
                <h3 class="text-green">
                    <i class="fa fa-cubes text-green" aria-hidden="true">&nbsp;</i>
                    Interventions (${incidents['interventions']['total']})
                </h3>

                <div class="dashboard-items">
                    <div class="dash bg-lyellow text-orange">
                        <div class="dash-stat bg-orange">${incidents['interventions']['draft']}</div>
                        <div>Draft</div>
                    </div>
                    <div class="dash bg-lblue text-blue">
                        <div class="dash-stat bg-blue">${incidents['interventions']['under_investigations']}</div>
                        <div>Under Investigation</div>
                    </div>
                    <div class="dash bg-lgreen text-green">
                        <div class="dash-stat bg-green">${incidents['interventions']['resolved']}</div>
                        <div>Resolved</div>
                    </div>
                    <div class="dash bg-pink text-red">
                        <div class="dash-stat bg-red">${incidents['interventions']['rejected']}</div>
                        <div>Rejected</div>
                    </div>
                </div>

            `;
            document.getElementById('user_dash_info').innerHTML = `
                <img src="../static/img/profile-pics/user1.png" class="img-profile" alt="profile picture">
                <p>Username: ${sessionStorage.getItem('iRUsername')}</p>
                <p>First Name: ${sessionStorage.getItem('iRFirstName')}</p>
                <p>Last Name: ${sessionStorage.getItem('iRlastName')}</p>
                <p id="other_names">Other Names: ${sessionStorage.getItem('iROtherNames')}</p>
                <p>Tel: ${sessionStorage.getItem('iRPhoneNumber')}</p>
                <p>Email: ${sessionStorage.getItem('iREmail')}</p>
                              
            `;

            if (!sessionStorage.getItem('iROtherNames')) {
                document.getElementById('other_names').style.display = 'none';
            }


        }


    })
    .catch((error) => console.log(error));

