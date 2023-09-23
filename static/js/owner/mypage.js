const deleteAlert = function (event) {
    const confirm = window.confirm("Pertchから退会します")
    if (!confirm) {
        event.stopPropagation();
        event.preventDefault();
    }
}

document.addEventListener("DOMContentLoaded", function () {

    const deleteButton = document.body.querySelector(".deleteBtn");
    deleteButton.addEventListener('click', deleteAlert);
});