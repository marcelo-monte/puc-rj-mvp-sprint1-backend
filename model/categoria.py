from typing import Union
from sqlalchemy import CheckConstraint, Column, DateTime, Integer, String, UniqueConstraint, func, text
from sqlalchemy.orm import validates, relationship

from model import Base

class Categoria(Base):
    __tablename__ = "categoria"

    id = Column("pk_categoria", Integer, primary_key=True)
    nome = Column(String(30), nullable=False)
    nome_normalizado = Column(String(30), nullable=False)

    # 0 = despesa
    # 1 = receita
    eh_receita = Column(Integer, nullable=False)
    CheckConstraint(eh_receita.in_([0, 1]), name="ck_eh_receita")

    data_insercao = Column(DateTime, default=func.now())

    # Permite termos uma despesa e uma receita com mesmo nome
    UniqueConstraint(eh_receita, nome_normalizado, name='idx_nome_eh_receita')

    lancamentos = relationship("Lancamento", back_populates="categoria")

    @validates("nome")
    def valida_nome(self, chave, valor):
        if len(valor) < 1:
            raise ValueError("Nome deve ter pelo menos um caractere.")
        return valor

    @validates("eh_receita")
    def valida_eh_receita(self, chave, valor):
        if valor not in [0, 1]:
            raise ValueError("eh_receita só pode ser 1 (receita) ou 0 (despesa) :/")
        return valor

    def __init__(self, nome:str, eh_receita: int, data_insercao: Union[DateTime, None] = None):
        """
        Cria uma Categoria

        Arguments:
            nome: o nome da categoria
            eh_receita: indica se é uma categoria de despesa (False)
                        ou se é uma categoria de receita (True)
            data_insercao: data de inserção da categoria no BD
        """
        self.set_nome(nome)
        self.eh_receita = eh_receita
        
        if data_insercao:
            self.data_insercao = data_insercao
    

    def set_nome(self, nome: str):
        """ Seta o nome dessa Categoria, ajustando também o nome
            normalizado.
        """
        self.nome = nome
        self.nome_normalizado = self.normalizar_nome()


    def normalizar_nome(self):
        """ Normaliza uma string, removendo os acentos e convertendo
            para lower case.
        """

        # Tabela de conversão para normalizar os nomes, removendo os acentos
        normalMap = {'À': 'A', 'Á': 'A', 'Â': 'A', 'Ã': 'A', 'Ä': 'A',
                     'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a', 'ª': 'A',
                     'È': 'E', 'É': 'E', 'Ê': 'E', 'Ë': 'E',
                     'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e',
                     'Í': 'I', 'Ì': 'I', 'Î': 'I', 'Ï': 'I',
                     'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
                     'Ò': 'O', 'Ó': 'O', 'Ô': 'O', 'Õ': 'O', 'Ö': 'O',
                     'ò': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o', 'º': 'O',
                     'Ù': 'U', 'Ú': 'U', 'Û': 'U', 'Ü': 'U',
                     'ù': 'u', 'ú': 'u', 'û': 'u', 'ü': 'u',
                     'Ñ': 'N', 'ñ': 'n',
                     'Ç': 'C', 'ç': 'c',
                     '§': 'S',  '³': '3', '²': '2', '¹': '1'}
    
        # Usado para a remoção dos acentos
        normalizar = str.maketrans(normalMap)

        return self.nome.translate(normalizar).strip().lower()