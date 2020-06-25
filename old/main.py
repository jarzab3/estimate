from flask import Flask, request, render_template, url_for, redirect
import datetime

app = Flask(__name__)


@app.route('/')
def my_form():
    return render_template('form.html')


@app.route('/', methods=['POST'])
def save_data():
    name = request.form['name']
    score = request.form['score']
    name_u = name.upper()
    x = datetime.datetime.now()
    print("Name: " + name_u + " Score: " + score + " Date: " + str(x))
    with open("scores.txt", "a") as fo:
        fo.write(name_u + " Score: " + score + "\n")
    return render_template('form.html')


@app.route('/get_estimate', methods=['GET'])
def get_data():
    file = None
    with open("scores.txt", "r") as fo:
        file = fo.readlines()

    text = ""
    for line in file:
        text = text + ("<p>" + line + "</p>")

    return '<div> Results: <br>' + text + "</div><a href='/reset'>New estimation</a>"


@app.route('/reset', methods=['GET'])
def reset_data():
    x = datetime.datetime.now()
    print("Cleared scores. Date: " + str(x))
    with open("scores.txt", "w") as fo:
        fo.write("")
    return redirect(url_for('get_data'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8001)
