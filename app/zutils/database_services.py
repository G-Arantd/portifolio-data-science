from app.models.datafilter import DataFilter, db

def get_all():
    try:
        data = DataFilter.query.all()
        
        return [{"rank": d.rank, "title": d.title, "artist": d.artist, "region": d.region, "streams": d.streams} for d in data]
        
    except Exception as e:
        print(f"Erro ao buscar todos os registros: {e}")
        return "[]"

def create_from_csv(dataframe):
    try:
        registros = dataframe.to_dict(orient='records')

        objetos_para_inserir = [
            DataFilter(
                rank=registro['rank'],
                title=registro['title'],
                artist=registro['artist'],
                region=registro['region'],
                streams=registro['streams']
            ) for registro in registros
        ]

        db.session.bulk_save_objects(objetos_para_inserir)
        db.session.commit()
        return {"status": "sucesso", "mensagem": "Dados inseridos com sucesso!"}
    
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao inserir dados: {e}")
        return {"status": "erro", "mensagem": f"Erro ao inserir dados: {e}"}