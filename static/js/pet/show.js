document.addEventListener("DOMContentLoaded", function () {
    const showEventTimes = document.body.querySelectorAll(".show-eventTime");
    showEventTimes.forEach(function (showEventTime) {
        showEventTime.innerText = showEventTime.innerText.substring(0, 16);
    });
});