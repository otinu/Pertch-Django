
const getAddress = function (input) {
    const api = 'https://zipcloud.ibsnet.co.jp/api/search?zipcode=';
    const inputValue = input.target.value;
    let url = api + inputValue;
    const address = document.querySelector('#address');

    fetchJsonp(url, {
        timeout: 10000
    })
        .then((response) => {
            // error.textContent = '';
            return response.json();
        })
        .then((data) => {
            if (data.status === 400) {
                if (inputValue.length == 0) {
                    address.value = "";
                }

                if (inputValue.length == 7) {
                    console.log(data.message);
                }
            } else if (data.results === null && inputValue.length == 7) {
                alert('郵便番号から住所が見つかりませんでした')
            } else {
                const prefecture = data.results[0].address1;
                const city = data.results[0].address2;
                const town = data.results[0].address3;
                address.value = prefecture + city + town;
            }
        })
        .catch((e) => {
            if (inputValue.length == 7) {
                console.log(e);
            }
        });
}