import pymongo
import pymongo as pym
import pprint

from bson import ObjectId

# Conectando ao cluster MongoDB
client = pym.MongoClient("mongodb+srv://kadekaro:<password>@clusterteste.zjv7moo.mongodb.net/?retryWrites=true&w"
                         "=majority")

# Acessando o banco de dados e a coleção
db = client.test
posts = db.posts

# Imprimindo todos os documentos da coleção 'posts'
print("Documentos na coleção 'posts':")
for post in posts.find():
    pprint.pprint(post)

# Contando o número total de documentos na coleção 'posts'
print("\nTotal de documentos na coleção 'posts':", posts.count_documents({}))

# Contando o número de documentos na coleção 'posts' com o autor 'Márcia'
print("Total de documentos na coleção 'posts' com autor 'Márcia':", posts.count_documents({"author": "Márcia"}))

# Contando o número de documentos na coleção 'posts' com a tag 'bulk'
print("Total de documentos na coleção 'posts' com tag 'bulk':", posts.count_documents({"tags": "bulk"}))

# Encontrando um documento com a tag 'insert'
pprint.pprint(posts.find_one({"tags": "insert"}))

# Recuperando informações da coleção 'posts' de maneira ordenada por data
print("\nRecuperando informações da coleção 'posts' de maneira ordenada por data:")
for post in posts.find({}).sort("date"):
    pprint.pprint(post)

# Criando um índice único na coleção 'profiles' para a chave 'author'
result = db.profiles.create_index([('author', pymongo.ASCENDING)], unique=True)
print(sorted(list(db.profiles.index_information())))

# Inserindo documentos na coleção 'profile_user'
user_profile_user = [{'user_id': 211, 'name': 'Luke'},
                     {'user_id': 212, 'name': 'wesley'}]
results = db.profile_user.insert_many(user_profile_user)

# Listando as coleções armazenadas no MongoDB
print("\nColeções armazenadas no MongoDB:")
collections = db.list_collection_names()
for collection in collections:
    print(collection)

# Deletando um documento com o autor 'Wesley' da coleção 'posts'
posts.delete_one({"author": "Wesley".strip()})

# Supondo que o _id seja ObjectId('64de23fc970adf909fde5e36')
posts.delete_one({"_id": ObjectId('64de23fc970adf909fde5e36')}) # -> excluiu o usuário Wesley pelo ObjectID

# Imprimindo os documentos restantes na coleção 'posts' após a exclusão
print("\nDocumentos na coleção 'posts' após a exclusão:")
for post in posts.find():
    pprint.pprint(post)

# client.drop_database('test') # Exclui o banco de dados
