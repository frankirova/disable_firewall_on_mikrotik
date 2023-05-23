from pymongo import MongoClient

client = MongoClient('mongodb+srv://franki:<password>@cluster0.sdqqh1u.mongodb.net/')
db = client['cortes-redmetro']

def addDoc(data):
    # Insertar los datos en la colección
    collection = db["cortes-redmetro"]  # Reemplaza "nombre_coleccion" con el nombre de tu colección
    document = {"datos": data}
    collection.insert_one(document)

# Datos a agregar
options = [
    "192.168.2.238",
    "64.76.121.146",
    "64.76.121.147",
    "64.76.121.143",
    "64.76.121.243",
    "168.194.32.50",
    "168.194.32.71",
    "168.194.32.21",
    "168.194.32.14",
    "168.194.34.196",
    "168.194.34.197",
]

# Llamada a la función addDoc
addDoc(options)

