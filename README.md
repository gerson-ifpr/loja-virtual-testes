# Loja Virtual - Exemplo de Níveis de Teste

## Estrutura do Projeto

```
loja_virtual/
├── src/
│   ├── __init__.py
│   ├── carrinho.py
│   ├── estoque.py
│   └── pagamento.py
├── tests/
│   ├── __init__.py
│   ├── test_carrinho_unit.py
│   └── test_carrinho_integracao.py
├── requirements.txt
├── pytest.ini
└── README.md
```

## Como Executar

```bash
pip install -r requirements.txt
pytest -v
pytest -m unit -v      # Apenas unitários
pytest -m integration -v  # Apenas integração
pytest --cov=src --cov-report=html
```