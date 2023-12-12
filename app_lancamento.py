from model import Session
from model.categoria import Categoria
from model.lancamento import Lancamento
from schemas.lancamento import LancamentoBuscaSchema, LancamentoSchema, \
                               apresenta_lancamento, apresenta_lancamentos


def create_lancamento(form: LancamentoSchema):

    """Adiciona um novo Lancamento à base de dados

    Retorna uma representação do Lancamento associado
    """

    try:
        categoria_id = form.categoria_id
        session = Session()
        categoria = session.query(Categoria).filter(Categoria.id == categoria_id).first()

        if not categoria:
            error_msg = "Categoria não encontrada na base :/"
            return {"message": error_msg}, 404

        lancamento = Lancamento(descricao=form.descricao, valor=form.valor, categoria=categoria)

        lancamento.date_str_to_date(form.data)
        session.add(lancamento)
        session.commit()

        return apresenta_lancamento(lancamento), 200

    except ValueError as e:
        return {"message": str(e)}, 409

    except Exception as e:
        error_msg = "Não foi possível salvar novo lançamento :/"
        return {"message": error_msg}, 400
    

def search_lancamentos():
    """Faz a busca por todos os lançamentos cadastrados

    Retorna uma representação da listagem de lançamentos
    """

    session = Session()

    # Retorna os lançamentos ordenados por data e data de inserção
    lancamentos = session.query(Lancamento).order_by(Lancamento.data.asc(),
                                                     Lancamento.data_insercao.asc() ).all()

    if not lancamentos:
        return {"lancamentos": []}, 200
    else:
        return apresenta_lancamentos(lancamentos), 200
    

def remove_lancamento(form: LancamentoBuscaSchema):
    """Deleta um Lancamento a partir do id informado

    Retorna uma mensagem de confirmação da remoção.
    """
    lancamento_id = form.id

    session = Session()
    lancamento_db = session.query(Lancamento).filter(Lancamento.id == lancamento_id).first()
    
    if not lancamento_db:
        error_msg = "Lançamento não encontrado na base :/"
        return {"message": error_msg}, 404

    count = session.query(Lancamento).filter(Lancamento.id == lancamento_id).delete()
    session.commit()

    if count:
        error_msg = "Lançamento removido!"
        status_msg = f"{lancamento_db.descricao} de valor R$ {lancamento_db.valor:.2f} em {lancamento_db.data.strftime('%d/%m/%Y')}"
        return {"message": error_msg, "descricao": status_msg}