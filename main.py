from flask import Flask, jsonify
from flask_cors import CORS
from routes.well_routes import create_well_routes

def create_app() -> Flask:
    app = Flask(__name__)

    CORS(app)

    app.register_blueprint(create_well_routes(), url_prefix='/api')

    @app.route("/health")
    def health_check():
        return jsonify({
            "status": "ok",
            "message": "Seismic Viewer Backend is running"
        })

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
