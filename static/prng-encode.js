document.addEventListener('DOMContentLoaded', () => {
    document.querySelector("#submit-button").addEventListener('click', () => {
        let formData = new FormData(document.querySelector("form"));
        fetch("/prng/encode", {
            method: 'POST',
            body: formData
        }).then((response) => {
            return response.json();
        }).then((data) => {
            document.querySelector("#result-seed").innerHTML = data["result-seed"]
            document.querySelector("#result-img").src = "data:image/png;base64," + data["result-img"];
        });
    });
});
