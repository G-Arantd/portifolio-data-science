from models.Database import Database

def get_all_data():
    return Database.query.all()

def get_filtered_data(filter):
    return Database.query.filter_by(filter=filter).all()