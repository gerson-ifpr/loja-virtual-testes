"""
Módulo CarrinhoDeCompras - Gerencia o carrinho de compras
"""

from decimal import Decimal
from typing import List, Dict, Optional, Tuple
from .estoque import Estoque


class CarrinhoDeCompras:
    def __init__(self, estoque: Estoque):
        self._estoque = estoque
        self._itens: List[Dict] = []
        self._desconto_percentual: Decimal = Decimal("0")
    
    def adicionar(self, sku: str, quantidade: int, preco_unitario: Optional[Decimal] = None) -> bool:
        if not self._estoque.verificar_disponibilidade(sku, quantidade):
            return False
        if preco_unitario is None:
            preco_unitario = self._estoque.obter_preco(sku)
            if preco_unitario is None:
                return False
        self._itens.append({"sku": sku, "quantidade": quantidade, "preco_unitario": preco_unitario})
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
    
    def finalizar_compra(self) -> Tuple[bool, Decimal]:
        """
        Finaliza a compra de forma ATÔMICA: primeiro confirma a
        disponibilidade atual de TODOS os itens (o estoque pode ter mudado
        desde que o item foi adicionado ao carrinho, por exemplo por causa
        de uma venda concorrente) e só então debita o estoque de cada um.

        Isso evita o cenário de "transação parcial": debitar o estoque de
        alguns itens e falhar no meio do caminho, deixando o carrinho e o
        estoque em um estado inconsistente.
        """
        total = self.calcular_total()

        # 1ª passada: valida a disponibilidade de tudo, sem alterar nada.
        for item in self._itens:
            if not self._estoque.verificar_disponibilidade(item["sku"], item["quantidade"]):
                return False, Decimal("0")

        # 2ª passada: como todos os itens foram confirmados, debita o estoque.
        for item in self._itens:
            self._estoque.baixar(item["sku"], item["quantidade"])

        self._itens.clear()
        self._desconto_percentual = Decimal("0")
        return True, total
    
    def listar_itens(self) -> List[Dict]:
        return self._itens.copy()
    
    def quantidade_itens(self) -> int:
        return len(self._itens)
    
    def limpar(self) -> None:
        self._itens.clear()
        self._desconto_percentual = Decimal("0")