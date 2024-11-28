from app import app
from flask import request, render_template, jsonify
from app.controllers.ControllerDatabase import *
from app.controllers.ControllerPrev import prev_top_artist

@app.route('/charts', methods=['GET'])
def charts():

    data_forecast = prev_top_artist()

    title_forecast = [item['artist'] for item in data_forecast]
    streams_forecast = [item['predicted_streams'] for item in data_forecast]

    data_2021 = get_datas_charts(2021).head(10)

    title_actual = data_2021['artist'].tolist()
    streams_actual = data_2021['total_streams'].tolist()

    return render_template('charts/charts.html', title_forecast=title_forecast, streams_forecast=streams_forecast, title_actual=title_actual, streams_actual=streams_actual)

@app.route('/charts/forecast', methods=['GET'])
def charts_forecast():
    data_forecast = prev_top_artist()
    title_forecast = [item['artist'] for item in data_forecast]
    streams_forecast = [item['predicted_streams'] for item in data_forecast]

    data_2021 = get_datas_charts(2021).head(10)
    title_actual = data_2021['artist'].tolist()
    streams_actual = data_2021['total_streams'].tolist()

    comparativo = []
    for i in range(len(title_forecast)):
        if title_forecast[i] in title_actual:
            idx = title_actual.index(title_forecast[i])
            comparativo.append({
                'artist': title_forecast[i],
                'predicted_streams': streams_forecast[i],
                'actual_streams': streams_actual[idx],
                'difference': streams_forecast[i] - streams_actual[idx]
            })
    
    return jsonify(comparativo)