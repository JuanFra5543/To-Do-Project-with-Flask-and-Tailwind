from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Creation of the list
class Task(db.Model):
    __tablename__ = 'task'
    id_task = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name_task = db.Column(db.String(100),nullable=False)
    created_at_task= db.Column(db.DateTime,nullable=False, default=datetime.now)

    def __repr__(self):
       return f'To-Do : {self.name_task}'


#Home page and add method
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        name = request.form['name']
        new_task = Task(name_task=name)
        db.session.add(new_task)
        db.session.commit()
        return redirect('/')
    else:
        tasks = Task.query.order_by(Task.created_at_task)
    return render_template("home.html",tasks=tasks)

#Remove function
@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.get_or_404(id)

    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except Exception:
        return "There was a problem deleting the task"

#Update function
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Task.query.get_or_404(id)

    if request.method == 'POST':
        task.name_task = request.form['name']
        try:
            db.session.commit()
            return redirect('/')
        except Exception:
            return "There was a problem updating the task"
    else:
        title = "Update Task"
        return render_template('update.html', title=title, task=task)

if __name__ == "__main__":
    app.run(debug=True)