
function clear_button() {
    var botoes = document.querySelectorAll('input[type="radio"]');
    for(var i=0; i<botoes.length; i++) {
    botoes[i].checked = false;
    }
    var infoDiv = document.getElementById('info-container');
    infoDiv.innerHTML = '';
}

var selectedOptions = {};
var opcoes = document.querySelectorAll('input[type="radio"]');
opcoes.forEach(function(opcao) {
    opcao.addEventListener('change', function() {
    // get the name of the match
    var matchName = this.name;

    // remove any previously selected options for this match
    if (selectedOptions[matchName]) {
        selectedOptions[matchName].forEach(function(selectedOption) {
        selectedOption.checked = false;
        });
        delete selectedOptions[matchName];
    }

    // add the selected option to the selectedOptions object
    selectedOptions[matchName] = [this];

    // initialize the message for all matches
    var mensagem = '';
    for (var match in selectedOptions) {
        mensagem += '<h3>' + match + '</h3>';
        selectedOptions[match].forEach(function(selectedOption) {
        var valor = selectedOption.value;
        var partes = valor.split(",");
        var odds = partes[0];
        var resultado = partes[1];
        mensagem += '<p>Você selecionou ' + resultado + ' com odds de ' + odds + '</p>';
        });
    }

    // update the box on the right side of the page with the message for all matches
    var infoDiv = document.getElementById('info-container');
    infoDiv.innerHTML = mensagem;
    });
});


function toggleDiv() {
    var button = document.getElementById('button_show');
    var div = document.getElementById('info-container');
    
    if (div.style.display === "none") {
        button.textContent = '-';
        div.style.display = "block";
      } else {
        div.style.display = "none";
        button.textContent = '+';
      }
    }
    