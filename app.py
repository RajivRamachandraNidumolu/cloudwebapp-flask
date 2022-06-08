from flask import Flask, render_template, request
import os
import json


app = Flask(__name__, template_folder="template")
print(os.getenv("PORT"))
port = int(os.getenv("PORT", 5000))

f = open('people.json', "r+")
data = json.load(f)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    val = str(request.form['ptext'])
    pic = ""
    for i in data:
        if i == val:
            pic += data[i]['Picture']
            print(pic)
    return render_template('/profile.html', r=pic)


@app.route('/salpicture', methods=['GET', 'POST'])
def pictures():
    val1 = int(request.form['salary'])
    a = val1
    arra2 = []
    for i in data:
        if data[i]['Salary'] != "" and data[i]['Salary'] < val1:
            array = []
            array.append(data[i]['Picture'])
            arra2.append(array)
    return render_template('/salpicture.html', r=arra2)


@app.route('/addimage', methods=['POST', 'GET'])
def addimage():
    val1 = str(request.form['person'])
    val2 = str(request.form['addim'])
    arra2 = []
    for i in data:
        if i == val1:
            data[i]['Picture'] = val2

    return render_template('/addimage.html', r=val2, s=val1)


@app.route('/updatekey', methods=['POST', 'GET'])
def changekey():
    name = str(request.form['name'])
    words = str(request.form['words'])
    for i in data:
        if i == name:
            data[i]['Keywords'] = words
    return render_template('/keywordupdate.html', r=name, y=words)


@app.route('/updatesalary', methods=['POST', 'GET'])
def changesalary():
    name = str(request.form['name'])
    salary = int(request.form['salary'])
    for i in data:
        if i == name:
            data[i]['Salary'] = salary
    return render_template('/updatesalary.html', r=name, y=salary)


if __name__ == '__main__':
    app.debug = True
    app.run()
