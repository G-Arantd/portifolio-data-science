from app import db
from app.models.Database import Database
from sqlalchemy.sql import func
import pandas as pd

def get_all_data(start, end):
    return Database.query.slice(start, end).all()

def get_filtered_data(column, value, like=False):
    if like:
        return Database.query.filter(getattr(Database, column).like(f'{value}%')).all()
    return Database.query.filter_by(**{column: value}).all()

def get_aggregated_data(column=None, value=None, like=False):
    query = db.session.query(
        Database.title,
        Database.date,
        Database.artist,
        func.sum(Database.streams).label('total_streams')
    )

    if column and value:
        if like:
            query = query.filter(getattr(Database, column).like(f'{value}%'))
        else:
            query = query.filter_by(**{column: value})

    query = query.group_by(Database.title, Database.date, Database.artist)

    result = query.all()

    result_dicts = [
        {'title': row[0], 'date': row[1], 'artist': row[2], 'total_streams': row[3]} 
        for row in result
    ]

    expanded_result = []

    for record in result_dicts:
        artists = record['artist'].split(', ')  
        for artist in artists:
            expanded_result.append({
                'title': record['title'],
                'date': record['date'],
                'artist': artist,
                'total_streams': record['total_streams']
            })

    return expanded_result

def get_aggregated_all_data(start, end):
    data = get_aggregated_data()
    return data[start:end]

def get_aggregated_filtered_data(column, value, like=False):
    return get_aggregated_data(column, value, like)

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