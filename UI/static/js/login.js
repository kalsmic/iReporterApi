document.getElementById("login-form").onsubmit=function() {
    var userName = document.getElementById("userName").value;
    if (userName =="admin") {
     
    window.location.replace("./UI/admin/profile.html");
    return false;
    }else{
        window.location.replace("./UI/user/profile.html");
        return false;
    } 
 }  