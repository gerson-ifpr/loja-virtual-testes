"""
Nível 1: Testes Unitários Isolados com Mocks
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock
from src.carrinho import CarrinhoDeCompras
from src.estoque import Estoque
from src.pagamento import Pagamento, MetodoPagamento, StatusPagamento

pytestmark = pytest.mark.unit


class TestCarrinhoUnitario:
    @pytest.fixture
    def setup_mocks(self):
        estoque_stub = Mock(spec=Estoque)
        estoque_stub.verificar_disponibilidade.return_value = True
        estoque_stub.obter_preco.return_value = Decimal("4500.00")
        estoque_stub.obter_nome.return_value = "Notebook Gamer"
        
        pagamento_mock = Mock(spec=Pagamento)
        pagamento_mock.processar.return_value = {
            "sucesso": True,
            "status": StatusPagamento.APROVADO,
            "transacao_id": "TRX-UNIT-999"
        }
        carrinho = CarrinhoDeCompras(estoque_stub, pagamento_mock)
        return carrinho, estoque_stub, pagamento_mock

    def test_adicionar_item_com_sucesso(self, setup_mocks):
        carrinho, _, _ = setup_mocks
        assert carrinho.adicionar("SKU-NOTE-01", 1) is True
        assert carrinho.quantidade_itens() == 1

    def test_calcular_total_com_desconto(self, setup_mocks):
        carrinho, _, _ = setup_mocks
        carrinho.adicionar("SKU-NOTE-01", 2, Decimal("4500.00")) # R$ 9000
        carrinho.aplicar_desconto(Decimal("10")) # 10% = R$ 8100
        assert carrinho.calcular_total() == Decimal("8100.00")

    def test_rejeitar_quantidade_negativa_ou_zero(self, setup_mocks):
        carrinho, _, _ = setup_mocks
        with pytest.raises(ValueError, match="Quantidade deve ser maior que zero"):
            carrinho.adicionar("SKU-MOUS-02", 0)

    def test_rejeitar_desconto_invalido(self, setup_mocks):
        carrinho, _, _ = setup_mocks
        with pytest.raises(ValueError, match="Percentual deve estar entre 0 e 100"):
            carrinho.aplicar_desconto(Decimal("150"))

    def test_limpar_carrinho(self, setup_mocks):
        carrinho, _, _ = setup_mocks
        carrinho.adicionar("SKU-NOTE-01", 1)
        carrinho.limpar()
        assert carrinho.quantidade_itens() == 0
        assert carrinho.calcular_total() == Decimal("0")