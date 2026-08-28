"""
Nível 2: Testes de Aceitação baseados em Critérios de Requisitos (BDD)
"""
import pytest
from decimal import Decimal
from src.carrinho import CarrinhoDeCompras
from src.estoque import Estoque
from src.pagamento import Pagamento, MetodoPagamento

pytestmark = pytest.mark.acceptance


class TestAceitacaoCriterios:
    def test_criterio_black_friday_combo_gamer(self):
        """
        Cenário: Compra Promocional Gamer
        Dado que um cliente adiciona 1 Teclado Mecânico (R$ 350) e 1 Headset Gamer (R$ 280)
        Quando ele aplica o cupom BLACKFRIDAY de 20%
        E finaliza a compra com PIX
        Então o valor cobrado deve ser R$ 504.00
        E o carrinho deve ficar limpo
        """
        estoque = Estoque(popular_padrao=True)
        carrinho = CarrinhoDeCompras(estoque, Pagamento())

        # Dado
        carrinho.adicionar("SKU-TECL-03", 1)
        carrinho.adicionar("SKU-HEAD-05", 1)

        # Quando
        carrinho.aplicar_desconto(Decimal("20"))
        sucesso, total, trx = carrinho.finalizar_compra(MetodoPagamento.PIX)

        # Então
        assert sucesso is True
        assert total == Decimal("504.00")
        assert carrinho.quantidade_itens() == 0
        assert trx.startswith("TRX-")