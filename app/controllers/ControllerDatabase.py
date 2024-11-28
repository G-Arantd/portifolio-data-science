from app import db
from app.models.Database import Database
from sqlalchemy.sql import func
import pandas as pd
import os

def get_datas_charts(year) -> pd.DataFrame:
    query = db.session.query(
        Database.artist,
        func.sum(Database.streams).label('total_streams')
    ).filter(
        Database.date.like(f'{year}%')
    ).group_by(Database.artist).order_by(
        func.sum(Database.streams).desc()
    )

    result = query.all()

    df = pd.DataFrame(result, columns=['artist', 'total_streams'])

    df_expanded = (
        df.assign(artist=df['artist'].str.split(','))
        .explode('artist')
        .assign(artist=lambda x: x['artist'].str.strip())
        .groupby('artist', as_index=False)['total_streams']
        .sum()
        .sort_values(by='total_streams', ascending=False)
    )

    return df_expanded

def get_data_analysis(year) -> pd.DataFrame:
    query = db.session.query(
        Database.artist,
        Database.date.label('month'),
        func.sum(Database.streams).label('total_streams')
    ).filter(
        Database.date.like(f'{year}-%')
    ).group_by(Database.artist, Database.date).order_by(
        func.sum(Database.streams).desc()
    )

    result = query.all()

    df = pd.DataFrame(result, columns=['artist', 'month', 'total_streams'])

    df_expanded = (
        df.assign(artist=df['artist'].str.split(','))
        .explode('artist')
        .assign(artist=lambda x: x['artist'].str.strip())
        .groupby(['artist', 'month'], as_index=False)['total_streams'].sum()
        .sort_values(by=['month', 'total_streams'], ascending=[True, False])
    )

    df_expanded['monthly_rank'] = df_expanded.groupby('month')['total_streams'].rank(
        method='dense', ascending=False
    )

    df_expanded['year'] = pd.to_datetime(df_expanded['month']).dt.year

    rank_annual = (
        df_expanded.groupby(['artist', 'year'], as_index=False)['total_streams']
        .sum()
        .assign(annual_rank=lambda x: x.groupby('year')['total_streams'].rank(
            method='dense', ascending=False
        ))
    )

    df_expanded = pd.merge(
        df_expanded, rank_annual[['artist', 'year', 'annual_rank']],
        on=['artist', 'year'], how='left'
    )

    return df_expanded

def extract_data():
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
    
def clear_data():
    
    file_path = "charts.csv"
    
    if not os.path.exists(file_path):
        raise Exception("Arquivo não encontrado")

    df = pd.read_csv(file_path)

    selected_columns = df[["title", "rank", "date", "artist", "region", "streams"]].copy()
    selected_columns['date'] = pd.to_datetime(selected_columns['date'])
    
    target_countries = ['Brazil', 'Argentina', 'Mexico', 'Uruguay']
    
    filtered_df = selected_columns[(selected_columns["region"].isin(target_countries)) & (selected_columns["rank"] <= 200)]
    filtered_df = filtered_df[filtered_df['streams'].notna() & (filtered_df['streams'] != '')]
    
    sorted_df = filtered_df.sort_values(by='date', ascending=True)
    sorted_df = sorted_df.drop(columns='rank')
    
    sorted_df.to_csv('instance/csv/data.csv', index=False)

    if os.path.exists('instance/csv/data.csv'):
        return {"message": "Arquivo foi limpo com sucesso"}