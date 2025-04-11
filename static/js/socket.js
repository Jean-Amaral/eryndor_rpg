const socket = io();

// Ao conectar, envia dados do usuário para o servidor
socket.on('connect', () => {
    console.log('[SocketIO] Conectado ao servidor. Socket ID:', socket.id);
    if (window.usuarioAtual && window.usuarioId) {
        console.log('[SocketIO] Emitindo usuario_logado:', window.usuarioAtual, window.usuarioId);
        socket.emit('usuario_logado', {
            user_id: window.usuarioId,
            nome: window.usuarioAtual
        });
    } else {
        console.warn('[SocketIO] Vari\u00e1veis usuarioAtual ou usuarioId n\u00e3o definidas.');
    }
});

// Confirma\u00e7\u00e3o do servidor
socket.on('usuario_logado_confirmado', (data) => {
    console.log('[SocketIO] Confirma\u00e7\u00e3o recebida:', data);
});

// Atualiza a lista de usu\u00e1rios online
socket.on('usuarios_online', (usuarios) => {
    console.log('[SocketIO] Lista de usu\u00e1rios online:', usuarios);
    const lista = document.getElementById('lista-jogadores-online');
    if (!lista) {
        console.warn('[SocketIO] Elemento "lista-jogadores-online" n\u00e3o encontrado.');
        return;
    }
    lista.innerHTML = '';
    usuarios.forEach(user => {
        if (user.user_id === String(window.usuarioId)) return; // Não exibe o pr\u00f3prio usu\u00e1rio
        const li = document.createElement('li');
        li.textContent = user.nome + " ";
        const btn = document.createElement('button');
        btn.textContent = "Convidar";
        btn.onclick = () => {
            console.log(`[SocketIO] Enviando convite para jogador ID ${user.user_id} para campanha ${window.campanhaAtualId}`);
            socket.emit('convidar_para_campanha', {
                user_id: user.user_id,
                campanha_id: window.campanhaAtualId
            });
        };
        li.appendChild(btn);
        lista.appendChild(li);
    });
});

// Recebe o convite e solicita confirma\u00e7\u00e3o para aceitar
socket.on('convite_recebido', (data) => {
    console.log('[SocketIO] Convite recebido:', data);
    const confirmacao = confirm(data.mensagem + "\nDeseja entrar agora?");
    if (confirmacao && data.campanha_id) {
        console.log('[SocketIO] Usu\u00e1rio aceitou o convite. Emitindo aceitar_convite...');
        socket.emit('aceitar_convite', {
            campanha_id: data.campanha_id,
            user_id: window.usuarioId
        });
    } else {
        console.log('[SocketIO] Convite recusado ou cancelado.');
    }
});

// Redireciona conforme a resposta de convite aceito
socket.on('convite_aceito', (data) => {
    console.log('[SocketIO] Convite aceito recebido:', data);
    if (data.campanha_id) {
        if (data.rota === 'selecionar_heroi') {
            console.log('[SocketIO] Redirecionando para sele\u00e7\u00e3o de her\u00f3i:', data.campanha_id);
            window.location.href = `/selecionar_heroi/${data.campanha_id}`;
        } else {
            console.log('[SocketIO] Redirecionando para campanha:', data.campanha_id);
            window.location.href = `/campanha/${data.campanha_id}`;
        }
    }
});

// Recebe nova rolagem e atualiza o log de rolagens
socket.on('nova_rolagem', (data) => {
    console.log('[SocketIO] Nova rolagem recebida:', data);
    const log = document.getElementById('log-rolagens');
    if (!log) return;
    const item = document.createElement('li');
    const detalhes = data.rolagens ? data.rolagens.join(', ') : '?';
    item.textContent = `${data.jogador} rolou ${data.pericia}: ${data.total} (${data.expressao}) [${detalhes}]`;
    log.prepend(item);
});
