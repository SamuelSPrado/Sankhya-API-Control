"""
Módulo para integração com a API Sankhya.
Contém funções para reprocessamento de pedidos e importação de produtos.
"""
import requests
import logging
import json
from database import secret

# Configurando o log
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def reprocessar_pedido(order_id):
    """
    Reprocessa um pedido através da API Sankhya.
    
    Args:
        order_id (str): ID do pedido a ser reprocessado.
        
    Returns:
        dict: Resposta da API contendo status code e mensagem.
    """
    url = f"{secret.API_BASE_URL}/sankhya/InvoiceOrder/Export?invoiceId={order_id}"
    
    try:
        logger.info(f"Reprocessando pedido {order_id}...")
        response = requests.post(url, timeout=30)
        
        # Forçar exceção para status codes de erro
        response.raise_for_status()
        
        return {
            "success": True,
            "status_code": response.status_code,
            "message": "Pedido reprocessado com sucesso."
        }
    except requests.exceptions.HTTPError as e:
        logger.error(f"Erro HTTP ao reprocessar pedido: {e}")
        return {
            "success": False,
            "status_code": e.response.status_code if hasattr(e, 'response') else 500,
            "message": str(e)
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao reprocessar pedido: {e}")
        return {
            "success": False,
            "status_code": 500,
            "message": str(e)
        }

def importar_produto(product_id):
    """
    Importa um produto através da API Sankhya.
    
    Args:
        product_id (str): ID do produto a ser importado.
        
    Returns:
        dict: Resposta da API contendo status code e dados do produto.
    """
    url = f"{secret.API_BASE_URL}/sankhya/ExportProduct/{product_id}"
    
    try:
        logger.info(f"Importando produto {product_id}...")
        response = requests.post(url, timeout=30)
        
        # Forçar exceção para status codes de erro
        response.raise_for_status()
        
        # Processar resposta JSON
        data = response.json()
        
        return {
            "success": True,
            "status_code": response.status_code,
            "product_code": data.get("productCode", ""),
            "description": data.get("description", ""),
            "data": data
        }
    except requests.exceptions.HTTPError as e:
        logger.error(f"Erro HTTP ao importar produto: {e}")
        return {
            "success": False,
            "status_code": e.response.status_code if hasattr(e, 'response') else 500,
            "message": str(e),
            "product_code": "",
            "description": ""
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao importar produto: {e}")
        return {
            "success": False,
            "status_code": 500,
            "message": str(e),
            "product_code": "",
            "description": ""
        }
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao decodificar resposta JSON: {e}")
        return {
            "success": False,
            "status_code": response.status_code if 'response' in locals() else 500,
            "message": f"Erro ao processar resposta: {str(e)}",
            "product_code": "",
            "description": ""
        }
