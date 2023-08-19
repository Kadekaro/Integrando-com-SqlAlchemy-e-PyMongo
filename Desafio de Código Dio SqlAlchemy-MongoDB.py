from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine, select
from sqlalchemy.orm import declarative_base, Session, relationship

Base = declarative_base()

"""
Classe do cliente
"""


class Client(Base):
    __tablename__ = "client"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    cpf = Column(String)
    address = Column(String)
    conta = relationship('Conta', back_populates='client')

    def __repr__(self):
        return f"Cliente: ID={self.id}, Nome={self.name}, CPF={self.cpf}"


"""
Classe da conta do cliente
"""


class Conta(Base):
    __tablename__ = "conta"
    id = Column(Integer, primary_key=True)
    type = Column(String)
    agency = Column(String)
    num = Column(Integer)
    id_cliente = Column(Integer, ForeignKey("client.id"))
    balance = Column(Float)
    client = relationship('Client', back_populates='conta')

    def __repr__(self):
        return f"Conta: Tipo={self.type}, Agência={self.agency}, N°={self.num}, Saldo{self.balance}"


engine = create_engine("sqlite+pysqlite:///:memory:")
Base.metadata.create_all(engine)

with Session(engine) as session:
    Wesley = Client(
        name='Wesley',
        cpf='00000000011',
        address='qualquercoisa@gmail.com',
        conta=[Conta(type="Pessoa Física", agency="Nubank", num=374840, balance=400.00)]
    )

    Nelsa = Client(
        name='Nelsa',
        cpf='00000000012',
        address='qualquercoisa1@gmail.com',
        conta=[Conta(type="Pessoa Jurídica", agency="Citi Bank", num=3744572, balance=10000000)]
    )

    Joao = Client(
        name='João',
        cpf='00000000013',
        address='qualquercoisa2@gmail.com',
        conta=[Conta(type="Pessoa Física", agency="Sicoob", num=3748, balance=700.00)]
    )

    session.add_all([Wesley, Nelsa, Joao])

    session.commit()

print('\nRetorna os clientes por nome:')
stmt = select(Client).where(Client.name.in_(["Wesley", "Nelsa"]))
for cliente in session.scalars(stmt):
    print(cliente)

print('\nRetorna os clientes com saldo entre 20 a 1000 reais:')
stmt = select(Client).join(Conta).where(Conta.balance.between(20, 1000))
for cliente in session.scalars(stmt):
    print(cliente)

print('\nRetorna os clientes com saldo acima de 1000 reais:')
stmt = select(Client).join(Conta).filter(Conta.balance < 500)
for cliente in session.scalars(stmt):
    print(cliente)
