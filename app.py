from flask import redirect
from flask_openapi3 import OpenAPI, Info, Tag

from schemas import *
from flask_cors import CORS

from app_categoria import create_categoria, search_categorias, remove_categoria
from app_lancamento import create_lancamento, remove_lancamento, search_lancamentos

info = Info(title="API de Finanças Pessoais", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)


# Definindo as tags do OpenAPI
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
lancamento_tag = Tag(name="Lançamento", description="Operações relacionadas a Lançamentos")
categoria_tag = Tag(name="Categoria", description="Operações relacionadas a Categorias de Lançamentos")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


###### Rotas referentes a categorias
@app.post('/categoria', tags=[categoria_tag],
          responses={"200": CategoriaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_categoria(form: CategoriaSchema):

    """Adiciona uma nova Categoria à base de dados

    Retorna uma representação da Categoria associada.
    """
    return create_categoria(form)


@app.get('/categorias', tags=[categoria_tag],
         responses={"200": ListagemCategoriasSchema, "404": ErrorSchema})
def get_categorias():
    """Faz a busca por todas as Categorias cadastradas

    Retorna uma representação da listagem de Categorias, subdivididas em
    despesas e receitas.
    """

    return search_categorias()


@app.delete('/categoria', tags=[categoria_tag],
            responses={"200": CategoriaDelSchema, "404": ErrorSchema})
def del_categoria(form: CategoriaBuscaSchema):
    """Deleta uma Categoria a partir do id informado

    Retorna uma mensagem de confirmação da remoção.
    """

    return remove_categoria(form)


###### Rotas referentes a lançamentos
@app.post('/lancamento', tags=[lancamento_tag],
          responses={"200": LancamentoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_lancamento(form: LancamentoSchema):

    """Adiciona um novo Lancamento à base de dados

    Retorna uma representação do Lancamento associado.
    """
    return create_lancamento(form)


@app.get('/lancamentos', tags=[lancamento_tag],
         responses={"200": ListagemLancamentosSchema, "404": ErrorSchema})
def get_lancamentos():
    """Faz a busca por todos os lançamentos cadastrados

    Retorna uma representação da listagem de lançamentos
    """

    return search_lancamentos()


@app.delete('/lancamento', tags=[lancamento_tag],
            responses={"200": LancamentoDelSchema, "404": ErrorSchema})
def del_lancamento(form: LancamentoBuscaSchema):
    """Deleta um Lancamento a partir do id informado

    Retorna uma mensagem de confirmação da remoção.
    """

    return remove_lancamento(form)