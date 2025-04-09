function obterModificador(valor) {
    return Math.floor((valor - 10) / 2);
}

function rolarComAtributo(atributoNome, valorBase) {
    const mod = obterModificador(valorBase);
    const sinal = mod >= 0 ? '+' : '';
    const expressao = `1d20${sinal}${mod}`;
    socket.emit('roll', {
        user: usuarioAtual,
        pericia: atributoNome,
        expression: expressao
    });
}
