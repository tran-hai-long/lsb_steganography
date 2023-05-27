document.addEventListener('DOMContentLoaded', () => {
    document.querySelector("#submit-button").addEventListener('click', () => {
        let formData = new FormData(document.querySelector("form"));
        fetch("/prng/decode", {
            method: 'POST',
            body: formData
        }).then((response) => {
            return response.text();
        }).then((data) => {
            document.querySelector("#result-msg").innerHTML = data;
        });
    });
});
