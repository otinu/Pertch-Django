let animationTimer = 50

const partialAdd = async (menuIcon, borderType) => {
    return new Promise(resolve => {
        setTimeout(() => {
            menuIcon.style[borderType] = "solid 2px"
            resolve()
        }, animationTimer)
    })
}

const partialDelete = (menuIcon, borderType) => {
    return new Promise(resolve => {
        setTimeout(() => {
            menuIcon.style[borderType] = "none"
            resolve()
        }, animationTimer)
    })
}

const appearBorder = async (menuIcon) => {
    menuIcon.classList.toggle('menu-open')
    document.body.style.backgroundColor = "white"
    let menuArea = document.body.querySelector("#menu-area")
    menuArea.style.visibility = "hidden"
    menuArea.style.height = "0"
    await partialAdd(menuIcon, "border-left")
    await partialAdd(menuIcon, "border-bottom")
    await partialAdd(menuIcon, "border-right")
    await partialAdd(menuIcon, "border-top")
    setTimeout(() => {
        document.body.style.visibility = "visible"
        menuIcon.style.pointerEvents = "auto"
    }, animationTimer)

}

const vanishBorder = async (menuIcon) => {

    await partialDelete(menuIcon, "border-top")
    await partialDelete(menuIcon, "border-right")
    await partialDelete(menuIcon, "border-bottom")
    await partialDelete(menuIcon, "border-left")
    setTimeout(() => {
        menuIcon.classList.toggle('menu-open')
        menuIcon.style.visibility = "visible"
        document.body.style.visibility = "hidden"
        document.body.style.backgroundColor = "#b0c4de"

        let menuArea = document.body.querySelector("#menu-area")
        menuArea.style.visibility = "visible"
        menuArea.style.height = "60vh"
        menuIcon.style.pointerEvents = "auto"
    }, 300)

}

// ドキュメント読み込み----------------------------------------------------------

document.addEventListener("DOMContentLoaded", function () {
    let menuIcon = document.body.querySelector(".hamburger-menu")
    menuIcon.addEventListener("click", () => {
        menuIcon.style.pointerEvents = "none"
        if (menuIcon.classList.contains('menu-open')) {
            appearBorder(menuIcon)
        } else {
            vanishBorder(menuIcon)
        }
    })

    let logout = document.body.querySelector("#logout")
    logout.addEventListener("click", () => {
        logout.submit()
    })

})


