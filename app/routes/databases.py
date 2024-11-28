from app import app
from flask import request, render_template, flash, jsonify
from app.controllers.ControllerDatabase import *

@app.route('/database', methods=['GET'])
def database():
    try:
        datas = get_datas_charts(2021).head(50).to_dict(orient='records')
    except Exception:
        flash('Erro ao carregar os dados do banco de dados', 'danger')
        datas = []

    return render_template('databases/database.html', datas=datas)

@app.route('/database/clear', methods=['POST'])
def clear_database():
    try:
        clear_data()
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
@app.route('/database/update', methods=['POST'])
def update_database():
    try:
        delete_data()
        extract_data()
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

