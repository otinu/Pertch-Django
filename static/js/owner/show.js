document.addEventListener("DOMContentLoaded", function () {
    const petShows = document.body.querySelectorAll('#pet-img');
    petShows.forEach(function (petShow) {
        petShow.addEventListener('click', () => {
            petShow.submit()
        });
    });
});