from flask import Flask, jsonify, request, g, abort
from app.database.database import init_db, SessionLocal
from app.controllers.cliente_controller import ClienteController
from app.controllers.ordem_servico_controller import OrdemServicoController
from app.services.cliente_service import ClienteService
from app.services.ordem_servico_service import OrdemServicoService
from app.factories.estrategia_factory import EstrategiaFactory


def create_app():
    app = Flask(__name__)
    init_db()

    def get_db():
        if "db" not in g:
            g.db = SessionLocal()
        return g.db

    def serialize_cliente(cliente):
        return {
            "id": cliente.id,
            "nome": cliente.nome,
            "cpf": cliente.cpf,
            "telefone": cliente.telefone,
            "email": cliente.email,
            "endereco": getattr(cliente, "endereco", None),
        }

    def serialize_ordem(ordem):
        return {
            "id": ordem.id,
            "data_abertura": ordem.data_abertura.isoformat() if ordem.data_abertura else None,
            "data_encerramento": ordem.data_encerramento.isoformat() if ordem.data_encerramento else None,
            "descricao_problema": ordem.descricao_problema,
            "status": ordem.status,
            "valor_base": ordem.valor_base,
            "valor_total": ordem.valor_total,
            "cliente_id": ordem.cliente_id,
            "aparelho_id": ordem.aparelho_id,
            "tecnico_id": ordem.tecnico_id,
        }

    def get_cliente_controller():
        return ClienteController(ClienteService(get_db()))

    def get_ordem_controller():
        return OrdemServicoController(OrdemServicoService(get_db()))

    @app.teardown_appcontext
    def close_db(exc=None):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    @app.route("/")
    def index():
        return (
            "<h1>Assistência Técnica</h1>"
            "<p>Use os endpoints abaixo para interagir com o sistema:</p>"
            "<ul>"
            "<li><a href=\"/clientes\">/clientes</a> - listar clientes</li>"
            "<li><a href=\"/ordens\">/ordens</a> - listar ordens de serviço</li>"
            "</ul>"
            "<p>Crie ordens via POST em /ordens e calcule valores em /ordens/&lt;id&gt;/calcular</p>"
        )

    @app.route("/clientes", methods=["GET", "POST"])
    def clientes():
        controller = get_cliente_controller()

        if request.method == "POST":
            data = request.get_json() or {}
            nome = data.get("nome")
            cpf = data.get("cpf")
            if not nome or not cpf:
                abort(400, description="Os campos 'nome' e 'cpf' são obrigatórios.")

            cliente = controller.cadastrar_cliente(
                nome=nome,
                cpf=cpf,
                telefone=data.get("telefone"),
                email=data.get("email"),
                endereco=data.get("endereco"),
            )
            return jsonify(serialize_cliente(cliente)), 201

        clientes = controller.listar_clientes()
        return jsonify([serialize_cliente(cliente) for cliente in clientes])

    @app.route("/ordens", methods=["GET", "POST"])
    def ordens():
        controller = get_ordem_controller()

        if request.method == "POST":
            data = request.get_json() or {}
            required = ["cliente_id", "aparelho_id", "valor_base", "descricao_problema"]
            if not all(field in data for field in required):
                abort(400, description="Os campos cliente_id, aparelho_id, valor_base e descricao_problema são obrigatórios.")

            ordem = controller.criar_ordem(
                cliente_id=data.get("cliente_id"),
                aparelho_id=data.get("aparelho_id"),
                valor_base=data.get("valor_base"),
                descricao_problema=data.get("descricao_problema"),
                tecnico_id=data.get("tecnico_id"),
            )
            return jsonify(serialize_ordem(ordem)), 201

        ordens = controller.listar_ordens()
        return jsonify([serialize_ordem(ordem) for ordem in ordens])

    @app.route("/ordens/<int:ordem_id>/calcular", methods=["POST"])
    def calcular_ordem(ordem_id):
        data = request.get_json() or {}
        tipo = data.get("tipo") or "padrao"
        ordem = get_ordem_controller().obter_ordem(ordem_id)
        if ordem is None:
            abort(404, description="Ordem de serviço não encontrada.")

        estrategia = EstrategiaFactory.criar(tipo)
        ordem = get_ordem_controller().calcular_valor_ordem(ordem, estrategia)
        return jsonify(serialize_ordem(ordem))

    return app
