document.getElementById("avatar").addEventListener("click", function () {
    document.getElementById("avatar-input").click();
});

document.getElementById("avatar-input").addEventListener("change", function () {
    document.getElementById("avatar-form").submit();
});