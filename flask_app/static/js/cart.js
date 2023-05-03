let cartBtn = document.getElementById("cart-btn")
let cartCanvas = document.getElementById("cart-canvas")

cartBtn.onclick = function(){
    cartCanvas.style.display = "block";
}

window.onclick = function(event) {
    if (event.target == cartCanvas) {
    cartCanvas.style.display = "none";
    }
}