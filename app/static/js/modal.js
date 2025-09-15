// Pega os elementos
const modal = document.getElementById("myModal");
const btn = document.getElementById("openModal");
const span = document.getElementById("closeModal");
const cancel = document.getElementById("cancelModal")

// Quando clicar no botão, abre o modal
btn.onclick = function () {
    modal.style.display = "flex";
}

// Quando clicar no X, fecha o modal
span.onclick = function () {
    modal.style.display = "none";
}

cancel.onclick = function () {
    modal.style.display = "none";
}

// Quando clicar fora da caixa, também fecha
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}