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
            "fornecedor": getattr(e, "fornecedor", None),
            "observacoes": getattr(e, "observacoes", None),
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
            "cliente_id": p.cliente_id,
            "valor_pago": p.valor_pago,
            "data_pagamento": p.data_pagamento.isoformat() if p.data_pagamento else None,
            "forma_pagamento": p.forma_pagamento,
            "numero_documento": p.numero_documento,
            "observacao": p.observacao,
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
        if request.args.get("json") is not None:
            return jsonify([serialize_cliente(cliente) for cliente in clientes])
        return render_template("clientes_list.html", clientes=clientes)

    @app.route("/clientes/<int:cliente_id>", methods=["GET", "PUT", "DELETE"])
    def cliente_detail(cliente_id):
        controller = get_cliente_controller()
        db = get_db()
        from app.models.cliente import Cliente

        cliente = db.query(Cliente).get(cliente_id)
        if cliente is None:
            abort(404, description="Cliente não encontrado.")

        if request.method == "GET":
            return jsonify(serialize_cliente(cliente))

        if request.method == "PUT":
            data = request.get_json() or {}
            cliente.nome = data.get("nome", cliente.nome)
            cliente.cpf = data.get("cpf", cliente.cpf)
            cliente.telefone = data.get("telefone", cliente.telefone)
            cliente.email = data.get("email", cliente.email)
            cliente.endereco = data.get("endereco", cliente.endereco)
            db.commit()
            db.refresh(cliente)
            return jsonify(serialize_cliente(cliente))

        controller.service.repository.delete(cliente)
        return jsonify({"message": "Cliente removido com sucesso."})

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
        from app.models.funcionario import Tecnico
        tecnicos = get_db().query(Tecnico).all()
        return render_template(
            "ordens_list.html",
            ordens=ordens,
            tecnicos=tecnicos
)

    @app.route("/ordens/<int:ordem_id>", methods=["GET", "PUT", "DELETE"])
    def ordem_detail(ordem_id):
        db = get_db()
        from app.models.ordem_servico import OrdemServico

        ordem = db.query(OrdemServico).get(ordem_id)
        if ordem is None:
            abort(404, description="Ordem de serviço não encontrada.")

        if request.method == "GET":
            return jsonify(serialize_ordem(ordem))

        if request.method == "PUT":
            data = request.get_json() or {}
            ordem.cliente_id = data.get("cliente_id", ordem.cliente_id)
            ordem.aparelho_id = data.get("aparelho_id", ordem.aparelho_id)
            ordem.tecnico_id = data.get("tecnico_id", ordem.tecnico_id)
            ordem.descricao_problema = data.get("descricao_problema", ordem.descricao_problema)
            ordem.status = data.get("status", ordem.status)
            ordem.valor_base = data.get("valor_base", ordem.valor_base)
            ordem.valor_total = data.get("valor_total", ordem.valor_total)
            db.commit()
            db.refresh(ordem)
            return jsonify(serialize_ordem(ordem))

        db.delete(ordem)
        db.commit()
        return jsonify({"message": "Ordem removida com sucesso."})

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
        if request.args.get("json") is not None:
            return jsonify([serialize_funcionario(t) for t in tecnicos])
        return render_template("tecnicos_list.html", tecnicos=tecnicos)

    @app.route("/tecnicos/<int:tecnico_id>", methods=["GET", "PUT", "DELETE"])
    def tecnico_detail(tecnico_id):
        db = get_db()
        from app.models.funcionario import Tecnico

        tecnico = db.query(Tecnico).get(tecnico_id)
        if tecnico is None:
            abort(404, description="Técnico não encontrado.")

        if request.method == "GET":
            return jsonify(serialize_funcionario(tecnico))

        if request.method == "PUT":
            data = request.get_json() or {}
            tecnico.nome = data.get("nome", tecnico.nome)
            tecnico.cpf = data.get("cpf", tecnico.cpf)
            tecnico.salario = data.get("salario", tecnico.salario)
            tecnico.especialidade = data.get("especialidade", tecnico.especialidade)
            db.commit()
            db.refresh(tecnico)
            return jsonify(serialize_funcionario(tecnico))

        db.delete(tecnico)
        db.commit()
        return jsonify({"message": "Técnico removido com sucesso."})

    @app.route("/equipamentos", methods=["GET", "POST"])
    def equipamentos():
        db = get_db()
        from app.models.equipamento import Equipamento

        if request.method == "POST":
            data = request.get_json() or {}
            nome = data.get("nome")
            quantidade = data.get("quantidade", 0)
            valor = data.get("valor_unitario", 0.0)
            fornecedor = data.get("fornecedor")
            observacoes = data.get("observacoes")
            if not nome:
                abort(400, description="O campo 'nome' é obrigatório.")

            equipamento = Equipamento(
                nome=nome,
                quantidade=quantidade,
                valor_unitario=valor,
                fornecedor=fornecedor,
                observacoes=observacoes,
            )
            db.add(equipamento)
            db.commit()
            db.refresh(equipamento)
            return jsonify(serialize_equipamento(equipamento)), 201

        equipamentos = db.query(Equipamento).all()
        if request.args.get("json") is not None:
            return jsonify([serialize_equipamento(e) for e in equipamentos])
        return render_template("equipamentos_list.html", equipamentos=equipamentos)

    @app.route("/equipamentos/<int:equipamento_id>", methods=["GET", "PUT", "DELETE"])
    def equipamento_detail(equipamento_id):
        db = get_db()
        from app.models.equipamento import Equipamento

        equipamento = db.query(Equipamento).get(equipamento_id)
        if equipamento is None:
            abort(404, description="Equipamento não encontrado.")

        if request.method == "GET":
            return jsonify(serialize_equipamento(equipamento))

        if request.method == "PUT":
            data = request.get_json() or {}
            equipamento.nome = data.get("nome", equipamento.nome)
            equipamento.quantidade = data.get("quantidade", equipamento.quantidade)
            equipamento.valor_unitario = data.get("valor_unitario", equipamento.valor_unitario)
            equipamento.fornecedor = data.get("fornecedor", equipamento.fornecedor)
            equipamento.observacoes = data.get("observacoes", equipamento.observacoes)
            db.commit()
            db.refresh(equipamento)
            return jsonify(serialize_equipamento(equipamento))

        db.delete(equipamento)
        db.commit()
        return jsonify({"message": "Equipamento removido com sucesso."})

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

    @app.route("/estoque/<int:estoque_id>", methods=["GET", "PUT", "DELETE"])
    def estoque_detail(estoque_id):
        db = get_db()
        from app.models.estoque import Estoque

        estoque = db.query(Estoque).get(estoque_id)
        if estoque is None:
            abort(404, description="Item de estoque não encontrado.")

        if request.method == "GET":
            return jsonify(serialize_estoque(estoque))

        if request.method == "PUT":
            data = request.get_json() or {}
            estoque.equipamento_id = data.get("equipamento_id", estoque.equipamento_id)
            estoque.quantidade_disponivel = data.get("quantidade_disponivel", estoque.quantidade_disponivel)
            estoque.quantidade_minima = data.get("quantidade_minima", estoque.quantidade_minima)
            db.commit()
            db.refresh(estoque)
            return jsonify(serialize_estoque(estoque))

        db.delete(estoque)
        db.commit()
        return jsonify({"message": "Item removido com sucesso."})

    @app.route("/pagamentos", methods=["GET", "POST"])
    def pagamentos():
        db = get_db()
        from app.models.pagamento import Pagamento

        if request.method == "POST":
            data = request.get_json() or {}
            cliente_id = data.get("cliente_id")
            conta_receber_id = data.get("conta_receber_id")
            valor_pago = data.get("valor_pago")
            forma = data.get("forma_pagamento")
            data_pagamento = data.get("data_pagamento")
            numero_documento = data.get("numero_documento")
            observacao = data.get("observacao")

            if cliente_id is None or conta_receber_id is None or valor_pago is None:
                abort(400, description="Os campos 'cliente_id', 'conta_receber_id' e 'valor_pago' são obrigatórios.")

            pagamento = get_pagamento_service().registrar_pagamento(
                cliente_id=cliente_id,
                conta_receber_id=conta_receber_id,
                valor_pago=valor_pago,
                forma_pagamento=forma,
                data_pagamento=data_pagamento,
                numero_documento=numero_documento,
                observacao=observacao,
            )
            return jsonify(serialize_pagamento(pagamento)), 201

        pagamentos = db.query(Pagamento).all()
        return render_template("pagamentos_list.html", pagamentos=pagamentos)

    @app.route("/contas-receber")
    def contas_receber():
        from app.models.conta_receber import ContaReceber
        from app.models.ordem_servico import OrdemServico

        db = get_db()
        cliente_id = request.args.get("cliente_id")

        query = db.query(ContaReceber).join(OrdemServico, ContaReceber.ordem_servico_id == OrdemServico.id)
        if cliente_id:
            query = query.filter(OrdemServico.cliente_id == int(cliente_id))

        contas = query.all()
        return jsonify([
            {
                "id": conta.id,
                "valor": conta.valor,
                "vencimento": conta.vencimento.isoformat() if conta.vencimento else None,
                "status": conta.status,
                "ordem_servico_id": conta.ordem_servico_id,
                "cliente_id": conta.ordem_servico.cliente_id if conta.ordem_servico else None,
            }
            for conta in contas
        ])

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
