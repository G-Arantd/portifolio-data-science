from app import app
from flask import request, render_template, jsonify
from app.controllers.ControllerDatabase import get_all_data, get_filtered_data, get_aggregated_filtered_data, create_data, delete_data

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import pandas as pd

@app.route('/database/<int:page>', methods=['GET', 'POST'])
def database(page):

    first_row = 0
    last_row = 199

    if page > 1:
        first_row = 1 + (200 * page)
        last_row = page * 200

    datas = get_all_data(first_row, last_row)

    if request.method == 'POST':
        pass

    return render_template('databases/database.html', datas=datas)

@app.route('/database/update', methods=['POST'])
def update_database():
    try:
        delete_data()
        create_data()
        return {'success': True}
    except Exception as e:
        print(f"Error updating database: {e}")
        return {'success': False}
        
@app.route('/charts', methods=['GET'])
def charts():

    dados_analise = prev_top_artist()

    titulos_analise = [item['artist'] for item in dados_analise]
    streams_analise = [item['predicted_streams'] for item in dados_analise]

    dados_true = get_aggregated_filtered_data('date', '2021', like=True)

    df = pd.DataFrame(dados_true)
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m')
    df['year'] = df['date'].dt.year

    dados_aggregated = df.groupby('artist')['total_streams'].sum().reset_index()
    dados_sorted = dados_aggregated.sort_values(by='total_streams', ascending=False).head(10)

    titulos = dados_sorted['artist'].tolist()
    streams = dados_sorted['total_streams'].tolist()

    return render_template('charts/charts.html', titulos=titulos, streams=streams, titulos_analise=titulos_analise, streams_analise=streams_analise)

def prev_top_artist():
    years = ['2017', '2018', '2019', '2020']
    data_frames = [pd.DataFrame(get_aggregated_filtered_data('date', year, like=True)) for year in years]
    
    df = pd.concat(data_frames)
    
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m')
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['quarter'] = df['date'].dt.quarter

    artist_year_streams = df.groupby(['artist', 'year'])['total_streams'].sum().reset_index()

    artist_year_streams['rolling_mean'] = artist_year_streams.groupby('artist')['total_streams'].transform(lambda x: x.rolling(window=6, min_periods=1).mean())

    artist_year_streams['streams_growth'] = artist_year_streams.groupby('artist')['total_streams'].pct_change().fillna(0)

    train_data = artist_year_streams[artist_year_streams['year'] <= 2020]
    test_data = artist_year_streams[artist_year_streams['year'] == 2020]

    X_train = train_data[['year', 'streams_growth', 'rolling_mean']]
    y_train = train_data['total_streams']

    X_test = test_data[['year', 'streams_growth', 'rolling_mean']]
    y_test = test_data['total_streams']

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    test_data['predicted_streams'] = y_pred
    top_10_artists = test_data.sort_values(by='predicted_streams', ascending=False).head(10)

    result = top_10_artists[['artist', 'predicted_streams']]

    print(f'MAE: {mae}')
    print(f'R²: {r2}')
    
    json_result = result.to_dict(orient='records')

    return json_result
