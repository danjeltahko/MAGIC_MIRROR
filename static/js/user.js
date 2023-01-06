function navbar_button(x) {

    x.classList.toggle("change");
}

function navbar_toggle(x) {

    if (x.classList.contains("change")) {
        document.getElementById("side_navigation").style.width = "100%"
    } else {
        document.getElementById("side_navigation").style.width = "0"
    }
}
