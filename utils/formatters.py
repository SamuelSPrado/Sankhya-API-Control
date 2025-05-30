"""
Módulo de utilidades para formatação e cálculos.
"""
import re

def parse_currency_value(value_str):
    """
    Converte uma string de valor monetário no formato brasileiro para float.
    
    Args:
        value_str (str): String com valor no formato brasileiro (ex: "1.234,56").
        
    Returns:
        float: Valor convertido para float.
    """
    if not value_str:
        return 0.0
    
    # Remove caracteres não numéricos, exceto ponto e vírgula
    clean_value = re.sub(r'[^\d,.]', '', value_str)
    
    # Substitui vírgula por ponto para conversão
    clean_value = clean_value.replace(".", "").replace(",", ".")
    
    try:
        return float(clean_value)
    except ValueError:
        return 0.0

def format_currency_value(value):
    """
    Formata um valor numérico para o formato de moeda brasileira.
    
    Args:
        value (float): Valor a ser formatado.
        
    Returns:
        str: Valor formatado no padrão brasileiro (ex: 1.234,56).
    """
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def calcular_diferenca(valor1, valor2):
    """
    Calcula a diferença entre dois valores monetários em formato brasileiro.
    
    Args:
        valor1 (str): Primeiro valor no formato brasileiro (ex: "1.234,56").
        valor2 (str): Segundo valor no formato brasileiro (ex: "1.000,00").
        
    Returns:
        str: Diferença formatada no padrão brasileiro.
    """
    # Converter para float
    float_valor1 = parse_currency_value(valor1)
    float_valor2 = parse_currency_value(valor2)
    
    # Calcular diferença
    diferenca = float_valor1 - float_valor2
    
    # Formatar resultado
    return format_currency_value(diferenca)
