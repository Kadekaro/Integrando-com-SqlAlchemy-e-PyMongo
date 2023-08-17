from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

engine = create_engine('sqlite:///C:/Users/kadek/Downloads/integration_with_sqlalchemy/integrationWithSql/testeDB.db')
connection = engine.connect()
metadata = MetaData()
user = Table(
    'user',
    metadata,
    Column('user_id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(40), nullable=False),
    Column('email_address', String(60)),
    Column('nick_name', String(50), nullable=False)
)

user_prefers = Table(
    'user_prefers',
    metadata,
    Column('prefer_id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('user.user_id'), nullable=False),
    Column('prefer_name', String(50), nullable=False),
    Column('prefer_value', String(100))
)


print('\nInfo da tabela user_prefers:')
print(user_prefers.primary_key)
print(user_prefers.constraints)

for table in metadata.sorted_tables:  # SAÍDA: teste.user
    print(f'\n{table}')  # SAÍDA: teste.user_prefers


metadata = MetaData()
financial_Info = Table(
    'financial_Info',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('value', String(100), nullable=False)
)

metadata.create_all(engine)

# Inserir um usuário
sql_insert = text("insert into user values(1, 'Wesley', 'email@gmail.com', 'Wesley')")
connection.execute(sql_insert)

# Confirmar a inserção
connection.commit()

print('\nInfo da tabela financial_Info:')
print(financial_Info.primary_key)
print(financial_Info.constraints)

print('\nImprimindo as informações do schema MetaData:')
print(metadata.tables)

# Consultar usuários
print('\nExecutando statement SQL:')
sql = text('SELECT * FROM "user"')
result = connection.execute(sql)

for row in result:
    print(row)

# Fechar a conexão
connection.close()
