from flask import Flask, render_template, redirect, request, session
import database_manager as dbHandler
import os

app = Flask(__name__)
app.secret_key = str(os.environ.get("FLASK_SECRET_KEY"))


def logged_in():
    if "user_id" in session:
        return True
    else:
        return False


@app.route("/home.html", methods=["GET"])
@app.route("/", methods=["POST", "GET"])
def home():
    return render_template("/home.html", logged_in=logged_in())


@app.route("/vtuber/<int:id>")
def vtuber_page(id):
    vtuber = dbHandler.get_vtuber(id)
    is_favourited = False

    if "user_id" in session:
        is_favourited = dbHandler.is_favourite(session["user_id"], id)

    return render_template(
        "vtuber.html", vtuber=vtuber, logged_in=logged_in(), is_favourited=is_favourited
    )


@app.route("/about.html", methods=["GET"])
def about():
    return render_template("/about.html", logged_in=logged_in())


@app.route("/index.html", methods=["GET"])
# @app.route("/", methods=["POST", "GET"])
def index():
    branch = request.args.get("branch")
    generation = request.args.get("generation")
    graduated = request.args.get("graduated")

    if branch:
        data = dbHandler.listVtuberbybranch(branch)
    elif generation:
        data = dbHandler.listVtuberbygeneration(generation)
    elif graduated:
        data = dbHandler.listVtuberbygraduated(graduated)
    else:
        data = dbHandler.listVtubers()

    # Sort graduated Vtubers after active Vtubers
    data.sort(key=lambda row: (row[11]))
    return render_template("/index.html", content=data, logged_in=logged_in())


@app.route("/signup.html", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        dbHandler.insertUser(email, password)
        return render_template(
            "/login.html",
            message="Signup Successful, Now please Login using those same credentials",
        )
    else:
        return render_template("/signup.html", logged_in=logged_in())


@app.route("/login.html", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = dbHandler.get_user(email)

        if dbHandler.checkUser(email, password):
            session["user_id"] = user[0]
            return render_template("/home.html", logged_in=logged_in())
        else:
            return render_template(
                "/login.html", message="Invalid Login", logged_in=logged_in()
            )
    else:
        return render_template("/login.html", logged_in=logged_in())


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/favourites.html")
def favourites():
    if "user_id" not in session:
        return redirect("/login.html")
    else:
        content = dbHandler.get_favourites(session["user_id"])

        branch = request.args.get("branch")
        generation = request.args.get("generation")
        graduated = request.args.get("graduated")

        if branch:
            content = [vtuber for vtuber in content if vtuber[3] == branch]
        elif generation:
            content = [vtuber for vtuber in content if vtuber[2] == generation]
        elif graduated:
            content = [vtuber for vtuber in content if vtuber[11] == int(graduated)]

        # Sort graduated Vtubers after active Vtubers
        content.sort(key=lambda row: (row[11]))

        return render_template(
            "favourites.html", logged_in=logged_in(), content=content
        )


@app.route("/favourite/<int:vtuber_id>")
def favourite(vtuber_id):
    if "user_id" not in session:
        return redirect("/login.html")

    dbHandler.add_favourite(session["user_id"], vtuber_id)

    return redirect(request.referrer)


@app.route("/unfavourite/<int:vtuber_id>")
def unfavourite(vtuber_id):
    if "user_id" not in session:
        return redirect("/login.html")

    dbHandler.remove_favourite(session["user_id"], vtuber_id)

    return redirect(request.referrer)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
