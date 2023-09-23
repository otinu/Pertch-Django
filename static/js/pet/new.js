const file = document.body.querySelector('[name="upload_file"]');
let uploadFile = document.body.querySelector("[name='upload_file']").files
let fileLabel = document.body.querySelector(".file-label");
let cancelButton;

function changeFileForm() {
    return new Promise((resolve) => {
        file.addEventListener('change', () => {
            let tmpUploadFile = file
            fileLabel.nextElementSibling.innerHTML = fileLabel.nextElementSibling.innerHTML.replace("未選択", "<i class='fa-solid fa-circle-xmark' style='color: deeppink;'></i>選択済");
            fileLabel.append(tmpUploadFile);

            cancelButton = document.body.querySelector(".fa-circle-xmark");
            resolve(cancelButton)
        })
    });
}

file.addEventListener('click', () => {
    changeFileForm().then((cancelButton) => {
        cancelButton.addEventListener('click', () => {
            file.value = "";
            fileLabel.nextElementSibling.innerHTML = "&nbsp;未選択"
        })
    })
})

document.addEventListener("DOMContentLoaded", function () {
    const postCord = document.querySelector('#post-cord');
    // postCordAPI.jsのメソッド呼び出し
    postCord.addEventListener('input', getAddress);
})