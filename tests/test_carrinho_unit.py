"""
Testes Unitários para CarrinhoDeCompras
"""

import pytest
from decimal import Decimal
from unittest.mock import Mock

from src.carrinho import CarrinhoDeCompras
from src.estoque import Estoque

# Marca TODOS os testes deste módulo como testes UNITÁRIOS.
# Isso é o que permite rodar apenas estes testes com: pytest -m unit -v
pytestmark = pytest.mark.unit


class TestCarrinhoUnitario:
    @pytest.fixture
    def estoque_stub(self):
        estoque = Mock(spec=Estoque)
        estoque.verificar_disponibilidade.return_value = True
        estoque.obter_preco.return_value = Decimal("50.00")
        return estoque
    
    @pytest.fixture
    def carrinho(self, estoque_stub):
        return CarrinhoDeCompras(estoque_stub)
    
    def test_adicionar_item_com_sucesso(self, carrinho):
        resultado = carrinho.adicionar("SKU-001", 2, Decimal("50.00"))
        assert resultado is True
        assert carrinho.quantidade_itens() == 1
    
    def test_calcular_total_com_dois_itens(self, carrinho):
        carrinho.adicionar("SKU-001", 2, Decimal("50.00"))
        carrinho.adicionar("SKU-002", 1, Decimal("30.00"))
        total = carrinho.calcular_total()
        assert total == Decimal("130.00")
    
    def test_calcular_total_sem_itens(self, carrinho):
        total = carrinho.calcular_total()
        assert total == Decimal("0")
    
    def test_aplicar_desconto_percentual(self, carrinho):
        carrinho.adicionar("SKU-001", 2, Decimal("100.00"))
        carrinho.aplicar_desconto(Decimal("10"))
        total = carrinho.calcular_total()
        assert total == Decimal("180.00")
    
    def test_remover_item(self, carrinho):
        carrinho.adicionar("SKU-001", 2, Decimal("50.00"))
        carrinho.adicionar("SKU-002", 1, Decimal("30.00"))
        removido = carrinho.remover("SKU-001")
        assert removido is True
        assert carrinho.quantidade_itens() == 1
    
    def test_limpar_carrinho(self, carrinho):
        carrinho.adicionar("SKU-001", 2, Decimal("50.00"))
        carrinho.limpar()
        assert carrinho.quantidade_itens() == 0