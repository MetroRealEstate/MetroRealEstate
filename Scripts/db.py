from pymongo import MongoClient

def get_mongodb_connection():
    try:
        # Establecer la conexión a la base de datos de MongoDB
        client = MongoClient('mongodb://localhost:27017/')

        # Seleccionar la base de datos
        db = client['Metro']

        return db
    except Exception as e:
        print("Error connecting to MongoDB:", str(e))
        return None

def save_data_to_mongodb(data):
    # Obtener la conexión a la base de datos de MongoDB
    db = get_mongodb_connection()

    # Guardar los datos en MongoDB
    collection = db['Moreno Valley']
    collection.insert_one(data)