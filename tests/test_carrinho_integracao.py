"""
Testes de Integração para CarrinhoDeCompras
"""

import pytest
from decimal import Decimal

from src.carrinho import CarrinhoDeCompras
from src.estoque import Estoque

# Marca TODOS os testes deste módulo como testes de INTEGRAÇÃO.
# Isso é o que permite rodar apenas estes testes com: pytest -m integration -v
pytestmark = pytest.mark.integration


class TestCarrinhoIntegracao:
    @pytest.fixture
    def estoque_real(self):
        estoque = Estoque()
        estoque.cadastrar("SKU-001", 10, Decimal("50.00"))
        estoque.cadastrar("SKU-002", 5, Decimal("30.00"))
        estoque.cadastrar("SKU-003", 0, Decimal("100.00"))
        return estoque
    
    @pytest.fixture
    def carrinho(self, estoque_real):
        return CarrinhoDeCompras(estoque_real)
    
    def test_adicionar_item_com_estoque_real(self, carrinho, estoque_real):
        resultado = carrinho.adicionar("SKU-001", 2)
        assert resultado is True
        assert carrinho.quantidade_itens() == 1
        assert estoque_real.quantidade_disponivel("SKU-001") == 10
    
    def test_adicionar_item_sem_estoque(self, carrinho):
        resultado = carrinho.adicionar("SKU-003", 1)
        assert resultado is False
        assert carrinho.quantidade_itens() == 0
    
    def test_finalizar_compra_da_baixa_no_estoque(self, carrinho, estoque_real):
        carrinho.adicionar("SKU-001", 3)
        qtd_inicial = estoque_real.quantidade_disponivel("SKU-001")
        sucesso, total = carrinho.finalizar_compra()
        assert sucesso is True
        assert total == Decimal("150.00")
        assert estoque_real.quantidade_disponivel("SKU-001") == qtd_inicial - 3
    
    def test_finalizar_compra_com_estoque_insuficiente(self, carrinho, estoque_real):
        """
        Simula uma condição real de concorrência: dois itens são
        adicionados ao carrinho enquanto havia estoque suficiente para
        ambos, mas o estoque de um deles é reduzido por OUTRA venda
        (concorrente) antes de este cliente finalizar a compra.

        Esse cenário só é possível de reproduzir com o Estoque REAL
        (por isso é um teste de INTEGRAÇÃO, e não unitário) e verifica que
        finalizar_compra() é atômica: se um item não puder mais ser
        debitado, NENHUM item do carrinho deve ter seu estoque alterado.
        """
        carrinho.adicionar("SKU-001", 8)   # estoque inicial: 10 unidades
        carrinho.adicionar("SKU-002", 3)   # estoque inicial: 5 unidades

        # "Outro cliente" compra 4 unidades de SKU-002 nesse meio-tempo,
        # deixando apenas 1 unidade disponível (insuficiente para este carrinho).
        estoque_real.baixar("SKU-002", 4)

        sucesso, total = carrinho.finalizar_compra()

        assert sucesso is False
        assert total == Decimal("0")
        # Ponto-chave: SKU-001 não pode ter sido debitado (transação atômica).
        assert estoque_real.quantidade_disponivel("SKU-001") == 10
    
    def test_carrinho_limpo_apos_compra(self, carrinho):
        carrinho.adicionar("SKU-001", 2)
        carrinho.aplicar_desconto(Decimal("10"))
        sucesso, _ = carrinho.finalizar_compra()
        assert sucesso is True
        assert carrinho.quantidade_itens() == 0
        assert carrinho.calcular_total() == Decimal("0")