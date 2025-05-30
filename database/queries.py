"""
Módulo para consultas SQL relacionadas à validação de caixa e pedidos.
"""
import logging
from database.database import get_connection

# Configurando o log
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def consultar_pedido(pedido_id):
    """
    Consulta informações de um pedido no banco de dados.
    
    Args:
        pedido_id (str): ID do pedido a ser consultado.
        
    Returns:
        list: Lista de registros encontrados para o pedido.
    """
    query = """
    SELECT 
        SO.SANKHYAID
        , IV.DISCOUNT
        , OP.VALUE
        , IV.ORDERDATE
        , S.ERRORMESSAGE
        , S.DATE
    FROM 
        VWSANKHYAORDER SO 
        FULL JOIN VWINVOICEORDER IV ON SO.MEEPID = IV.ID 
        INNER JOIN VWORDERPAYMENT OP ON IV.ID = OP.ORDER_ID
        FULL JOIN VWSANKHYAINVOICEERROR S ON S.INVOICEORDER_ID = IV.ID
    WHERE 
        IV.ID = ?
    ORDER BY 
        S.DATE DESC
    """
    
    try:
        logger.info(f"Consultando pedido {pedido_id}...")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (pedido_id,))
        
        # Converter resultados para lista de dicionários
        columns = [column[0] for column in cursor.description]
        results = []
        
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        
        cursor.close()
        conn.close()
        
        return results
    except Exception as e:
        logger.error(f"Erro ao consultar pedido: {e}")
        raise

def consultar_info_caixa(caixa_id):
    """
    Consulta informações básicas do caixa.
    
    Args:
        caixa_id (str): ID do caixa a ser consultado.
        
    Returns:
        dict: Informações do caixa (portal, data inicial, data final).
    """
    query = """
    SELECT
        L.NOME 'PORTAL_MEEP',
        CONVERT(VARCHAR(10), MIN(SP.DATAINICIO), 103) AS DATA_INICIAL,
        CONVERT(VARCHAR(10), MAX(SP.DATAFIM), 103) AS DATA_FINAL
    FROM VWSESSAOPOS SP INNER JOIN VWLOCAL L ON SP.LOCALCLIENTEID = L.ID
    WHERE SP.ID = ?
    GROUP BY L.NOME
    """
    
    try:
        logger.info(f"Consultando informações do caixa {caixa_id}...")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (caixa_id,))
        
        row = cursor.fetchone()
        if row:
            result = {
                "portal_meep": row[0],
                "data_inicial": row[1],
                "data_final": row[2]
            }
        else:
            result = {
                "portal_meep": "",
                "data_inicial": "",
                "data_final": ""
            }
        
        cursor.close()
        conn.close()
        
        return result
    except Exception as e:
        logger.error(f"Erro ao consultar informações do caixa: {e}")
        raise

def consultar_invoice_order(local_id, caixa_id):
    """
    Consulta valores de Invoice Order para um caixa.
    
    Args:
        local_id (str): ID do local.
        caixa_id (str): ID do caixa.
        
    Returns:
        dict: Valores agrupados por tipo de pagamento.
    """
    query = """
    SELECT 
        FORMAT(SUM(CASE WHEN FP.CODIGO = 1 THEN OP.VALUE ELSE 0 END), 'N', 'PT-BR') AS [CREDITO],
        FORMAT(SUM(CASE WHEN FP.CODIGO = 2 THEN OP.VALUE ELSE 0 END), 'N', 'PT-BR') AS [DEBITO],
        FORMAT(SUM(CASE WHEN FP.CODIGO = 3 THEN OP.VALUE ELSE 0 END), 'N', 'PT-BR') AS [DINHEIRO],
        FORMAT(SUM(CASE WHEN FP.CODIGO = 100 THEN OP.VALUE ELSE 0 END), 'N', 'PT-BR') AS [OUTROS],
        FORMAT(SUM(IV.DISCOUNT), 'N', 'PT-BR') AS [DESCONTO],
        FORMAT(SUM(OP.VALUE), 'N', 'PT-BR') AS TOTAL_CAIXA_INVOICE
    FROM
        VWINVOICEORDER IV
        INNER JOIN VWORDERPAYMENT OP ON IV.ID = OP.ORDER_ID
        INNER JOIN VWFORMAPAGAMENTO FP ON OP.FORMOFPAYMENT_ID = FP.ID
        LEFT JOIN VWPEDIDOPOS PP ON IV.ID = PP.ID
    WHERE
        IV.OWNER_ID = ?
        AND IV.CASHIER_ID = ?
        AND PP.STATUS = 3
    """
    
    try:
        logger.info(f"Consultando Invoice Order para local {local_id} e caixa {caixa_id}...")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (local_id, caixa_id))
        
        row = cursor.fetchone()
        if row:
            result = {
                "credito": row[0],
                "debito": row[1],
                "dinheiro": row[2],
                "outros": row[3],
                "desconto": row[4],
                "total": row[5]
            }
        else:
            result = {
                "credito": "0,00",
                "debito": "0,00",
                "dinheiro": "0,00",
                "outros": "0,00",
                "desconto": "0,00",
                "total": "0,00"
            }
        
        cursor.close()
        conn.close()
        
        return result
    except Exception as e:
        logger.error(f"Erro ao consultar Invoice Order: {e}")
        raise

def consultar_transacao_offline(local_id, caixa_id):
    """
    Consulta valores de Transação Offline para um caixa.
    
    Args:
        local_id (str): ID do local.
        caixa_id (str): ID do caixa.
        
    Returns:
        dict: Valores agrupados por tipo de pagamento.
    """
    query = """
    SELECT 
        FORMAT(SUM(CASE WHEN T.TIPOPAGAMENTO = 1 THEN T.VALOR ELSE 0 END), 'N', 'PT-BR') AS 'CREDITO',
        FORMAT(SUM(CASE WHEN T.TIPOPAGAMENTO = 2 THEN T.VALOR ELSE 0 END), 'N', 'PT-BR') AS 'DEBITO',
        FORMAT(SUM(CASE WHEN T.TIPOPAGAMENTO = 3 THEN T.VALOR ELSE 0 END), 'N', 'PT-BR') AS 'DINHEIRO',
        FORMAT(SUM(CASE WHEN T.TIPOPAGAMENTO NOT IN (1, 2, 3) THEN T.VALOR ELSE 0 END), 'N', 'PT-BR') AS 'OUTROS',
        FORMAT(SUM(PP.DESCONTO), 'N', 'PT-BR') AS 'DESCONTO',
        FORMAT(SUM(T.VALOR), 'N', 'PT-BR') AS 'TOTAL'
    FROM 
        VWTRANSACAOOFFLINE T 
        JOIN VWPEDIDOPOS PP ON T.PEDIDOPOSID = PP.ID
    WHERE
        T.LOCALCLIENTEID = ?
        AND PP.SESSAOPOSID = ?
        AND T.STATUS NOT IN (5)
    """
    
    try:
        logger.info(f"Consultando Transação Offline para local {local_id} e caixa {caixa_id}...")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (local_id, caixa_id))
        
        row = cursor.fetchone()
        if row:
            result = {
                "credito": row[0],
                "debito": row[1],
                "dinheiro": row[2],
                "outros": row[3],
                "desconto": row[4],
                "total": row[5]
            }
        else:
            result = {
                "credito": "0,00",
                "debito": "0,00",
                "dinheiro": "0,00",
                "outros": "0,00",
                "desconto": "0,00",
                "total": "0,00"
            }
        
        cursor.close()
        conn.close()
        
        return result
    except Exception as e:
        logger.error(f"Erro ao consultar Transação Offline: {e}")
        raise

def consultar_transacao_pos(local_id, caixa_id):
    """
    Consulta valores de Transação POS para um caixa.
    
    Args:
        local_id (str): ID do local.
        caixa_id (str): ID do caixa.
        
    Returns:
        dict: Valores agrupados por tipo de pagamento.
    """
    query = """
    SELECT
        FORMAT(SUM(CASE WHEN T.TIPOPAGAMENTO = 1 THEN T.VALOR ELSE 0 END), 'N', 'PT-BR') AS [CREDITO],
        FORMAT(SUM(CASE WHEN T.TIPOPAGAMENTO = 2 THEN T.VALOR ELSE 0 END), 'N', 'PT-BR') AS [DEBITO],
        FORMAT(SUM(CASE WHEN T.TIPOPAGAMENTO = 3 THEN T.VALOR ELSE 0 END), 'N', 'PT-BR') AS [DINHEIRO],
        FORMAT(SUM(CASE WHEN T.TIPOPAGAMENTO NOT IN (1, 2, 3) THEN T.VALOR ELSE 0 END), 'N', 'PT-BR') AS [OUTROS],
        FORMAT(SUM(PP.DESCONTO), 'N', 'PT-BR') AS [DESCONTO],
        FORMAT(SUM(T.VALOR), 'N', 'PT-BR') AS 'TOTAL'
    FROM 
        VWTRANSACAOPOS T 
        JOIN VWPEDIDOPOS PP ON T.PEDIDOPOSID = PP.ID
    WHERE
        T.LOCALCLIENTEID = ?
        AND PP.SESSAOPOSID = ?
        AND T.STATUS NOT IN (5)
    """
    
    try:
        logger.info(f"Consultando Transação POS para local {local_id} e caixa {caixa_id}...")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (local_id, caixa_id))
        
        row = cursor.fetchone()
        if row:
            result = {
                "credito": row[0],
                "debito": row[1],
                "dinheiro": row[2],
                "outros": row[3],
                "desconto": row[4],
                "total": row[5]
            }
        else:
            result = {
                "credito": "0,00",
                "debito": "0,00",
                "dinheiro": "0,00",
                "outros": "0,00",
                "desconto": "0,00",
                "total": "0,00"
            }
        
        cursor.close()
        conn.close()
        
        return result
    except Exception as e:
        logger.error(f"Erro ao consultar Transação POS: {e}")
        raise
