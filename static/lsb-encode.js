document.addEventListener('DOMContentLoaded', () => {
    document.querySelector("#submit-button").addEventListener('click', () => {
        let formData = new FormData(document.querySelector("form"));
        fetch("/lsb/encode", {
            method: 'POST',
            body: formData
        }).then((response) => {
            return response.text();
        }).then((data) => {
            document.querySelector("#result-img").src = "data:image/png;base64," + data;
        });
    });
});
