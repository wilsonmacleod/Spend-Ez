window.onload = function () {
    document.getElementById("dLogin").addEventListener("click", function () {
        var logUsername = document.getElementById("usern");
        logUsername.value += "ez_demo";
        var logPW = document.getElementById("passw");
        logPW.value += "demo123";
        document.getElementById("loginSubmit").click()
    })
}
