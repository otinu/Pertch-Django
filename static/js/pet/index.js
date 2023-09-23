const deleteAlert = function (event) {
    const confirm = window.confirm("削除します。\n内容をご確認ください。")
    if (!confirm) {
        event.stopPropagation();
        event.preventDefault();
    }
}

document.addEventListener("DOMContentLoaded", function () {

    const deleteButtons = document.body.querySelectorAll("#deleteBtn");

    // HTML 要素に対して、イベントのハンドラー関数を登録する
    deleteButtons.forEach(function (deleteButton) {
        deleteButton.addEventListener('click', deleteAlert);
    });

    const petShows = document.body.querySelectorAll('#pet-show');
    petShows.forEach(function (petShow) {
        petShow.addEventListener('click', () => { petShow.submit() });
    });

    const postCord = document.querySelector('#post-cord');
    // postCordAPI.jsのメソッド呼び出し
    postCord.addEventListener('input', getAddress);

    // 特徴が長文の場合は割愛して表示
    let tdArray = document.querySelector('#index-tbody').children;
    for (td of tdArray) {
        let charmPoint = td.children[3].innerHTML;
        if (charmPoint.length > 100) {
            td.children[3].innerHTML = charmPoint.slice(0, 100) + '……';
        }
    }

})