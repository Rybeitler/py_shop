let file = document.getElementById("pie-img")
let imgPrev = document.getElementById("img-prev")

const displayPrev = (e) => {
    let input = e.target
    const imageURL = URL.createObjectURL(input.files[0]);
    imgPrev.src = imageURL;
}

file.addEventListener("change", displayPrev);