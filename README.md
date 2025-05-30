# Documentação do Projeto de Integração Sankhya

## Visão Geral

Este projeto implementa uma interface web para integração com o sistema Sankhya, oferecendo três funcionalidades principais:

1. **Reprocessamento de pedidos**: Permite consultar e reprocessar pedidos via API
2. **Importação de produtos**: Facilita a importação de produtos via API
3. **Validação de caixa**: Possibilita a comparação de valores entre diferentes sistemas

A aplicação foi desenvolvida com uma interface moderna, responsiva e de fácil utilização, com menu lateral fixo para navegação entre as funcionalidades.

## Estrutura do Projeto

```
integracao_sankhya/
├── static/                  # Arquivos estáticos
│   ├── css/                 # Estilos CSS
│   │   └── styles.css       # Estilos da aplicação
│   ├── js/                  # Scripts JavaScript
│   │   └── script.js        # Lógica de interação frontend-backend
│   └── img/                 # Imagens (pasta vazia para uso futuro)
├── templates/               # Templates HTML
│   └── index.html           # Página principal da aplicação
├── database/                # Módulos de banco de dados
│   ├── __init__.py          # Inicializador do pacote
│   ├── database.py          # Funções de conexão com banco de dados
│   ├── queries.py           # Consultas SQL para as funcionalidades
│   └── secret.py            # Credenciais (simuladas)
├── api/                     # Módulos de API
│   ├── __init__.py          # Inicializador do pacote
│   └── sankhya.py           # Funções para integração com API Sankhya
├── utils/                   # Utilitários
│   ├── __init__.py          # Inicializador do pacote
│   └── formatters.py        # Funções para formatação e cálculos
└── app.py                   # Aplicação Flask principal
```

## Requisitos do Sistema

### Dependências Python
- Flask
- pyodbc
- requests

### Dependências do Sistema
- unixodbc
- unixodbc-dev
- ODBC Driver 17 for SQL Server (para ambiente de produção)

## Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd integracao_sankhya
```

2. Instale as dependências Python:
```bash
pip install flask pyodbc requests
```

3. Instale as dependências do sistema:
```bash
sudo apt-get update
sudo apt-get install -y unixodbc unixodbc-dev
```

4. Para ambiente de produção, instale o driver ODBC para SQL Server:
```bash
# Para Ubuntu/Debian
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list
apt-get update
ACCEPT_EULA=Y apt-get install -y msodbcsql17
```

5. Configure as credenciais:
   - Edite o arquivo `database/secret.py` com suas credenciais reais

## Execução

Para iniciar a aplicação:

```bash
python app.py
```

A aplicação estará disponível em `http://localhost:5001`

## Funcionalidades

### 1. Reprocessamento de Pedidos

Esta funcionalidade permite consultar informações de um pedido no banco de dados e reprocessá-lo via API Sankhya.

**Fluxo de uso:**
1. Insira o ID do pedido no campo correspondente
2. Clique em "Validar" para consultar o pedido no banco de dados
3. Clique em "Reprocessar" para enviar o pedido para reprocessamento via API
4. O status code e os resultados serão exibidos nas áreas correspondentes
5. Use o botão "Limpar" para reiniciar o processo

**Endpoint da API utilizado:**
- `https://third-api.meep.cloud/api/sankhya/InvoiceOrder/Export?invoiceId={Order_ID}`
- Método: POST
- Não requer autenticação

### 2. Importação de Produtos

Esta funcionalidade permite importar produtos via API Sankhya.

**Fluxo de uso:**
1. Insira o ID do produto no campo correspondente
2. Clique em "Importar" para enviar o produto para importação via API
3. O status code, código do produto e descrição serão exibidos nas áreas correspondentes
4. Use o botão "Limpar" para reiniciar o processo

**Endpoint da API utilizado:**
- `https://third-api.meep.cloud/api/sankhya/ExportProduct/{PRODUCT_ID}`
- Método: POST
- Não requer autenticação

### 3. Validação de Caixa

Esta funcionalidade permite comparar valores entre diferentes sistemas (Invoice Order, Transação Offline, Transação POS e Sankhya).

**Fluxo de uso:**
1. Insira o LOCAL_ID e CAIXA_ID nos campos correspondentes
2. Clique em "Consultar Caixa" para obter os dados do banco de dados
3. Preencha manualmente os valores do Caixa Sankhya
4. Clique em um dos botões de diferença para calcular a diferença entre o sistema selecionado e o Sankhya
5. As diferenças serão exibidas na área correspondente
6. Use o botão "Limpar" para reiniciar o processo

**Consultas SQL utilizadas:**
- Consulta de informações do caixa
- Consulta de valores de Invoice Order
- Consulta de valores de Transação Offline
- Consulta de valores de Transação POS

## Personalização

### Estilos
Para personalizar a aparência da aplicação, edite o arquivo `static/css/styles.css`.

### Comportamento
Para modificar o comportamento da aplicação, edite o arquivo `static/js/script.js`.

### Backend
Para ajustar as consultas SQL ou a integração com a API, edite os arquivos em `database/queries.py` e `api/sankhya.py`.

## Notas Importantes

- Em ambiente de produção, substitua as credenciais simuladas pelas reais no arquivo `database/secret.py`
- Certifique-se de que o driver ODBC para SQL Server esteja instalado corretamente
- Para melhor desempenho, considere usar um servidor WSGI como Gunicorn ou uWSGI em produção
- Mantenha as credenciais seguras e não as compartilhe em repositórios públicos
