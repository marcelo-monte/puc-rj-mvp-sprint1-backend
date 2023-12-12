from sqlite3 import IntegrityError
from model import Categoria, Session
from model.lancamento import Lancamento
from schemas import *


def create_categoria(form: CategoriaSchema):

    """Adiciona uma nova Categoria à base de dados

    Retorna uma representação da Categoria associada.
    """

    try:
        categoria = Categoria(
        nome=form.nome,
        eh_receita=form.eh_receita)

        session = Session()
        session.add(categoria)
        session.commit()

        return apresenta_categoria(categoria), 200

    except IntegrityError as e:
        error_msg = "Categoria de mesmo nome e tipo já salva na base :/"
        return {"message": error_msg}, 409
    
    except ValueError as e:
        return {"message": str(e)}, 409

    except Exception as e:
        error_msg = "Não foi possível salvar nova categoria :/"
        return {"message": error_msg}, 400


def search_categorias():
    """Faz a busca por todas as Categorias cadastradas

    Retorna uma representação da listagem de Categorias, subdivididas em
    despesas e receitas.
    """

    session = Session()

    # Retorna as Categorias ordenadas por eh_receita e nome (despesas primeiro)
    categorias = session.query(Categoria).order_by(Categoria.eh_receita.asc(),
                                                   Categoria.nome.asc() ).all()

    if not categorias:
        return {"categorias": []}, 200
    else:
        return apresenta_categorias(categorias), 200


def remove_categoria(form: CategoriaBuscaSchema):
    """Deleta uma Categoria a partir do id informado

    Retorna uma mensagem de confirmação da remoção.
    """
    categoria_id = form.id

    session = Session()
    categoria_db = session.query(Categoria).filter(Categoria.id == categoria_id).first()
    
    if not categoria_db:
        error_msg = "Categoria não encontrada na base :/"
        return {"message": error_msg}, 404

    lancamentos_count = session.query(Lancamento).filter(Lancamento.categoria_id == categoria_id).count()

    if lancamentos_count:
        error_msg = "Categoria não pode ser removida porque existem lançamentos associados :/"
        return {"message": error_msg}, 409

    count = session.query(Categoria).filter(Categoria.id == categoria_id).delete()
    session.commit()

    if count:
        if categoria_db.eh_receita:
            error_msg = "Receita removida!"
        else:
            error_msg = "Despesa removida!"

        return {"message": error_msg, "nome": categoria_db.nome}