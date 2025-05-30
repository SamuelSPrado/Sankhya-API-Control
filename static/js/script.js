// Script para integração com backend e manipulação da interface

document.addEventListener('DOMContentLoaded', function() {
    // Elementos do DOM
    const sidebar = document.getElementById('sidebar');
    const content = document.getElementById('content');
    const sidebarCollapse = document.getElementById('sidebarCollapse');
    const pageTitle = document.getElementById('page-title');
    const menuItems = document.querySelectorAll('#sidebar ul li a');
    const sections = document.querySelectorAll('.content-section');
    const toast = document.getElementById('toast');
    const toastTitle = document.getElementById('toastTitle');
    const toastMessage = document.getElementById('toastMessage');
    const toastIcon = document.getElementById('toastIcon');
    const closeToast = document.querySelector('.toast .close');

    // Elementos da seção de Reprocessamento de Pedidos
    const pedidoId = document.getElementById('pedidoId');
    const btnValidarPedido = document.getElementById('btnValidarPedido');
    const btnReprocessarPedido = document.getElementById('btnReprocessarPedido');
    const btnLimparPedido = document.getElementById('btnLimparPedido');
    const statusCodeResult = document.getElementById('statusCodeResult');
    const databaseResult = document.getElementById('databaseResult');
    const pedidoTable = document.getElementById('pedidoTable');

    // Elementos da seção de Importação de Produtos
    const produtoId = document.getElementById('produtoId');
    const btnImportarProduto = document.getElementById('btnImportarProduto');
    const btnLimparProduto = document.getElementById('btnLimparProduto');
    const produtoStatusCode = document.getElementById('produtoStatusCode');
    const produtoCode = document.getElementById('produtoCode');
    const produtoDescription = document.getElementById('produtoDescription');

    // Elementos da seção de Validação de Caixa
    const localId = document.getElementById('localId');
    const caixaId = document.getElementById('caixaId');
    const btnConsultarCaixa = document.getElementById('btnConsultarCaixa');
    const btnLimparCaixa = document.getElementById('btnLimparCaixa');
    
    // Informações do Caixa
    const portalMeep = document.getElementById('portalMeep');
    const dataInicial = document.getElementById('dataInicial');
    const dataFinal = document.getElementById('dataFinal');
    
    // Invoice Order
    const invoiceCredito = document.getElementById('invoiceCredito');
    const invoiceDebito = document.getElementById('invoiceDebito');
    const invoiceDinheiro = document.getElementById('invoiceDinheiro');
    const invoiceOutros = document.getElementById('invoiceOutros');
    const invoiceDesconto = document.getElementById('invoiceDesconto');
    const invoiceTotal = document.getElementById('invoiceTotal');
    
    // Transação Offline
    const offlineCredito = document.getElementById('offlineCredito');
    const offlineDebito = document.getElementById('offlineDebito');
    const offlineDinheiro = document.getElementById('offlineDinheiro');
    const offlineOutros = document.getElementById('offlineOutros');
    const offlineDesconto = document.getElementById('offlineDesconto');
    const offlineTotal = document.getElementById('offlineTotal');
    
    // Transação POS
    const posCredito = document.getElementById('posCredito');
    const posDebito = document.getElementById('posDebito');
    const posDinheiro = document.getElementById('posDinheiro');
    const posOutros = document.getElementById('posOutros');
    const posDesconto = document.getElementById('posDesconto');
    const posTotal = document.getElementById('posTotal');
    
    // Sankhya (Entrada Manual)
    const sankhyaCredito = document.getElementById('sankhyaCredito');
    const sankhyaDebito = document.getElementById('sankhyaDebito');
    const sankhyaDinheiro = document.getElementById('sankhyaDinheiro');
    const sankhyaOutros = document.getElementById('sankhyaOutros');
    const sankhyaDesconto = document.getElementById('sankhyaDesconto');
    const sankhyaTotal = document.getElementById('sankhyaTotal');
    
    // Botões de Diferença
    const btnDiferencaInvoice = document.getElementById('btnDiferencaInvoice');
    const btnDiferencaOffline = document.getElementById('btnDiferencaOffline');
    const btnDiferencaPos = document.getElementById('btnDiferencaPos');
    
    // Diferença
    const difCredito = document.getElementById('difCredito');
    const difDebito = document.getElementById('difDebito');
    const difDinheiro = document.getElementById('difDinheiro');
    const difOutros = document.getElementById('difOutros');
    const difDesconto = document.getElementById('difDesconto');
    const difTotal = document.getElementById('difTotal');

    // Variáveis para armazenar dados
    let dadosInvoiceOrder = {};
    let dadosTransacaoOffline = {};
    let dadosTransacaoPos = {};

    // Funções de Utilidade
    function showToast(title, message, type = 'info') {
        toastTitle.textContent = title;
        toastMessage.textContent = message;
        
        // Definir ícone com base no tipo
        if (type === 'success') {
            toastIcon.className = 'fas fa-check-circle';
            toastIcon.style.color = '#1cc88a';
        } else if (type === 'error') {
            toastIcon.className = 'fas fa-exclamation-circle';
            toastIcon.style.color = '#e74a3b';
        } else if (type === 'warning') {
            toastIcon.className = 'fas fa-exclamation-triangle';
            toastIcon.style.color = '#f6c23e';
        } else {
            toastIcon.className = 'fas fa-info-circle';
            toastIcon.style.color = '#4e73df';
        }
        
        toast.classList.add('active');
        
        // Remover toast após 5 segundos
        setTimeout(() => {
            toast.classList.remove('active');
        }, 5000);
    }

    function limparCamposDiferenca() {
        difCredito.textContent = '';
        difDebito.textContent = '';
        difDinheiro.textContent = '';
        difOutros.textContent = '';
        difDesconto.textContent = '';
        difTotal.textContent = '';
    }

    // Eventos de navegação
    sidebarCollapse.addEventListener('click', () => {
        sidebar.classList.toggle('active');
        content.classList.toggle('active');
    });

    menuItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Atualizar menu ativo
            menuItems.forEach(i => i.parentElement.classList.remove('active'));
            this.parentElement.classList.add('active');
            
            // Mostrar seção correspondente
            const targetSection = this.getAttribute('data-section');
            sections.forEach(section => {
                section.classList.remove('active');
                if (section.id === targetSection) {
                    section.classList.add('active');
                    pageTitle.textContent = this.textContent.trim();
                }
            });
        });
    });

    closeToast.addEventListener('click', () => {
        toast.classList.remove('active');
    });

    // Eventos da seção de Reprocessamento de Pedidos
    btnValidarPedido.addEventListener('click', async () => {
        const id = pedidoId.value.trim();
        if (!id) {
            showToast('Erro', 'Por favor, informe o ID do pedido.', 'error');
            return;
        }

        try {
            const response = await fetch('/api/pedido/consultar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ pedido_id: id })
            });

            const data = await response.json();

            if (data.success) {
                // Limpar tabela
                const tbody = pedidoTable.querySelector('tbody');
                tbody.innerHTML = '';

                // Preencher tabela com resultados
                if (data.data && data.data.length > 0) {
                    data.data.forEach(row => {
                        const tr = document.createElement('tr');
                        tr.innerHTML = `
                            <td>${row.SANKHYAID || 'NULL'}</td>
                            <td>${row.DISCOUNT || '0.00'}</td>
                            <td>${row.VALUE || '0.00'}</td>
                            <td>${row.ORDERDATE || ''}</td>
                            <td>${row.ERRORMESSAGE || ''}</td>
                            <td>${row.DATE || ''}</td>
                        `;
                        tbody.appendChild(tr);
                    });
                    showToast('Sucesso', 'Consulta realizada com sucesso.', 'success');
                } else {
                    tbody.innerHTML = '<tr><td colspan="6">Nenhum resultado encontrado.</td></tr>';
                    showToast('Aviso', 'Nenhum resultado encontrado para este pedido.', 'warning');
                }
            } else {
                showToast('Erro', data.error || 'Erro ao consultar pedido.', 'error');
            }
        } catch (error) {
            console.error('Erro ao consultar pedido:', error);
            showToast('Erro', 'Falha ao comunicar com o servidor.', 'error');
        }
    });

    btnReprocessarPedido.addEventListener('click', async () => {
        const id = pedidoId.value.trim();
        if (!id) {
            showToast('Erro', 'Por favor, informe o ID do pedido.', 'error');
            return;
        }

        try {
            const response = await fetch('/api/pedido/reprocessar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ pedido_id: id })
            });

            const data = await response.json();

            if (data.success) {
                statusCodeResult.textContent = `${data.status_code} OK`;
                statusCodeResult.classList.add('positive');
                showToast('Sucesso', 'Pedido reprocessado com sucesso.', 'success');
            } else {
                statusCodeResult.textContent = `${data.status_code} ${data.message}`;
                statusCodeResult.classList.add('negative');
                showToast('Erro', data.message || 'Erro ao reprocessar pedido.', 'error');
            }
        } catch (error) {
            console.error('Erro ao reprocessar pedido:', error);
            showToast('Erro', 'Falha ao comunicar com o servidor.', 'error');
        }
    });

    btnLimparPedido.addEventListener('click', () => {
        pedidoId.value = '';
        statusCodeResult.textContent = '';
        statusCodeResult.classList.remove('positive', 'negative');
        
        const tbody = pedidoTable.querySelector('tbody');
        tbody.innerHTML = '';
        
        showToast('Info', 'Campos limpos com sucesso.', 'info');
    });

    // Eventos da seção de Importação de Produtos
    btnImportarProduto.addEventListener('click', async () => {
        const id = produtoId.value.trim();
        if (!id) {
            showToast('Erro', 'Por favor, informe o ID do produto.', 'error');
            return;
        }

        try {
            const response = await fetch('/api/produto/importar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ produto_id: id })
            });

            const data = await response.json();

            if (data.success) {
                produtoStatusCode.textContent = `${data.status_code} OK`;
                produtoCode.textContent = data.product_code;
                produtoDescription.textContent = data.description;
                
                produtoStatusCode.classList.add('positive');
                showToast('Sucesso', 'Produto importado com sucesso.', 'success');
            } else {
                produtoStatusCode.textContent = `${data.status_code} ${data.message}`;
                produtoCode.textContent = '';
                produtoDescription.textContent = '';
                
                produtoStatusCode.classList.add('negative');
                showToast('Erro', data.message || 'Erro ao importar produto.', 'error');
            }
        } catch (error) {
            console.error('Erro ao importar produto:', error);
            showToast('Erro', 'Falha ao comunicar com o servidor.', 'error');
        }
    });

    btnLimparProduto.addEventListener('click', () => {
        produtoId.value = '';
        produtoStatusCode.textContent = '';
        produtoCode.textContent = '';
        produtoDescription.textContent = '';
        
        produtoStatusCode.classList.remove('positive', 'negative');
        
        showToast('Info', 'Campos limpos com sucesso.', 'info');
    });

    // Eventos da seção de Validação de Caixa
    btnConsultarCaixa.addEventListener('click', async () => {
        const local = localId.value.trim();
        const caixa = caixaId.value.trim();
        
        if (!local || !caixa) {
            showToast('Erro', 'Por favor, informe LOCAL_ID e CAIXA_ID.', 'error');
            return;
        }

        try {
            const response = await fetch('/api/caixa/consultar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ local_id: local, caixa_id: caixa })
            });

            const data = await response.json();

            if (data.success) {
                // Preencher informações do caixa
                portalMeep.textContent = data.info_caixa.portal_meep;
                dataInicial.textContent = data.info_caixa.data_inicial;
                dataFinal.textContent = data.info_caixa.data_final;
                
                // Preencher Invoice Order
                invoiceCredito.textContent = data.invoice_order.credito;
                invoiceDebito.textContent = data.invoice_order.debito;
                invoiceDinheiro.textContent = data.invoice_order.dinheiro;
                invoiceOutros.textContent = data.invoice_order.outros;
                invoiceDesconto.textContent = data.invoice_order.desconto;
                invoiceTotal.textContent = data.invoice_order.total;
                
                // Preencher Transação Offline
                offlineCredito.textContent = data.transacao_offline.credito;
                offlineDebito.textContent = data.transacao_offline.debito;
                offlineDinheiro.textContent = data.transacao_offline.dinheiro;
                offlineOutros.textContent = data.transacao_offline.outros;
                offlineDesconto.textContent = data.transacao_offline.desconto;
                offlineTotal.textContent = data.transacao_offline.total;
                
                // Preencher Transação POS
                posCredito.textContent = data.transacao_pos.credito;
                posDebito.textContent = data.transacao_pos.debito;
                posDinheiro.textContent = data.transacao_pos.dinheiro;
                posOutros.textContent = data.transacao_pos.outros;
                posDesconto.textContent = data.transacao_pos.desconto;
                posTotal.textContent = data.transacao_pos.total;
                
                // Armazenar dados para cálculos posteriores
                dadosInvoiceOrder = data.invoice_order;
                dadosTransacaoOffline = data.transacao_offline;
                dadosTransacaoPos = data.transacao_pos;
                
                // Limpar diferenças
                limparCamposDiferenca();
                
                showToast('Sucesso', 'Consulta realizada com sucesso.', 'success');
            } else {
                showToast('Erro', data.error || 'Erro ao consultar caixa.', 'error');
            }
        } catch (error) {
            console.error('Erro ao consultar caixa:', error);
            showToast('Erro', 'Falha ao comunicar com o servidor.', 'error');
        }
    });

    btnLimparCaixa.addEventListener('click', () => {
        // Limpar campos de entrada
        localId.value = '';
        caixaId.value = '';
        
        // Limpar informações do caixa
        portalMeep.textContent = '';
        dataInicial.textContent = '';
        dataFinal.textContent = '';
        
        // Limpar Invoice Order
        invoiceCredito.textContent = '';
        invoiceDebito.textContent = '';
        invoiceDinheiro.textContent = '';
        invoiceOutros.textContent = '';
        invoiceDesconto.textContent = '';
        invoiceTotal.textContent = '';
        
        // Limpar Transação Offline
        offlineCredito.textContent = '';
        offlineDebito.textContent = '';
        offlineDinheiro.textContent = '';
        offlineOutros.textContent = '';
        offlineDesconto.textContent = '';
        offlineTotal.textContent = '';
        
        // Limpar Transação POS
        posCredito.textContent = '';
        posDebito.textContent = '';
        posDinheiro.textContent = '';
        posOutros.textContent = '';
        posDesconto.textContent = '';
        posTotal.textContent = '';
        
        // Limpar Sankhya
        sankhyaCredito.value = '';
        sankhyaDebito.value = '';
        sankhyaDinheiro.value = '';
        sankhyaOutros.value = '';
        sankhyaDesconto.value = '';
        sankhyaTotal.value = '';
        
        // Limpar diferenças
        limparCamposDiferenca();
        
        // Limpar dados armazenados
        dadosInvoiceOrder = {};
        dadosTransacaoOffline = {};
        dadosTransacaoPos = {};
        
        showToast('Info', 'Campos limpos com sucesso.', 'info');
    });

    // Funções para calcular diferenças
    async function calcularDiferenca(origem) {
        // Obter valores do Sankhya
        const valoresSankhya = {
            credito: sankhyaCredito.value,
            debito: sankhyaDebito.value,
            dinheiro: sankhyaDinheiro.value,
            outros: sankhyaOutros.value,
            desconto: sankhyaDesconto.value,
            total: sankhyaTotal.value
        };
        
        // Verificar se todos os campos do Sankhya estão preenchidos
        const camposVazios = Object.values(valoresSankhya).some(valor => !valor);
        if (camposVazios) {
            showToast('Erro', 'Por favor, preencha todos os campos do Caixa Sankhya.', 'error');
            return;
        }
        
        try {
            const response = await fetch('/api/caixa/calcular-diferenca', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    origem: origem,
                    valores_sankhya: valoresSankhya,
                    invoice_order: dadosInvoiceOrder,
                    transacao_offline: dadosTransacaoOffline,
                    transacao_pos: dadosTransacaoPos
                })
            });

            const data = await response.json();

            if (data.success) {
                // Preencher diferenças
                difCredito.textContent = data.diferencas.credito;
                difDebito.textContent = data.diferencas.debito;
                difDinheiro.textContent = data.diferencas.dinheiro;
                difOutros.textContent = data.diferencas.outros;
                difDesconto.textContent = data.diferencas.desconto;
                difTotal.textContent = data.diferencas.total;
                
                // Aplicar classes para valores positivos e negativos
                aplicarClassesDiferenca(difCredito);
                aplicarClassesDiferenca(difDebito);
                aplicarClassesDiferenca(difDinheiro);
                aplicarClassesDiferenca(difOutros);
                aplicarClassesDiferenca(difDesconto);
                aplicarClassesDiferenca(difTotal);
                
                showToast('Sucesso', 'Diferença calculada com sucesso.', 'success');
            } else {
                showToast('Erro', data.error || 'Erro ao calcular diferença.', 'error');
            }
        } catch (error) {
            console.error('Erro ao calcular diferença:', error);
            showToast('Erro', 'Falha ao comunicar com o servidor.', 'error');
        }
    }

    function aplicarClassesDiferenca(elemento) {
        elemento.classList.remove('positive', 'negative');
        
        const valor = elemento.textContent;
        if (valor.includes('-')) {
            elemento.classList.add('negative');
        } else if (valor !== '0,00') {
            elemento.classList.add('positive');
        }
    }

    btnDiferencaInvoice.addEventListener('click', () => calcularDiferenca('invoice_order'));
    btnDiferencaOffline.addEventListener('click', () => calcularDiferenca('transacao_offline'));
    btnDiferencaPos.addEventListener('click', () => calcularDiferenca('transacao_pos'));

    // Inicialização
    showToast('Bem-vindo', 'Sistema de Integração Sankhya iniciado.', 'info');
});
