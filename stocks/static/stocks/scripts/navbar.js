const navbarLinks = document.getElementById("navigation").firstElementChild.firstElementChild.children

for (let navlink of navbarLinks) {
    navlink.addEventListener("mouseover", (event) => {
        event.target.style.opacity = 0.5
    })

    navlink.addEventListener("mouseout", (event) => {
        event.target.style.opacity = 1.0
    })
}