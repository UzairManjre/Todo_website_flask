from flask import Flask, request, render_template, redirect
from pymongo import MongoClient
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    SNo = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno}-{self.title}-{self.desc}"


@app.route('/', methods=['GET', 'POST'])
def HelloWorld():
    if request.method == 'POST':
        todo = Todo(Title=request.form['taskName'], desc=request.form['taskDescription'])
        db.session.add(todo)
        db.session.commit()
    try:
        todo = Todo()
        todo_all = todo.query.all()

        return render_template('index.html', todo_all=todo_all)
    except:
        return render_template('index.html')


@app.route('/update/<int:SNo>', methods=['GET', 'POST'])
def Update(SNo):

    if request.method == 'POST':
        title = request.form['taskName']
        description = request.form['taskDescription']
        todoUpdate = Todo.query.filter_by(SNo=SNo).first()
        todoUpdate.Title = title
        todoUpdate.desc = description
        db.session.add(todoUpdate)
        db.session.commit()
        print(todoUpdate.Title + " " + todoUpdate.desc)
        return redirect('/')


    todoUpdate = Todo.query.filter_by(SNo=SNo).first()
    return render_template('/update.html', todo=todoUpdate)




@app.route('/delete/<int:SNo>', methods=['GET', 'POST'])
def delete(SNo):
    try:
        todo_del = Todo.query.filter_by(SNo=SNo).first()
        db.session.delete(todo_del)
        db.session.commit()
        return redirect('/')
    except:
        return redirect('/')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
