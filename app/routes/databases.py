from app import app
from flask import request, render_template
from app.controllers.ControllerDatabase import get_all_data, get_filtered_data, create_data, delete_data

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
    # Obter os dados de título e streams do banco de dados
    dados = get_all_data(0, 100)

    # Separar os dados para o gráfico
    titulos = [dado.title for dado in dados]
    streams = [dado.streams for dado in dados]

    # Retornar os dados como um JSON para o frontend
    return render_template('charts/charts.html', titulos=titulos, streams=streams)