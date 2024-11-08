from app import app
from flask import request, render_template
from app.controllers.ControllerDatabase import ControllerDatabase

@app.route('/database', methods=['GET', 'POST'])
def database():

    if request.method == 'POST':
        pass



    return render_template('database.html')