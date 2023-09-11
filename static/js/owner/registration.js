const goToTop = (event) => {

    let name = document.body.querySelector("#name").value
    let password = document.body.querySelector("#password").value
    let userName = document.body.querySelector("#username").value
    let message = document.body.querySelector("#message").value
    let contact = document.body.querySelector("#contact").value

    // 入力欄に1箇所でも記入がある場合、入力破棄のアラートを表示
    if (!(!name && !password && !userName && !message && !contact)) {
        const confirm = window.confirm("入力を破棄し、TOP画面に移動します")
        if (!confirm) {
            event.stopPropagation();
            event.preventDefault();
        }
    }

}


document.addEventListener("DOMContentLoaded", function () {
    let topButton = document.body.querySelector(".top-button")
    topButton.addEventListener('submit', goToTop)
})