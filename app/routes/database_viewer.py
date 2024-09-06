from flask import jsonify
from app import app

from app.services.database_services import get_all, create_from_csv

import pandas as pd

@app.route('/view_database')
def view_database():

    # df = pd.read_csv("app/database/charts.csv")

    # df_filtered = df[["rank", "title", "artist", "region", "streams"]]

    # df_argentina = df_filtered[(df_filtered["region"] == "Argentina") & (df_filtered["rank"] <= 10)]

    # data = create_from_csv(df_argentina)

    # print(data)
    
    result = get_all()

    return jsonify({"data": result})
