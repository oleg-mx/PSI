from flask import Flask, render_template, url_for, send_from_directory, send_file
from flask_wtf import FlaskForm
from wtforms import SearchField, StringField, SubmitField
from wtforms.validators import DataRequired
import sqlite3
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess1'


class SearchForm(FlaskForm):
    search = SearchField('Поиск', validators=[DataRequired()])
    # string = StringField('Текст', validators=[DataRequired()])
    submit = SubmitField('Поиск')


@app.errorhandler(404)
def pageNotFount(error):
    return render_template('page404.html', title='Страница не найдена')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/psi', methods=['GET', 'POST'])
def psi():
    form = SearchForm()
    if form.search.data is None:
        query = """SELECT * FROM files"""
    else:
        query = """SELECT * FROM files
        WHERE FileNames like '%""" + form.search.data + """%'
        """
    conn = sqlite3.connect(r'data/data.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    # rows = cur.execute(query).fetchall()
    rows = cur.execute(query).fetchmany(100)
    return render_template('psi.html', rows=rows, form=form)


@app.route('/test', methods=['GET', 'POST'])
def test():
    form = SearchForm()
    if form.search.data is None:
        query = """SELECT * FROM files"""
    else:
        query = """SELECT * FROM files
        WHERE FileNames like '%""" + form.search.data + """%'
        """
    conn = sqlite3.connect(r'data/data.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    rows = cur.execute(query).fetchall()
    # rows = cur.execute(query).fetchmany(100)
    return render_template('test.html', rows=rows, form=form)


@app.route('/open/<year>/<filename>')
def download_file(year, filename):
    # def download_file():
    p = r'D:\WORK\oformitel\END'
    # p = path
    y = year
    f = filename
    pyf = os.path.join(p, y, f)
    return send_file(pyf, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
