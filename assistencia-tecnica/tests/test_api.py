import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app import create_app
from app.database.database import SessionLocal
from app.models.aparelho import Aparelho


def test_index_menu():
    app = create_app()
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    content = response.data.decode("utf-8")
    assert "Assistência Técnica" in content


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
    clientes = response.get_json()
    assert any(item["cpf"] == "12345678901" for item in clientes)


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
