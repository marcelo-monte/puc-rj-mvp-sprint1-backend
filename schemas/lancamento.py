from typing import List
from pydantic import BaseModel, validator
from model.lancamento import Lancamento

from schemas.categoria import CategoriaViewSchema, apresenta_categoria


class LancamentoViewSchema(BaseModel):
    """ Define como um Lancamento será retornado.
    """
    id: int = 1
    descricao: str = "Padaria Pãozinho"
    valor: float = 16.34
    data: str = "28/12/2023"
    categoria: CategoriaViewSchema

class LancamentoSchema(BaseModel):
    """ Define como um novo Lancamento a ser inserido deve ser representado
    """
    descricao: str = "Padaria Pãozinho"
    valor: float = 22.34
    data: str = "05/12/2023"
    categoria_id: int = 1

    @validator('valor', pre=True, always=True)
    def valida_valor(cls, valor):
        if not valor or valor == "":
            valor = 0
        return valor

    @validator('categoria_id', pre=True, always=True)
    def valida_categoria_id(cls, valor):
        if not valor or valor == "":
            valor = 0
        return valor

class ListagemLancamentosSchema(BaseModel):
    """ Define como uma listagem de lançamentos será retornada.
    """
    lancamentos: List[LancamentoViewSchema]

class LancamentoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    descricao: str

class LancamentoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca, que será
        feita apenas com base no id do lançamento.
    """
    id: int = 1

    @validator('id', pre=True, always=True)
    def valida_id(cls, valor):
        if not valor or valor == "":
            valor = 0
        return valor

def apresenta_lancamento(lancamento: Lancamento):
    """ Retorna uma representação do Lancamento seguindo o schema definido em
        LancamentoViewSchema.
    """
    return {
        "id": lancamento.id,
        "descricao": lancamento.descricao,
        "valor": f"{lancamento.valor:.2f}",
        "data": lancamento.data.strftime('%d/%m/%Y'),
        "categoria": apresenta_categoria(lancamento.categoria)
    }

def apresenta_lancamentos(lancamentos: List[Lancamento]):
    """ Retorna uma representação dos lançamentos seguindo o schema definido em
        LancamentoViewSchema.
    """
    resultado = []
    for lancamento in lancamentos:
        resultado.append({
            "id": lancamento.id,
            "descricao": lancamento.descricao,
            "valor": f"{lancamento.valor:.2f}",
            "data": lancamento.data.strftime('%d/%m/%Y'),
            "categoria": apresenta_categoria(lancamento.categoria)
        })

    return {"lancamentos": resultado}