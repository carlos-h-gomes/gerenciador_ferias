from flask import Flask, render_template
from blueprints.times import times_bp
from blueprints.squads import squads_bp
from blueprints.pessoas import pessoas_bp
from blueprints.datas import datas_bp
from blueprints.regras import regras_bp
from blueprints.operacao import operacao_bp
from blueprints.analitica import analitica_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = 'H1_cu$t0m3rC4r3'  # Substitua por uma chave segura

    # ✅ Registro dos Blueprints
    app.register_blueprint(times_bp)
    app.register_blueprint(squads_bp)
    app.register_blueprint(pessoas_bp)
    app.register_blueprint(datas_bp)
    app.register_blueprint(regras_bp)
    app.register_blueprint(operacao_bp)
    app.register_blueprint(analitica_bp)

    # ✅ Rota do Hub Central
    @app.route("/")
    def hub():
        return render_template("hub.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=3000)
