document.getElementById("login-form").onsubmit=function() {
    var userName = document.getElementById("userName").value;
    if (userName =="admin") {
     
    window.location.replace("admin/profile.html");
    return false;
    }else{
        window.location.replace("user/profile.html");
        return false;
    } 
 }  



function deleteIncident(incidentType, delStatus, hideContent) {

    if (delStatus == 1) {
        if (confirm("Are you sure you want to delete this record!")) {

            secId = document.getElementById("sec-1")
            switch (incidentType) {
                case "red-flag":
                    if (hideContent == "true") {
                        secId.style.display = "none";
                        break;

                    } else {
                        window.location.href = "https://kalsmic.github.io/iReporter/UI/user/view_red-flags.html";
                        break;
                    }
                case "intervention":
                    window.location.href = "https://kalsmic.github.io/iReporter/UI/user/view_interventions.html";
                    break;
                default:
                    console.log("Invalid request");
            }

        }
    } else {
        alert("You cannot delete this record");
    }
}