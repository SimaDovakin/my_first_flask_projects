from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test.sqlite3'
app.config["SECRET_KEY"] = ')7m2R@7-46@gak88G()HSEY&t)3eTcHz'
db = SQLAlchemy(app)

# this model of task for task manager
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Task {self.id}>"


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        task_content = request.form['task']
        task = Task(content=task_content)

        try:
            db.session.add(task)
            db.session.commit()
            flash("Successfuly added!!!", category='success')
            return redirect('/')
        except:
            flash("There was some error while adding!", category='error')
            return redirect('/')

    else:
        tasks = Task.query.order_by(Task.created_at).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<id>')
def delete(id):
    task = Task.query.get_or_404(id)

    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except:
        flash("There was some error while deleting!", category='error')
        return redirect('/')


@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    task = Task.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['task']

        try:
            db.session.commit()
        except:
            return "There was some error while updating!"
        return redirect('/')
    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
