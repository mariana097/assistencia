from flask import Flask, jsonify, request, g, abort, render_template
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

    def serialize_funcionario(funcionario):
        return {
            "id": funcionario.id,
            "nome": funcionario.nome,
            "cpf": funcionario.cpf,
            "salario": funcionario.salario,
            "tipo": getattr(funcionario, "tipo", None),
            "especialidade": getattr(funcionario, "especialidade", None),
        }

    def serialize_equipamento(e):
        return {
            "id": e.id,
            "nome": e.nome,
            "quantidade": e.quantidade,
            "valor_unitario": e.valor_unitario,
        }

    def serialize_aparelho(a):
        return {
            "id": a.id,
            "tipo": a.tipo,
            "marca": a.marca,
            "modelo": a.modelo,
            "numero_serie": a.numero_serie,
            "cliente_id": a.cliente_id,
        }

    def serialize_estoque(s):
        return {
            "id": s.id,
            "equipamento_id": s.equipamento_id,
            "quantidade_disponivel": s.quantidade_disponivel,
            "quantidade_minima": s.quantidade_minima,
        }

    def serialize_pagamento(p):
        return {
            "id": p.id,
            "valor_pago": p.valor_pago,
            "data_pagamento": p.data_pagamento.isoformat() if p.data_pagamento else None,
            "forma_pagamento": p.forma_pagamento,
            "conta_receber_id": p.conta_receber_id,
        }

    def get_cliente_controller():
        return ClienteController(ClienteService(get_db()))

    def get_ordem_controller():
        return OrdemServicoController(OrdemServicoService(get_db()))

    def get_funcionario_service():
        from app.services.funcionario_service import FuncionarioService

        return FuncionarioService(get_db())

    def get_aparelho_service():
        from app.services.aparelho_service import AparelhoService

        return AparelhoService(get_db())

    def get_estoque_service():
        from app.services.estoque_service import EstoqueService

        return EstoqueService(get_db())

    def get_pagamento_service():
        from app.services.pagamento_service import PagamentoService

        return PagamentoService(get_db())

    @app.teardown_appcontext
    def close_db(exc=None):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    @app.route("/")
    def index():
        return render_template("index.html")

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
        return render_template("clientes_list.html", clientes=clientes)

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
        return render_template("ordens_list.html", ordens=ordens)

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

    @app.route("/tecnicos", methods=["GET", "POST"])
    def tecnicos():
        if request.method == "POST":
            data = request.get_json() or {}
            nome = data.get("nome")
            cpf = data.get("cpf")
            salario = data.get("salario")
            if not nome or not cpf or salario is None:
                abort(400, description="Os campos 'nome', 'cpf' e 'salario' são obrigatórios.")

            tecnico = get_funcionario_service().cadastrar_tecnico(nome=nome, cpf=cpf, salario=salario)
            return jsonify(serialize_funcionario(tecnico)), 201

        db = get_db()
        from app.models.funcionario import Tecnico

        tecnicos = db.query(Tecnico).all()
        return render_template("tecnicos_list.html", tecnicos=tecnicos)

    @app.route("/equipamentos", methods=["GET", "POST"])
    def equipamentos():
        db = get_db()
        from app.models.equipamento import Equipamento

        if request.method == "POST":
            data = request.get_json() or {}
            nome = data.get("nome")
            quantidade = data.get("quantidade", 0)
            valor = data.get("valor_unitario", 0.0)
            if not nome:
                abort(400, description="O campo 'nome' é obrigatório.")

            equipamento = Equipamento(nome=nome, quantidade=quantidade, valor_unitario=valor)
            db.add(equipamento)
            db.commit()
            db.refresh(equipamento)
            return jsonify(serialize_equipamento(equipamento)), 201

        equipamentos = db.query(Equipamento).all()
        return render_template("equipamentos_list.html", equipamentos=equipamentos)

    @app.route("/estoque", methods=["GET", "POST"])
    def estoque():
        db = get_db()
        from app.models.estoque import Estoque

        if request.method == "POST":
            data = request.get_json() or {}
            equipamento_id = data.get("equipamento_id")
            quantidade_disponivel = data.get("quantidade_disponivel", 0)
            quantidade_minima = data.get("quantidade_minima", 0)
            if equipamento_id is None:
                abort(400, description="O campo 'equipamento_id' é obrigatório.")

            estoque_obj = get_estoque_service().atualizar_estoque(equipamento_id, quantidade_disponivel, quantidade_minima)
            return jsonify(serialize_estoque(estoque_obj)), 201

        estoques = db.query(Estoque).all()
        return render_template("estoque_list.html", estoques=estoques)

    @app.route("/pagamentos", methods=["GET", "POST"])
    def pagamentos():
        db = get_db()
        from app.models.pagamento import Pagamento

        if request.method == "POST":
            data = request.get_json() or {}
            conta_receber_id = data.get("conta_receber_id")
            valor_pago = data.get("valor_pago")
            forma = data.get("forma_pagamento")
            if conta_receber_id is None or valor_pago is None:
                abort(400, description="Os campos 'conta_receber_id' e 'valor_pago' são obrigatórios.")

            pagamento = get_pagamento_service().registrar_pagamento(conta_receber_id, valor_pago, forma)
            return jsonify(serialize_pagamento(pagamento)), 201

        pagamentos = db.query(Pagamento).all()
        return render_template("pagamentos_list.html", pagamentos=pagamentos)

    @app.route("/aparelhos", methods=["GET", "POST"])
    def aparelhos():
        service = get_aparelho_service()
        if request.method == "POST":
            data = request.get_json() or {}
            tipo = data.get("tipo")
            marca = data.get("marca")
            modelo = data.get("modelo")
            numero_serie = data.get("numero_serie")
            observacoes = data.get("observacoes")
            cliente_id = data.get("cliente_id")
            if not tipo or not marca or not modelo or cliente_id is None:
                abort(400, description="Os campos 'tipo','marca','modelo' e 'cliente_id' são obrigatórios.")

            aparelho = service.cadastrar(tipo, marca, modelo, numero_serie, observacoes, cliente_id)
            return jsonify(serialize_aparelho(aparelho)), 201

        aparelhos = service.listar()
        return render_template("aparelhos_list.html", aparelhos=aparelhos)

    @app.route("/funcionarios", methods=["GET", "POST"])
    def funcionarios():
        service = get_funcionario_service()
        if request.method == "POST":
            data = request.get_json() or {}
            nome = data.get("nome")
            cpf = data.get("cpf")
            salario = data.get("salario")
            tipo = data.get("tipo", "tecnico")
            if not nome or not cpf or salario is None:
                abort(400, description="Os campos 'nome', 'cpf' e 'salario' são obrigatórios.")

            if tipo == "tecnico":
                f = service.cadastrar_tecnico(nome, cpf, salario)
            else:
                f = service.cadastrar_administrador(nome, cpf, salario)
            return jsonify(serialize_funcionario(f)), 201

        funcionarios = service.listar()
        return jsonify([serialize_funcionario(f) for f in funcionarios])

    return app
