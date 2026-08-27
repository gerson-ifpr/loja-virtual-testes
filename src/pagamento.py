"""
Módulo Pagamento - Processa pagamentos da loja virtual
"""

from decimal import Decimal
from typing import Optional, Dict, Any
from enum import Enum


class StatusPagamento(Enum):
    PENDENTE = "pendente"
    PROCESSANDO = "processando"
    APROVADO = "aprovado"
    RECUSADO = "recusado"
    CANCELADO = "cancelado"


class MetodoPagamento(Enum):
    CARTAO_CREDITO = "cartao_credito"
    CARTAO_DEBITO = "cartao_debito"
    PIX = "pix"
    BOLETO = "boleto"
    TRANSFERENCIA = "transferencia"


class Pagamento:
    def __init__(self):
        self._transacoes: Dict[str, Dict] = {}
        self._id_counter = 0
    
    def processar(self, valor: Decimal, metodo: MetodoPagamento,
                  dados: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        self._id_counter += 1
        transacao_id = f"TRX-{self._id_counter:06d}"
        if valor <= 0:
            return {"sucesso": False, "transacao_id": transacao_id,
                    "status": StatusPagamento.RECUSADO, "motivo": "Valor inválido"}
        aprovado = valor <= Decimal("10000")
        transacao = {
            "transacao_id": transacao_id,
            "valor": valor,
            "metodo": metodo.value,
            "dados": dados or {},
            "status": StatusPagamento.APROVADO if aprovado else StatusPagamento.RECUSADO,
            "motivo": None if aprovado else "Valor acima do limite"
        }
        self._transacoes[transacao_id] = transacao
        return transacao
    
    def obter_transacao(self, transacao_id: str) -> Optional[Dict[str, Any]]:
        return self._transacoes.get(transacao_id)
    
    def cancelar(self, transacao_id: str) -> bool:
        transacao = self._transacoes.get(transacao_id)
        if not transacao:
            return False
        if transacao["status"] in [StatusPagamento.APROVADO, StatusPagamento.PENDENTE]:
            transacao["status"] = StatusPagamento.CANCELADO
            return True
        return False