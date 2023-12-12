from typing import List
from pydantic import BaseModel, validator
from model import Categoria


class CategoriaSchema(BaseModel):
    """ Define como uma nova Categoria a ser inserida deve ser representada
    """
    nome: str = "Salário"
    eh_receita: int = 1

class CategoriaDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    nome: str

class CategoriaViewSchema(BaseModel):
    """ Define como uma Categoria será retornada.
    """
    id: int = 1
    nome: str = "13o Salário"
    eh_receita: int = 1

class CategoriaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca, que será
        feita apenas com base no id da categoria.
    """
    id: int = 1

    @validator('id', pre=True, always=True)
    def valida_id(cls, valor):
        if not valor or valor == "":
            valor = 0
        return valor

class ListagemCategoriasSchema(BaseModel):
    """ Define como uma listagem de categorias será retornada.
    """
    categorias: List[CategoriaViewSchema]

def apresenta_categoria(categoria: Categoria):
    """ Retorna uma representação da Categoria seguindo o schema definido em
        CategoriaViewSchema.
    """
    return {
        "id": categoria.id,
        "nome": categoria.nome,
        "eh_receita": categoria.eh_receita
    }

def apresenta_categorias(categorias: List[Categoria]):
    """ Retorna uma representação das Categorias seguindo o schema definido em
        CategoriaViewSchema.
    """
    resultado = []
    for categoria in categorias:
        resultado.append({
            "id": categoria.id,
            "nome": categoria.nome,
            "eh_receita": categoria.eh_receita
        })

    return {"categorias": resultado}