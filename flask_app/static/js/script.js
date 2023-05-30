let login_modal = document.getElementById("login-modal");
let reg_modal = document.getElementById("register-modal")
let btn = document.getElementById("open-btn");
let reg_btn = document.getElementById("open-reg")
let button = document.getElementById("ok-btn");


btn.onclick = function() {
    login_modal.style.display = "block";
}
reg_btn.onclick = function() {
    reg_modal.style.display = "block";
}

window.onclick = function(event) {
    if (event.target == login_modal || event.target==reg_modal) {
    login_modal.style.display = "none";
    reg_modal.style.display = "none"
    }
    if (event.target == cartCanvas){
        cartCanvas.style.display = "none";
    }
}



