"""
Nível 2: Teste de Sistema (E2E) - Jornada Completa do Cliente
"""
import pytest
from decimal import Decimal
from src.carrinho import CarrinhoDeCompras
from src.estoque import Estoque
from src.pagamento import Pagamento, MetodoPagamento, StatusPagamento

pytestmark = pytest.mark.system


class TestSistemaCompleto:
    def test_jornada_completa_setup_office_e_estorno(self):
        """
        Jornada E2E:
        1. Consulta o catálogo completo com 20 itens.
        2. Monta um Setup Home Office (Mesa + Cadeira + Suporte + Webcam).
        3. Aplica cupom de 5%.
        4. Finaliza via Cartão de Crédito.
        5. Cliente solicita cancelamento total da compra (pós-venda).
        """
        estoque = Estoque(popular_padrao=True)
        pagamento = Pagamento()
        carrinho = CarrinhoDeCompras(estoque, pagamento)

        # Montagem do carrinho
        carrinho.adicionar("SKU-MESA-08", 1) # R$ 1850.00
        carrinho.adicionar("SKU-CADE-07", 1) # R$ 1100.00
        carrinho.adicionar("SKU-SUPM-10", 1) # R$ 320.00
        carrinho.adicionar("SKU-WEBC-06", 1) # R$ 210.00
        # Subtotal: R$ 3480.00

        carrinho.aplicar_desconto(Decimal("5")) # 5% = R$ 174.00 de desconto -> Total R$ 3306.00

        sucesso, total_pago, transacao_id = carrinho.finalizar_compra(MetodoPagamento.CARTAO_CREDITO)

        assert sucesso is True
        assert total_pago == Decimal("3306.00")
        assert estoque.quantidade_disponivel("SKU-MESA-08") == 4
        assert estoque.quantidade_disponivel("SKU-CADE-07") == 7

        # Pós-venda: Estorno da transação
        cancelado = pagamento.cancelar(transacao_id)
        assert cancelado is True
        transacao = pagamento.obter_transacao(transacao_id)
        assert transacao["status"] == StatusPagamento.CANCELADO