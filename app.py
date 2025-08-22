from flask import Flask, render_template, request , redirect , url_for , session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///statement.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "yoursecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"


    
db = SQLAlchemy(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Statement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    catagory = db.Column(db.String(50), nullable=False)
    
with app.app_context():
    db.create_all()

@app.template_filter('currencyFormat')
def currencyFormat(value):
    try:
        value = float(value)
        return f"{value:,.2f}"
    except (TypeError, ValueError):
        return "0.00"


@app.route("/")
def fhome():
    if "user_id" in session:
        return f"ยินดีต้อนรับ {session['user_email']}!"
    return render_template("login.html")

@app.route("/home")
def home():
    if "user_id" in session:
        # แสดงหน้า home.html แทนข้อความ
        return render_template("index.html")
    return redirect(url_for("login"))



@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/profile")
def profile():
    if "user_id" in session:
        user = User.query.get(session["user_id"])
        return render_template("profile.html", user=user)
    return redirect(url_for("login"))

@app.route("/users")
def users():
    all_users = User.query.all()
    return render_template("users.html", users=all_users)


@app.route("/addStatement", methods=["POST"])
def addStatement():
    date = request.form["date"]
    name = request.form["name"]
    amount = request.form["amount"]
    catagory = request.form["catagory"]

    statement = Statement(date=date, name=name, amount=amount, catagory=catagory)
    db.session.add(statement)
    db.session.commit()

    # redirect ไปยังฟังก์ชัน index
    return redirect("index")

@app.route("/showData")
def showData():
    statements = Statement.query.all()
    return render_template("statements.html", statements=statements)


@app.route("/delete/<int:id>")
def deleteStatement(id):
    state = Statement.query.filter_by(id = id).first()
    db.session.delete(state)
    db.session.commit()
    return redirect("/showData")

@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["user_email"] = user.email
            return redirect(url_for("home"))
        else:
            message = "Email หรือ Password ไม่ถูกต้อง"

    return render_template("login.html", message=message)


@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            message = "Email นี้ถูกใช้งานแล้ว!"
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            message = "สมัครสมาชิกสำเร็จ!"

    return render_template("register.html", message=message)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/edit/<int:id>")
def editStatement(id):
    state = Statement.query.filter_by(id = id).first()
    return render_template("edit.html",state=state)


@app.route("/updateStatement" , methods=["POST"])
def updateStatement() :
    id = request.form["id"]
    date = request.form["date"]
    name = request.form["name"]
    amount = request.form["amount"]
    catagory = request.form["catagory"]
    state = Statement.query.filter_by(id = id).first()
    state.date = date
    state.name = name
    state.amount = amount
    state.catagory = catagory
    db.session.commit()
    return redirect("/showData")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
