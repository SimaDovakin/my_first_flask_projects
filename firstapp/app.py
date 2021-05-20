from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test.sqlite3'
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
            return redirect('/')
        except:
            return "There was some error!"

    else:
        tasks = Task.query.order_by(Task.created_at).all()
        return render_template('index.html', tasks=tasks)

@app.route("/users/<name>")
def user(name):
    return f"Hello {name}"


if __name__ == "__main__":
    app.run(debug=True)
