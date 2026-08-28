"""
Módulo Estoque - Gerencia o catálogo e inventário de 20 produtos diversos
"""
from decimal import Decimal
from typing import Dict, Optional


class Estoque:
    def __init__(self, popular_padrao: bool = False):
        self._produtos: Dict[str, Dict] = {}
        if popular_padrao:
            self.carregar_catalogo_padrao()
    
    def cadastrar(self, sku: str, quantidade: int, preco: Optional[Decimal] = None, nome: Optional[str] = None) -> None:
        if sku in self._produtos:
            self._produtos[sku]["quantidade"] += quantidade
            if preco is not None:
                self._produtos[sku]["preco"] = preco
            if nome is not None:
                self._produtos[sku]["nome"] = nome
        else:
            self._produtos[sku] = {
                "nome": nome or sku,
                "quantidade": quantidade,
                "preco": preco
            }
    
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

    def obter_nome(self, sku: str) -> Optional[str]:
        if sku not in self._produtos:
            return None
        return self._produtos[sku].get("nome")

    def carregar_catalogo_padrao(self) -> None:
        """Cadastra 20 produtos variados para testes práticos."""
        catalogo = [
            ("SKU-NOTE-01", "Notebook Gamer 16GB SSD 512GB", 10, Decimal("4500.00")),
            ("SKU-MOUS-02", "Mouse Sem Fio Ergonômico", 50, Decimal("120.00")),
            ("SKU-TECL-03", "Teclado Mecânico RGB Switch Blue", 25, Decimal("350.00")),
            ("SKU-MONI-04", "Monitor Curvo 27 Pol 165Hz", 15, Decimal("1400.00")),
            ("SKU-HEAD-05", "Headset Gamer 7.1 Surround", 30, Decimal("280.00")),
            ("SKU-WEBC-06", "Webcam Full HD 1080p com Microfone", 40, Decimal("210.00")),
            ("SKU-CADE-07", "Cadeira Ergonômica Presidente", 8, Decimal("1100.00")),
            ("SKU-MESA-08", "Mesa Gamer com Regulagem de Altura", 5, Decimal("1850.00")),
            ("SKU-PADM-09", "Mousepad Speed Extra Grande 90x40cm", 60, Decimal("75.00")),
            ("SKU-SUPM-10", "Suporte Articulado a Gás para 2 Monitores", 20, Decimal("320.00")),
            ("SKU-SMAR-11", "Smartphone 128GB 5G Câmera Tripla", 12, Decimal("2400.00")),
            ("SKU-TABL-12", "Tablet 10 Pol 64GB com Caneta", 14, Decimal("1600.00")),
            ("SKU-FONE-13", "Fone Bluetooth TWS com Cancelamento de Ruído", 45, Decimal("190.00")),
            ("SKU-RELO-14", "Smartwatch Esportivo à Prova d'Água", 22, Decimal("450.00")),
            ("SKU-CAIX-15", "Caixa de Som Portátil Bluetooth 20W", 35, Decimal("230.00")),
            ("SKU-CABO-16", "Cabo HDMI 2.1 Ultra High Speed 2m", 80, Decimal("45.00")),
            ("SKU-PEND-17", "Pendrive 128GB USB 3.2", 100, Decimal("65.00")),
            ("SKU-SSDX-18", "SSD NVMe M.2 1TB 3500MB/s", 18, Decimal("420.00")),
            ("SKU-ROUT-19", "Roteador Wi-Fi 6 Gigabit Dual Band", 16, Decimal("380.00")),
            ("SKU-ESTB-20", "Estabilizador e Filtro de Linha 8 Tomadas", 0, Decimal("110.00")) # Sem estoque para testes de falta
        ]
        for sku, nome, qtd, preco in catalogo:
            self.cadastrar(sku, qtd, preco, nome)