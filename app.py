from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    attribute = db.Column(db.String(50))
    description = db.Column(db.Text)

@app.route('/')
def index():
    characters = Character.query.all()
    return render_template('index.html', characters=characters)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        attribute = request.form['attr']
        description = request.form['description']

        new_character = Character(name=name, attribute=attribute, description=description)
        db.session.add(new_character)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    character = Character.query.get(id)

    if request.method == 'POST':
        if name := request.form.get('name'):
            character.name = name
        else:
            print("error")
        character.attribute = request.form['attr']
        character.description = request.form['description']

        db.session.commit()

        return redirect(url_for('index'))

    return render_template('edit.html', character=character)

@app.route('/delete/<int:id>')
def delete(id):
    character = Character.query.get(id)
    db.session.delete(character)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
