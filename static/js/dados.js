/**
 * Essa função calcula o modificador a partir de um valor base.
 * Fórmula: Math.floor((valor - 10) / 2)
 */
function obterModificador(valor) {
    return Math.floor((valor - 10) / 2);
}

/**
 * Função para rolar os dados com base nos menus dropdown.
 * Lê os valores de quantidade, tipo e modificador, monta uma expressão (ex: "2d6+3")
 * e emite o evento 'roll' para o servidor.
 */
function rolarMenu() {
    const quantidadeSelect = document.getElementById('quantidade-dados');
    const tipoSelect = document.getElementById('tipo-dado');
    const modSelect = document.getElementById('modificador');

    if (!quantidadeSelect || !tipoSelect || !modSelect) {
        alert("Erro: Um ou mais campos de rolagem não foram encontrados.");
        return;
    }

    const quantidade = quantidadeSelect.value;
    const faces = tipoSelect.value;
    const modificador = modSelect.value;

    // Monta a expressão, por exemplo, "2d6+3" ou "2d6-1"
    let expressao = `${quantidade}d${faces}`;
    const modInt = parseInt(modificador, 10);
    if (modInt > 0) {
        expressao += `+${modInt}`;
    } else if (modInt < 0) {
        expressao += `${modInt}`; // O sinal já está embutido
    }
    console.log("[Dados] Expressão formada:", expressao);

    // Emite o evento de rolagem para o servidor via SocketIO
    socket.emit('roll', {
        user: window.usuarioAtual,
        pericia: 'Custom (Menu)',
        expression: expressao
    });
}
