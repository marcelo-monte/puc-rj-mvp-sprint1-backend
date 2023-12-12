from datetime import datetime
from decimal import Decimal
from typing import Union
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, Numeric, String, func, text
from sqlalchemy.orm import validates, relationship

from model import Base, Categoria


class Lancamento(Base):
    __tablename__ = "lancamento"

    id = Column(Integer, primary_key=True)
    descricao = Column(String(30), nullable=False)
    valor = Column(Numeric(precision=10, scale=2), nullable=False)
    data = Column(Date, server_default=text("CURRENT_DATE"))

    categoria_id = Column(Integer, ForeignKey("categoria.pk_categoria"), nullable=False)
    
    data_insercao = Column(DateTime, default=func.now())

    categoria = relationship('Categoria', back_populates='lancamentos')

    @validates("descricao")
    def valida_descricao(self, chave, valor):
        if len(valor) < 1:
            raise ValueError("Descricao deve ter pelo menos um caractere.")
        return valor
    
    @validates("valor")
    def valida_valor(self, chave, valor):
        if not valor or valor <= 0:
            raise ValueError("Valor deve ser positivo, inclusive para despesas.")
        return valor

    def __init__(self, descricao:str, valor: Decimal, categoria: Categoria,
                 data: Union[Date, None] = None, data_insercao: Union[DateTime, None] = None):
        """
        Cria um Lancamento

        Arguments:
            descricao: a descrição do lançamento
            valor: o valor do lançamento. Se for uma despesa, deve ser negativo.
            data: a data/hora associada a este lançamento, permitindo informar
                       lançamento no passado e no futuro. Se não for informada, usa
                       a data de hoje
            categoria: a categoria desse Lancamento
            data_insercao: data de inserção da categoria no BD
        """
        self.descricao = descricao
        self.valor = valor
        self.data = data
        self.categoria = categoria
        
        if data_insercao:
            self.data_insercao = data_insercao
        
        if data:
            self.data = data
        

    def date_str_to_date(self, data_str: str):
        try:
            self.data = datetime.strptime(data_str, '%d/%m/%Y').date()
        except (ValueError, TypeError):
            raise ValueError('Informe uma data no formato DD/MM/YYYY') from None