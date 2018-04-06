from flask import Flask, request
from flask import render_template
from flask import send_file
import json
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
    
@app.route('/download/', methods=['GET','POST'])
def download():
    abc = request.form['url']
    print (abc)
    try:
        return send_file('/app/demo.pbn', as_attachment=True,
                            attachment_filename='output.pbn')
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
