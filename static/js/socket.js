const socket = io();

// Ao conectar, envia dados do usuário para registrar presença
socket.on('connect', () => {
    console.log('[SocketIO] Conectado ao servidor SocketIO');
    if (window.usuarioAtual && window.usuarioId) {
        console.log('[SocketIO] Emitindo usuario_logado:', window.usuarioAtual, window.usuarioId);
        socket.emit('usuario_logado', {
            user_id: window.usuarioId,
            nome: window.usuarioAtual
        });
    } else {
        console.warn('[SocketIO] Vari\u00e1veis usuarioAtual ou usuarioId n\u00e3o est\u00e3o definidas.');
    }
});

// Recebe confirma\u00e7\u00e3o do servidor de que o usu\u00e1rio entrou na sala
socket.on('usuario_logado_confirmado', (data) => {
    console.log('[SocketIO] Confirma\u00e7\u00e3o recebida:', data);
});

// Recebe nova rolagem de dados e atualiza o log
socket.on('nova_rolagem', (data) => {
    console.log('[SocketIO] nova_rolagem recebida:', data);
    const log = document.getElementById('log-rolagens');
    if (!log) return;
    const item = document.createElement('li');
    const detalhes = data.rolagens ? data.rolagens.join(', ') : '?';
    const texto = `${data.jogador} rolou ${data.pericia}: ${data.total} (${data.expressao}) [${detalhes}]`;
    item.textContent = texto;
    log.prepend(item);
});

// Atualiza lista de usu\u00e1rios online (para o painel do mestre)
socket.on('usuarios_online', (usuarios) => {
    console.log('[SocketIO] Lista de usu\u00e1rios online recebida:', usuarios);
    const lista = document.getElementById('lista-jogadores-online');
    if (!lista) return;
    lista.innerHTML = '';
    usuarios.forEach(user => {
        if (user.user_id === String(window.usuarioId)) return; // Não mostra o pr\u00f3prio usu\u00e1rio
        const li = document.createElement('li');
        li.textContent = user.nome + " ";
        const btn = document.createElement('button');
        btn.textContent = "Convidar";
        btn.onclick = () => {
            console.log(`[SocketIO] Enviando convite para o jogador ID ${user.user_id} para campanha ${window.campanhaAtualId}`);
            socket.emit('convidar_para_campanha', {
                user_id: user.user_id,
                campanha_id: window.campanhaAtualId
            });
        };
        li.appendChild(btn);
        lista.appendChild(li);
    });
});

// Recebe convite de campanha e solicita confirma\u00e7\u00e3o para aceitar
socket.on('convite_recebido', (data) => {
    console.log('[SocketIO] convite_recebido recebido:', data);
    const confirmacao = confirm(data.mensagem + "\nDeseja entrar agora?");
    if (confirmacao && data.campanha_id) {
        console.log('[SocketIO] Usu\u00e1rio aceitou o convite. Emitindo aceitar_convite...');
        socket.emit('aceitar_convite', {
            campanha_id: data.campanha_id,
            user_id: window.usuarioId
        });
    } else {
        console.log('[SocketIO] Convite recusado ou n\u00e3o aceito.');
    }
});

// Recebe confirma\u00e7\u00e3o de convite aceito e redireciona
socket.on('convite_aceito', (data) => {
    console.log('[SocketIO] convite_aceito recebido:', data);
    if (data.campanha_id) {
        console.log('[SocketIO] Redirecionando para campanha:', data.campanha_id);
        window.location.href = `/campanha/${data.campanha_id}`;
    }
});
