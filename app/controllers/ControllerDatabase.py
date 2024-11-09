from app import db
from app.models.Database import Database
import pandas as pd

def get_all_data(start, end):
    return Database.query.slice(start, end).all()

def get_filtered_data(column, value):
    return Database.query.filter_by(**{column: value}).all()

def create_data():
    file_path = 'instance/csv/data.csv'

    try:
        data = pd.read_csv(file_path)
        data_dicts = data.to_dict(orient='records')
        new_entries = [Database(**row) for row in data_dicts]
        db.session.bulk_save_objects(new_entries)
        db.session.commit()
        return {"message": "Arquivo foi adicionando no banco"}, 201
    except FileNotFoundError:
        return {"message": "Arquivo não encontrado"}, 404
    except Exception as e:
        return {"message": f"Ocorreu um erro: {str(e)}"}, 500

def delete_data():
    try:
        Database.query.delete()
        db.session.commit()
        return {"message": "Todos os dados foram deletados"}, 200
    except Exception as e:
        return {"message": f"Ocorreu um erro: {str(e)}"}, 500