from app.models.estoque import Estoque


def test_estoque_precisa_repor_quando_abaixo_do_minimo():
    estoque = Estoque(quantidade_disponivel=2, quantidade_minima=5, equipamento_id=1)
    assert estoque.precisa_repor()


def test_estoque_nao_precisa_repor_quando_acima_do_minimo():
    estoque = Estoque(quantidade_disponivel=10, quantidade_minima=5, equipamento_id=1)
    assert not estoque.precisa_repor()
