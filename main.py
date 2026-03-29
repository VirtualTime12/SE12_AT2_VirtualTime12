from flask import Flask, render_template, request
import database_manager as dbHandler

app = Flask(__name__)


@app.route("/home.html", methods=["GET"])
@app.route("/", methods=["POST", "GET"])
def home():
    return render_template("/home.html")


@app.route("/vtuber/<int:id>")
def vtuber_page(id):

    vtuber = dbHandler.get_vtuber(id)
    return render_template("vtuber.html", vtuber=vtuber)


@app.route("/about.html", methods=["GET"])
def about():
    return render_template("/about.html")


@app.route("/index.html", methods=["GET"])
# @app.route("/", methods=["POST", "GET"])
def index():
    branch = request.args.get("branch")
    generation = request.args.get("generation")

    if branch:
        data = dbHandler.listVtuberbybranch(branch)
    elif generation:
        data = dbHandler.listVtuberbygeneration(generation)
    else:
        data = dbHandler.listVtubers()
    return render_template("/index.html", content=data)


@app.route("/add.html", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        email = request.form["email"]
        name = request.form["name"]
        dbHandler.insertContact(email, name)
        return render_template("/add.html", is_done=True)
    else:
        return render_template("/add.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
