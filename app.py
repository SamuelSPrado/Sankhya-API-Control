from flask import Flask, render_template, request, jsonify
import logging
import os
import sys

# Configurando o log
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Importando módulos do projeto
from api.sankhya import reprocessar_pedido, importar_produto
from database.queries import (
    consultar_pedido, 
    consultar_info_caixa, 
    consultar_invoice_order, 
    consultar_transacao_offline, 
    consultar_transacao_pos
)
from utils.formatters import calcular_diferenca

# Inicialização da aplicação Flask
app = Flask(__name__)

@app.route('/')
def index():
    """Rota principal que renderiza a página inicial com menu lateral."""
    return render_template('index.html')

# Rotas para Reprocessamento de Pedidos
@app.route('/api/pedido/consultar', methods=['POST'])
def api_consultar_pedido():
    """API para consultar pedido no banco de dados."""
    try:
        data = request.json
        pedido_id = data.get('pedido_id')
        
        if not pedido_id:
            return jsonify({
                'success': False,
                'error': 'ID do pedido não informado'
            }), 400
        
        resultados = consultar_pedido(pedido_id)
        
        return jsonify({
            'success': True,
            'data': resultados
        })
    except Exception as e:
        logger.error(f"Erro ao consultar pedido: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/pedido/reprocessar', methods=['POST'])
def api_reprocessar_pedido():
    """API para reprocessar pedido via API Sankhya."""
    try:
        data = request.json
        pedido_id = data.get('pedido_id')
        
        if not pedido_id:
            return jsonify({
                'success': False,
                'error': 'ID do pedido não informado'
            }), 400
        
        resultado = reprocessar_pedido(pedido_id)
        
        return jsonify(resultado)
    except Exception as e:
        logger.error(f"Erro ao reprocessar pedido: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Rotas para Importação de Produtos
@app.route('/api/produto/importar', methods=['POST'])
def api_importar_produto():
    """API para importar produto via API Sankhya."""
    try:
        data = request.json
        produto_id = data.get('produto_id')
        
        if not produto_id:
            return jsonify({
                'success': False,
                'error': 'ID do produto não informado'
            }), 400
        
        resultado = importar_produto(produto_id)
        
        return jsonify(resultado)
    except Exception as e:
        logger.error(f"Erro ao importar produto: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Rotas para Validação de Caixa
@app.route('/api/caixa/consultar', methods=['POST'])
def api_consultar_caixa():
    """API para consultar informações do caixa."""
    try:
        data = request.json
        local_id = data.get('local_id')
        caixa_id = data.get('caixa_id')
        
        if not local_id or not caixa_id:
            return jsonify({
                'success': False,
                'error': 'LOCAL_ID e CAIXA_ID são obrigatórios'
            }), 400
        
        # Consultar informações básicas do caixa
        info_caixa = consultar_info_caixa(caixa_id)
        
        # Consultar valores de Invoice Order
        invoice_order = consultar_invoice_order(local_id, caixa_id)
        
        # Consultar valores de Transação Offline
        transacao_offline = consultar_transacao_offline(local_id, caixa_id)
        
        # Consultar valores de Transação POS
        transacao_pos = consultar_transacao_pos(local_id, caixa_id)
        
        return jsonify({
            'success': True,
            'info_caixa': info_caixa,
            'invoice_order': invoice_order,
            'transacao_offline': transacao_offline,
            'transacao_pos': transacao_pos
        })
    except Exception as e:
        logger.error(f"Erro ao consultar caixa: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/caixa/calcular-diferenca', methods=['POST'])
def api_calcular_diferenca():
    """API para calcular diferença entre valores."""
    try:
        data = request.json
        origem = data.get('origem')
        valores_sankhya = data.get('valores_sankhya')
        
        if not origem or not valores_sankhya:
            return jsonify({
                'success': False,
                'error': 'Origem e valores Sankhya são obrigatórios'
            }), 400
        
        # Obter valores de origem
        if origem == 'invoice_order':
            valores_origem = data.get('invoice_order')
        elif origem == 'transacao_offline':
            valores_origem = data.get('transacao_offline')
        elif origem == 'transacao_pos':
            valores_origem = data.get('transacao_pos')
        else:
            return jsonify({
                'success': False,
                'error': 'Origem inválida'
            }), 400
        
        # Calcular diferenças
        diferencas = {
            'credito': calcular_diferenca(valores_origem.get('credito', '0,00'), valores_sankhya.get('credito', '0,00')),
            'debito': calcular_diferenca(valores_origem.get('debito', '0,00'), valores_sankhya.get('debito', '0,00')),
            'dinheiro': calcular_diferenca(valores_origem.get('dinheiro', '0,00'), valores_sankhya.get('dinheiro', '0,00')),
            'outros': calcular_diferenca(valores_origem.get('outros', '0,00'), valores_sankhya.get('outros', '0,00')),
            'desconto': calcular_diferenca(valores_origem.get('desconto', '0,00'), valores_sankhya.get('desconto', '0,00')),
            'total': calcular_diferenca(valores_origem.get('total', '0,00'), valores_sankhya.get('total', '0,00'))
        }
        
        return jsonify({
            'success': True,
            'diferencas': diferencas
        })
    except Exception as e:
        logger.error(f"Erro ao calcular diferença: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
