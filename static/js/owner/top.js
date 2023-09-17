const messageSecond = "令和3年度 環境省 統計資料「犬・猫の引取り及び負傷動物等の収容並びに処分の状況」より"
const messageThird = "誰か 見かけませんでしたか？"
const cursorFilePath = "/static/image/cursor3.png"
const foundPetFilePath = "/static/image/found_pet.png"
const logoFilePath = "/static/image/logo2.png"

const windowWidth = window.innerWidth
const windowHeight = window.innerHeight
const windowSizeTAB = 800
const windowSizeSP = 420

class pixelObject {
    x = 0
    y = 0
    pixelObject(x, y) {
        this.x = x
        this.y = y
    }
    translateString() {
        return "(" + this.x + "px" + "," + this.y + "px)"
    }
}

// カーソルアニメーションの動きを乱数で作成
function makeRandomPixel() {
    let array = []
    for (let i = 0; i < 6; i++) {
        let pixel = new pixelObject()
        if (i == 0) {
            // 「x = y = 乱数生成」としてしまうと動きに規則性が生まれてしまうため、x・yにそれぞれ代入
            pixel.x = Math.random() * 100 * 10
            pixel.y = Math.random() * 100 * 5
        } else if (i % 2 == 0) {
            pixel.x = Math.random() * 100 * (i + 2) * 2
            pixel.y = Math.random() * 100 * (i + 2)
        } else if (i % 2 == 1) {
            pixel.x = Math.random() * 100 * i * 2
            pixel.y = Math.random() * 100 * i
        }
        array[i] = pixel
    }
    return array
}

// 乱数生成時、画面外へのアニメーションはみ出し防止
function compressionIntoWindow(randomPixel, imgWidth, imgHeight) {
    let maxWidth = window.innerWidth - imgWidth
    let maxHeight = window.innerHeight - imgHeight
    for (let i = 0; i < randomPixel.length; ++i) {
        if (randomPixel[i].x > maxWidth) { randomPixel[i].x = maxWidth }
        if (randomPixel[i].y > maxHeight) { randomPixel[i].y = maxHeight }
    }
    return randomPixel
}

// アニメーション終了時 / キャンセル時 画面上部のボタンを作成
function makeButton() {
    document.body.insertAdjacentHTML('beforeend', "<div id='button-area'></div>")
    const buttonArea = document.querySelector('#button-area')
    buttonArea.insertAdjacentHTML('beforeend', "<div class='login-button'><a href='/owner/login'>ログイン</a></div>")
    buttonArea.insertAdjacentHTML('beforeend', "<div class='signup-button'><a href='/owner/registration'>登録</a></div>")
}

// randomPixelは複数スコープに跨るため、グローバル変数で作成
var randomPixel = []
randomPixel = makeRandomPixel()

document.addEventListener("DOMContentLoaded", function () {

    let timer = 10000
    const slideTitle = document.querySelector('#message-area')

    function firstAnimation() {
        slideTitle.classList.remove("animate-title-first")
        slideTitle.classList.add("animate-title-second")
        slideTitle.innerHTML = "<p class='string-second'>" + messageSecond + "</p>"
    }

    // TODO firstのアニメーションは意味ない可能性あり
    const animationInstance = setTimeout(firstAnimation, timer)

    function secondAnimation() {
        slideTitle.classList.remove("animate-title-second")
        slideTitle.classList.add("animate-title-third")
        slideTitle.innerHTML = "<h2 class='string-third'>" + messageThird + "</h2>"
    }
    const animationInstance2 = setTimeout(secondAnimation, timer + 7000)

    function thirdAnimation() {
        slideTitle.classList.remove("animate-title-second")
        slideTitle.classList.add("animate-title-third")
        slideTitle.innerHTML = "<img class='search-cursor' src='" + cursorFilePath + "'>"

        slideTitle.remove()
        document.querySelector('#container').remove()
        document.body.innerHTML = "<img class='search-cursor' src='" + cursorFilePath + "'>"
        const cursor = document.querySelector('.search-cursor')

        cursor.addEventListener('load', (e) => {
            let imgWidth = e.target.width
            let imgHeight = e.target.height

            randomPixel = compressionIntoWindow(randomPixel, imgWidth, imgHeight)
            cursor.animate(
                {
                    opacity: [1, 0],
                    // opacity: 1,
                    transform: [
                        "translate" + randomPixel[0].translateString(),
                        "translate" + randomPixel[1].translateString(),
                        "translate" + randomPixel[2].translateString(),
                        "translate" + randomPixel[3].translateString(),
                        "translate" + randomPixel[4].translateString(),
                        "translate" + randomPixel[5].translateString()
                    ]
                },
                {
                    //持続時間を乱数を使って設定
                    duration: 4000,
                    direction: 'alternate',
                    fill: 'forwards',
                    easing: 'ease-in-out'
                }
            )
        })
    }
    const animationInstance3 = setTimeout(thirdAnimation, timer + 11000)

    // !!!アイコンの表示座標
    let stringX = ""
    let stringY = ""
    // カーソルアニメーション 最終モーションでのpixelObject(座標)
    let lastRandomPixel = randomPixel.slice(-1)[0]

    function fourthAnimation() {
        document.body.innerHTML = "<div class='fontAwesome'><i class='fa-solid fa-exclamation fa-5x fa-bounce'></i><i class='fa-solid fa-exclamation fa-5x fa-bounce'></i><i class='fa-solid fa-exclamation fa-5x fa-bounce'></i></div>"
        const exclamation = document.querySelector('.fontAwesome')

        if (lastRandomPixel.x > 330) {
            lastRandomPixel.x = 330
        }
        stringX = String(lastRandomPixel.x) + 'px'
        stringY = String(lastRandomPixel.y) + 'px'
        exclamation.style.paddingTop = stringY
        exclamation.style.paddingLeft = stringX
        exclamation.style.color = "white"
    }
    const animationInstance4 = setTimeout(fourthAnimation, timer + 15000)

    // ペット発見アイコン
    let foundPet = ""

    // 画面中央の座標(アニメーション後、中央への移動 / キャンセル時に利用)
    let windowCenterX = windowWidth / 2
    let windowCenterY = windowHeight / 2

    function fifthAnimation() {
        document.body.innerHTML = ""
        document.body.innerHTML = "<div id='title-area'><img class='found-pet' src='" + foundPetFilePath + "'></div>"
        foundPet = document.querySelector('.found-pet')
        foundPet.style.paddingTop = stringY
        foundPet.style.paddingLeft = stringX
    }
    const animationInstance5 = setTimeout(fifthAnimation, timer + 16000)

    function sixthAnimation() {

        // レスポンシブ対応(SP)
        if (windowSizeSP > windowWidth) { windowCenterX += 40 }

        let absoluteAddressX = windowCenterX - foundPet.width - foundPet.style.paddingLeft.replace("px", "")
        let absoluteAddressY = windowCenterY - foundPet.height - foundPet.style.paddingTop.replace("px", "")

        foundPet.animate(
            {
                transform: "translate(" + absoluteAddressX + "px" + "," + absoluteAddressY + "px)"
            },
            {
                duration: 1500,
                direction: 'alternate',
                fill: 'forwards',
                easing: 'ease-in-out'
            }
        )
    }
    const animationInstance6 = setTimeout(sixthAnimation, timer + 17000)

    function seventhAnimation() {
        let afterMovingImg = document.querySelector('.found-pet')
        afterMovingImg.classList.remove('found-pet')
        afterMovingImg.setAttribute("id", "logo")
        afterMovingImg.src = logoFilePath
        makeButton()
    }
    const animationInstance7 = setTimeout(seventhAnimation, timer + 19000)

    // アニメーションキャンセル
    function animationCancel() {
        clearTimeout(animationInstance)
        clearTimeout(animationInstance2)
        clearTimeout(animationInstance3)
        clearTimeout(animationInstance4)
        clearTimeout(animationInstance5)
        clearTimeout(animationInstance6)
        clearTimeout(animationInstance7)

        document.body.innerHTML = "<img id='after-cancel' src='" + logoFilePath + "'>"
        const afterCancel = document.querySelector('#after-cancel')

        afterCancel.addEventListener('load', (e) => {

            let afterCancelWidth = e.target.width
            let afterCancelHeight = e.target.width
            if (windowSizeSP > windowWidth) {
                e.target.style.width = "30%"
                afterCancelWidth = afterCancelWidth / 3
                afterCancelHeight = e.target.height / 2
            } else if (windowSizeTAB > windowWidth && windowWidth > windowSizeSP) {
                e.target.style.width = "25%"
                afterCancelWidth = afterCancelWidth / 2
                afterCancelHeight = afterCancelHeight / 2
            } else {
                e.target.style.width = "10%"
                afterCancelWidth = afterCancelWidth
                afterCancelHeight = afterCancelHeight
            }
            afterCancel.style.paddingLeft = (windowCenterX - afterCancelWidth) + "px"
            afterCancel.style.paddingTop = (windowCenterY - afterCancelHeight) + "px"
            afterCancel.style.position = "absolute"
        })
        makeButton()
    }
    const canceller = document.querySelector('#animation-cancel')
    canceller.addEventListener('click', animationCancel)

})

