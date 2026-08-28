"""
Módulo CarrinhoDeCompras - Gerencia regras do carrinho com atomicidade total
"""
from decimal import Decimal
from typing import List, Dict, Optional, Tuple
from .estoque import Estoque
from .pagamento import Pagamento, MetodoPagamento, StatusPagamento


class CarrinhoDeCompras:
    def __init__(self, estoque: Estoque, gateway_pagamento: Optional[Pagamento] = None):
        self._estoque = estoque
        self._pagamento = gateway_pagamento or Pagamento()
        self._itens: List[Dict] = []
        self._desconto_percentual: Decimal = Decimal("0")
    
    def adicionar(self, sku: str, quantidade: int, preco_unitario: Optional[Decimal] = None) -> bool:
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser maior que zero")
        if not self._estoque.verificar_disponibilidade(sku, quantidade):
            return False
        if preco_unitario is None:
            preco_unitario = self._estoque.obter_preco(sku)
            if preco_unitario is None:
                return False
        self._itens.append({
            "sku": sku,
            "nome": self._estoque.obter_nome(sku) or sku,
            "quantidade": quantidade,
            "preco_unitario": preco_unitario
        })
        return True
    
    def remover(self, sku: str) -> bool:
        for i, item in enumerate(self._itens):
            if item["sku"] == sku:
                del self._itens[i]
                return True
        return False
    
    def calcular_total(self) -> Decimal:
        total = Decimal("0")
        for item in self._itens:
            total += item["quantidade"] * item["preco_unitario"]
        if self._desconto_percentual > 0:
            desconto = total * (self._desconto_percentual / Decimal("100"))
            total -= desconto
        return total
    
    def aplicar_desconto(self, percentual: Decimal) -> None:
        if 0 <= percentual <= 100:
            self._desconto_percentual = percentual
        else:
            raise ValueError("Percentual deve estar entre 0 e 100")
    
    def finalizar_compra(self, metodo_pagamento: MetodoPagamento, dados_pagamento: Optional[Dict] = None) -> Tuple[bool, Decimal, Optional[str]]:
        """
        Executa checkout atômico:
        1. Pré-validação de estoque
        2. Débito de estoque
        3. Cobrança financeira
        4. Rollback automático caso o pagamento não seja aprovado
        """
        if not self._itens:
            return False, Decimal("0"), "Carrinho vazio"

        total = self.calcular_total()

        # 1. Pré-validação
        for item in self._itens:
            if not self._estoque.verificar_disponibilidade(item["sku"], item["quantidade"]):
                return False, Decimal("0"), "Estoque insuficiente"

        # 2. Débito de estoque
        itens_debitados = []
        for item in self._itens:
            if self._estoque.baixar(item["sku"], item["quantidade"]):
                itens_debitados.append(item)

        # 3. Processamento do Pagamento
        res_pagamento = self._pagamento.processar(total, metodo_pagamento, dados_pagamento)
        
        # 4. Rollback em caso de falha
        if res_pagamento["status"] != StatusPagamento.APROVADO:
            for item in itens_debitados:
                self._estoque.cadastrar(item["sku"], item["quantidade"])
            return False, total, res_pagamento.get("motivo", "Pagamento recusado")

        self._itens.clear()
        self._desconto_percentual = Decimal("0")
        return True, total, res_pagamento["transacao_id"]
    
    def listar_itens(self) -> List[Dict]:
        return self._itens.copy()
    
    def quantidade_itens(self) -> int:
        return len(self._itens)
    
    def limpar(self) -> None:
        self._itens.clear()
        self._desconto_percentual = Decimal("0")