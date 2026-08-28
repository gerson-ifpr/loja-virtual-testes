"""
Nível 1: Testes de Integração com Estoque Real e Rollback de Transação
"""
import pytest
from decimal import Decimal
from src.carrinho import CarrinhoDeCompras
from src.estoque import Estoque
from src.pagamento import Pagamento, MetodoPagamento

pytestmark = pytest.mark.integration


class TestCarrinhoIntegracao:
    @pytest.fixture
    def setup_integracao(self):
        estoque = Estoque(popular_padrao=True)
        pagamento = Pagamento()
        carrinho = CarrinhoDeCompras(estoque, pagamento)
        return carrinho, estoque, pagamento

    def test_bloqueio_de_item_sem_estoque(self, setup_integracao):
        carrinho, _, _ = setup_integracao
        # SKU-ESTB-20 foi cadastrado com estoque 0
        assert carrinho.adicionar("SKU-ESTB-20", 1) is False
        assert carrinho.quantidade_itens() == 0

    def test_compra_atômica_com_baixa_multiplos_produtos(self, setup_integracao):
        carrinho, estoque, _ = setup_integracao
        carrinho.adicionar("SKU-MOUS-02", 2)  # R$ 120 * 2 = 240
        carrinho.adicionar("SKU-TECL-03", 1)  # R$ 350 * 1 = 350
        
        sucesso, total, trx_id = carrinho.finalizar_compra(MetodoPagamento.PIX)
        
        assert sucesso is True
        assert total == Decimal("590.00")
        assert estoque.quantidade_disponivel("SKU-MOUS-02") == 48
        assert estoque.quantidade_disponivel("SKU-TECL-03") == 24

    def test_rollback_de_estoque_apos_recusa_de_pagamento(self, setup_integracao):
        carrinho, estoque, _ = setup_integracao
        # Tenta comprar 4 Notebooks (R$ 18.000, excede o limite de R$ 15.000 da regra de crédito)
        carrinho.adicionar("SKU-NOTE-01", 4)
        
        sucesso, _, motivo = carrinho.finalizar_compra(MetodoPagamento.CARTAO_CREDITO)
        
        assert sucesso is False
        assert motivo == "Valor acima do limite permitido"
        # Garante que o estoque foi revertido integralmente (rollback)
        assert estoque.quantidade_disponivel("SKU-NOTE-01") == 10