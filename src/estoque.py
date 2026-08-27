"""
Módulo Estoque - Gerencia o inventário de produtos
"""

from decimal import Decimal
from typing import Dict, Optional


class Estoque:
    def __init__(self):
        self._produtos: Dict[str, Dict] = {}
    
    def cadastrar(self, sku: str, quantidade: int, preco: Optional[Decimal] = None) -> None:
        if sku in self._produtos:
            self._produtos[sku]["quantidade"] += quantidade
            if preco is not None:
                self._produtos[sku]["preco"] = preco
        else:
            self._produtos[sku] = {"quantidade": quantidade, "preco": preco}
    
    def verificar_disponibilidade(self, sku: str, quantidade: int = 1) -> bool:
        if sku not in self._produtos:
            return False
        return self._produtos[sku]["quantidade"] >= quantidade
    
    def baixar(self, sku: str, quantidade: int) -> bool:
        if not self.verificar_disponibilidade(sku, quantidade):
            return False
        self._produtos[sku]["quantidade"] -= quantidade
        return True
    
    def quantidade_disponivel(self, sku: str) -> int:
        if sku not in self._produtos:
            return 0
        return self._produtos[sku]["quantidade"]
    
    def obter_preco(self, sku: str) -> Optional[Decimal]:
        if sku not in self._produtos:
            return None
        return self._produtos[sku].get("preco")