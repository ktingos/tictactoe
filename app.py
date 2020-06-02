from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():

    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["turn"] = "X"
        session["moves"] = []

    return render_template("game.html", game=session["board"], turn=session["turn"])

@app.route("/play/<int:row>/<int:col>")
def play(row, col):

    session["board"][row][col] = session["turn"]
    session["moves"].append((row, col, session["turn"]))

    if session["turn"] is "X":
        session["turn"] = "O"
    else:
        session["turn"] = "X"

    return redirect(url_for("checkoutcome"))

@app.route("/restart")
def restart():

    session.clear()

    return redirect(url_for("index"))

@app.route("/checkoutcome")
def checkoutcome():

    if not session["moves"]:
        return redirect(url_for("restart"))

    for i in range(3):
        if (session["board"][i][0] is session["board"][i][1] is session["board"][i][2] and session["board"][i][0]) \
        or (session["board"][0][i] is session["board"][1][i] is session["board"][2][i] and session["board"][0][i]):
            return render_template("outcome.html", outcome=session["moves"][-1][2])

    if (session["board"][0][0] is session["board"][1][1] is session["board"][2][2] and session["board"][0][0]) \
    or (session["board"][0][2] is session["board"][1][1] is session["board"][2][0] and session["board"][2][0]):
        return render_template("outcome.html", outcome=session["moves"][-1][2])

    for i in range(3):
        for j in range(3):
            if session["board"][i][j] == None:
                return redirect(url_for("index"))

    return render_template("outcome.html", outcome="No One")

@app.route("/undomove")
def undomove():

    if not session["moves"]:
        return redirect(url_for("restart"))

    move = session["moves"].pop(-1)
    session["board"][move[0]][move[1]] = None
    session["turn"] = move[2]

    return redirect(url_for("index"))

@app.route("/movehistory")
def movehistory():

    history = []

    if not session:
        return redirect(url_for("restart"))

    if not session["moves"]:
        return redirect(url_for("restart"))

    for move in session["moves"]:
        line = f"{move[2]} went "

        if move[0] == 0:
            line += " top"
        elif move[0] == 1:
            line += " middle"
        else:
            line += " bottom"

        if move[1] == 0:
            line += " left"
        elif move[1] == 1:
            line += " middle"
        else:
            line += " right"

        history.append(line)

    return render_template("movehistory.html", history = history)
