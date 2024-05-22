from flask import Flask, render_template, request, make_response, redirect, url_for


app = Flask(__name__)


@app.route('/index/')
def html_index():
    return render_template('index.html')

@app.route('/clothes/')
def html_clothes():
    return render_template('clothes.html')

@app.route('/jacket/')
def html_jacket():
    return render_template('jacket.html')

@app.route('/shoes/')
def html_shoes():
    return render_template('shoes.html')

@app.route('/submit/', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        name = request.form.get('name')
        #email = request.form.get('email')
        response = make_response("Cookie установлен")
        response.set_cookie('name', 'email')
        return redirect(url_for('exit'))
    return render_template('form.html')

@app.route('/exit/', methods=['GET', 'POST'])
def exit():
    if request.method == 'POST':
        name = request.form.get('name')
        #email = request.form.get('email')
        res = make_response("Cookie удалён")
        res.set_cookie('0', '0', max_age=0)
        return f'Hello {name}!'
    return render_template('exit.html')

if __name__ == '__main__':
    app.run()