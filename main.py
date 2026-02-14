from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/health")
def main():
    return jsonify({
        "message": "ok"
    })

if __name__ == "__main__":
    app.run(debug=True)
