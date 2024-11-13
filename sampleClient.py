from flask import Flask,jsonify

app = Flask(__name__)
port=5600

@app.route('/asd')
def index():
    return f'Flask is running {port}!'

@app.route('/secret-heart-beat')
def hell():
    return jsonify(heart='beating')

@app.route('/api')
def hello():
    return jsonify(hello='world')

if __name__ == '__main__':
    app.run(debug=False,port=port)

