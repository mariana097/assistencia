import os
from datetime import date

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app import create_app
from app.database.database import SessionLocal
from app.models.aparelho import Aparelho
from app.models.conta_receber import ContaReceber
from app.models.ordem_servico import OrdemServico


def test_index_menu():
    app = create_app()
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    content = response.data.decode("utf-8")
    assert "Assistência Técnica" in content
    assert "bootstrap" in content.lower()  # Verifica Bootstrap


def test_criar_e_listar_cliente():
    app = create_app()
    client = app.test_client()

    response = client.post("/clientes", json={
        "nome": "Ana",
        "cpf": "12345678901",
        "telefone": "11999999999",
        "email": "ana@example.com",
        "endereco": "Rua A, 123"
    })
    assert response.status_code == 201
    cliente = response.get_json()
    assert cliente["nome"] == "Ana"
    assert cliente["cpf"] == "12345678901"

    response = client.get("/clientes")
    assert response.status_code == 200
    content = response.data.decode("utf-8")
    # Verifica que é HTML e contém o Bootstrap
    assert "<!DOCTYPE html>" in content
    assert "bootstrap" in content.lower()
    # Verifica que contém a tabela com dados
    assert "Ana" in content or "Lista de Clientes" in content


def test_criar_e_listar_equipamentos():
    app = create_app()
    client = app.test_client()

    # Criar equipamento via POST
    response = client.post("/equipamentos", json={
        "nome": "HD SSD 240GB",
        "quantidade": 10,
        "valor_unitario": 150.00
    })
    assert response.status_code == 201
    equipamento = response.get_json()
    assert equipamento["nome"] == "HD SSD 240GB"
    assert equipamento["quantidade"] == 10

    # Listar equipamentos
    response = client.get("/equipamentos")
    assert response.status_code == 200
    content = response.data.decode("utf-8")
    # Verifica que é HTML com Bootstrap
    assert "<!DOCTYPE html>" in content
    assert "bootstrap" in content.lower()
    assert "Lista de Equipamentos" in content


def test_criar_ordem_e_calcular_valor():
    app = create_app()
    client = app.test_client()

    # Criar cliente e aparelho necessários para a ordem
    cliente_response = client.post("/clientes", json={
        "nome": "Carlos",
        "cpf": "98765432100",
    })
    assert cliente_response.status_code == 201
    cliente_id = cliente_response.get_json()["id"]

    session = SessionLocal()
    aparelho = Aparelho(tipo="Celular", marca="Samsung", modelo="Galaxy", numero_serie="XYZ123", cliente_id=cliente_id)
    session.add(aparelho)
    session.commit()
    aparelho_id = aparelho.id
    session.close()

    response = client.post("/ordens", json={
        "cliente_id": cliente_id,
        "aparelho_id": aparelho_id,
        "valor_base": 100,
        "descricao_problema": "Tela quebrada"
    })
    assert response.status_code == 201
    ordem = response.get_json()
    ordem_id = ordem["id"]
    assert ordem["valor_base"] == 100

    calculo_response = client.post(f"/ordens/{ordem_id}/calcular", json={"tipo": "urgente"})
    assert calculo_response.status_code == 200
    calculada = calculo_response.get_json()
    assert calculada["valor_total"] == 150


def test_criar_pagamento_com_cliente_e_conta():
    app = create_app()
    client = app.test_client()

    cliente_response = client.post("/clientes", json={
        "nome": "Maria Silva",
        "cpf": "11122233344",
    })
    assert cliente_response.status_code == 201
    cliente_id = cliente_response.get_json()["id"]

    session = SessionLocal()
    aparelho = Aparelho(
        tipo="Notebook",
        marca="Dell",
        modelo="Inspiron",
        numero_serie="DL123",
        cliente_id=cliente_id,
    )
    session.add(aparelho)
    session.commit()
    session.refresh(aparelho)

    ordem = OrdemServico(
        cliente_id=cliente_id,
        aparelho_id=aparelho.id,
        valor_base=150,
        descricao_problema="Problema na tela",
        valor_total=150,
    )
    session.add(ordem)
    session.commit()
    session.refresh(ordem)

    conta = ContaReceber(
        valor=150,
        vencimento=date.today(),
        status="aberta",
        ordem_servico_id=ordem.id,
    )
    session.add(conta)
    session.commit()
    session.refresh(conta)
    session.close()

    response = client.post(
        "/pagamentos",
        json={
            "cliente_id": cliente_id,
            "conta_receber_id": conta.id,
            "valor_pago": 50,
            "data_pagamento": "2026-06-19",
            "forma_pagamento": "pix",
            "numero_documento": "DOC-001",
            "observacao": "Pagamento parcial",
        },
    )

    assert response.status_code == 201
    pagamento = response.get_json()
    assert pagamento["cliente_id"] == cliente_id
    assert pagamento["conta_receber_id"] == conta.id
    assert pagamento["numero_documento"] == "DOC-001"
    assert pagamento["observacao"] == "Pagamento parcial"


def test_listar_ordens_com_bootstrap():
    """Testa se a página de ordens retorna HTML com Bootstrap"""
    app = create_app()
    client = app.test_client()

    response = client.get("/ordens")
    assert response.status_code == 200
    content = response.data.decode("utf-8")
    
    # Verifica que é HTML com Bootstrap
    assert "<!DOCTYPE html>" in content
    assert "bootstrap" in content.lower()
    assert "Ordens de Serviço" in content
    assert "Modal" in content or "modal" in content.lower()


def test_listar_tecnicos_com_bootstrap():
    """Testa se a página de técnicos retorna HTML com Bootstrap"""
    app = create_app()
    client = app.test_client()

    response = client.get("/tecnicos")
    assert response.status_code == 200
    content = response.data.decode("utf-8")
    
    # Verifica que é HTML com Bootstrap
    assert "<!DOCTYPE html>" in content
    assert "bootstrap" in content.lower()
    assert "Técnicos" in content


def test_erro_cliente_sem_cpf():
    """Testa se POST /clientes sem CPF retorna erro"""
    app = create_app()
    client = app.test_client()

    response = client.post("/clientes", json={
        "nome": "João",
        # Falta CPF
    })
    assert response.status_code == 400


def test_erro_equipamento_sem_nome():
    """Testa se POST /equipamentos sem nome retorna erro"""
    app = create_app()
    client = app.test_client()

    response = client.post("/equipamentos", json={
        "quantidade": 5,
        "valor_unitario": 100.00
        # Falta nome
    })
    assert response.status_code == 400
