import os
from flask import Flask, render_template, session, redirect, url_for, jsonify, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_table import Table, Col

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)#used for changing db structure
manager.add_command('db', MigrateCommand)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    score = db.Column(db.Integer, unique=False)
    users = db.relationship('Usuario', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    score = db.Column(db.Integer, unique=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User {0} Score {1}>'.format(self.username, self.score)

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class Results(Table):
    id = Col('Id', show=False)
    username = Col('username')
    score = Col('score')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/scoreboard', methods=['GET', 'POST'])
def scoreboard():
    if(session.get('name')):
        user = db.session.query(Usuario).filter_by(username = session.get('name'));
        print(user.first())
        scoreValue = request.form.get('score', 0)
        if(user.count() < 1):
            new_user = Usuario(username=session.get('name'), score=scoreValue)
            db.session.add(new_user)
            db.session.commit()
        else:
            if(user.first().score < int(scoreValue)):
                user.first().score = int(scoreValue)
                db.session.commit()

    results = []
    results = Usuario.query.order_by(Usuario.score.desc()).all()
    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        table = Results(results)
        table.border = True
        return render_template('scoreboard.html', table=table)

@app.route('/game')
def game():
    return render_template('game.html', name=session.get('name'),
                           known=session.get('known', False));

@app.route('/', methods=['GET', 'POST'])
def index():
    #print(User.query.all())
    form = NameForm()
    if form.validate_on_submit():
        session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('game'))

    return render_template('index.html', form=form, name=session.get('name'),
                           known=session.get('known', False))
if __name__ == '__main__':
    app.run()
    #manager.run()
