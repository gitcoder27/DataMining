from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from scripts import kmeans as k

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def hello_world():
    return render_template('form.html')

@app.route('/upload', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['myFile']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('navigate.html')


@app.route('/kmeans')
def route_kmeans():
    return render_template('kmean.html')

@app.route('/kmeansalgo', methods=['GET','POST'])
def kmean_algo():
    if request.method == 'POST':
        output,ran = k.main()
        return render_template('output.html', output_result=output, ran=ran)


if __name__ == '__main__':
    app.run(port=8000, debug=True)
