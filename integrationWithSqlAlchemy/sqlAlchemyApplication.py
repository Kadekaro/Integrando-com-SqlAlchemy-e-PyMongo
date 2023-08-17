from sqlalchemy import Column, create_engine, Integer, String, ForeignKey, inspect, select, func
from sqlalchemy.orm import declarative_base, relationship, Session

Base = declarative_base()


class User(Base):
    # Atributos:
    __tablename__ = "user_account"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    lastName = Column(String)
    fullName = Column(String)
    age = Column(Integer)
    address = relationship(
        "Address", back_populates="user", cascade="all, delete"
    )

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, lastName={self.lastName}, fullName={self.fullName})"


class Address(Base):
    # Atributos:
    __tablename__ = "address"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email_address = Column(String(40), nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"))
    user = relationship(
        "User", back_populates="address"
    )

    def __repr__(self):
        return f"Address(id={self.id}, email={self.email_address})"


# conexão com o banco de dados:
engine = create_engine("sqlite://")

# criando as classes como tabelas no banco de dados:
Base.metadata.create_all(engine)

# depreciando - será removido em um futuro release(liberar):
insp = inspect(engine)

# criando uma sessão e colocando os dados das pessoas no sqlite:
with Session(engine) as session:
    wesley = User(
        name='wesley',
        lastName='Kadekaro',
        fullName="Wesley Kadekaro",
        age=31,
        address=[Address(email_address='kadekaro@email.com')]
    )

    julia = User(
        name='julia',
        lastName='Pereira',
        fullName="Julia Pereira",
        age=52,
        address=[Address(email_address='juliaPereira@email.com')]
    )

    sandy = User(
        name='sandy',
        lastName='& Junior',
        fullName='Sandy & Junior',
        age=53,
        address=[Address(email_address='Sandy&Junior@email.com'),
                 Address(email_address='DuplaDinamica@email.com')]
    )

    patrick = User(
        name='patrick',
        lastName='BobEsponja',
        fullName='Patrick BobEsponja'
    )

    # enviando os dados para o BD:
    session.add_all([wesley, julia, sandy, patrick])

    session.commit()

stmt = select(User).where(User.name.in_(["wesley", "julia"]))
print("\nRecuperando usuário a partir de uma filtragem")
for user in session.scalars(stmt):
    print(user)

stmt_address = select(Address).where(Address.user_id.in_([2]))
print('\nRecuperando os endereços de email de julia')
for address in session.scalars(stmt_address):
    print(address)

stmt_order = select(User).order_by(User.fullName.desc())  # ordenando de forma decrescente o fullName
print("\nRecuperando informações de maneira ordenada:")
for result in session.scalars(stmt_order):
    print(result)

#   stmt = select(User, (User.name + ' ' + User.lastName).label('fullname')).order_by(desc("fullname"))
# for result in session.execute(stmt):
#     print(result)

stmt_join = select(User.fullName, Address.email_address).join_from(Address, User)
print("\nExecutando um JOIN do nome completo e do email:")
for result in session.scalars(stmt_join):
    print(result)

connection = engine.connect()
results = connection.execute(stmt_join).fetchall()
print("\nExecutando statement a partir da connection:")
for result in results:
    print(result)

stmt_count = select(func.count('*')).select_from(User)
print("\nExecutando uma contagem dos statement:")
for result in session.scalars(stmt_count):
    print(result)
