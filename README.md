# Projeto – Sistema de Gestão de Assistência Técnica

## Disciplina

Programação Orientada a Objetos II

## Tema

Sistema de Gestão de Assistência Técnica

---

# 1. API

URL pública: https://psychic-succotash-jwpp47xrgj525xx7-5000.app.github.dev
Acesse a raiz para testar: https://psychic-succotash-jwpp47xrgj525xx7-5000.app.github.dev/
Comando usado localmente: python3 assistencia-tecnica/run.py

---

# 2. Objetivo

Desenvolver um sistema para gerenciar clientes, aparelhos, técnicos, estoque, pagamentos e ordens de serviço de uma assistência técnica, aplicando conceitos de Programação Orientada a Objetos, princípios SOLID e os padrões de projeto **Strategy** e **Factory Method**.

---

# 3. Objetivos Específicos

* Cadastrar clientes.
* Cadastrar aparelhos.
* Cadastrar funcionários.
* Gerenciar ordens de serviço.
* Registrar visitas técnicas.
* Controlar estoque de peças e equipamentos.
* Gerenciar pagamentos.
* Calcular automaticamente o valor das ordens de serviço.
* Aplicar padrões de projeto para aumentar a flexibilidade e a manutenção do sistema.

---

# 4. Tecnologias

* Python 3.12
* Flask
* SQLAlchemy
* PostgreSQL
* Pytest
* Pylint
* SonarQube
* Git
* GitHub

---

# 5. Conceitos de POO Aplicados

## Encapsulamento

Os atributos das classes serão protegidos e acessados através de métodos específicos.

## Herança

A classe Funcionario será a superclasse de:

* Tecnico
* Administrador

## Polimorfismo

As diferentes estratégias de cálculo utilizarão a mesma interface.

## Abstração

As entidades representam objetos do mundo real da assistência técnica.

---

# 6. Entidades do Sistema

## Cliente

* id
* nome
* cpf
* telefone
* email

## Aparelho

* id
* tipo
* marca
* modelo
* numero_serie
* observacoes

## Funcionario

* id
* nome
* cpf
* salario

## Tecnico

Herda de Funcionario.

## Administrador

Herda de Funcionario.

## OrdemServico

* id
* data_abertura
* data_encerramento
* descricao_problema
* status
* valor_total

## VisitaTecnica

* id
* data_agendamento
* data_realizacao
* resultado
* status

## Equipamento

* id
* nome
* quantidade
* valor_unitario

## Estoque

* id
* quantidade_disponivel
* quantidade_minima

## ContaReceber

* id
* valor
* vencimento
* status

## Pagamento

* id
* valor_pago
* data_pagamento
* forma_pagamento

---

# 7. Padrão Strategy

## Objetivo

Permitir diferentes formas de cálculo do valor final da Ordem de Serviço.

---

## Interface

```python
from abc import ABC, abstractmethod

class EstrategiaCalculo(ABC):

    @abstractmethod
    def calcular(self, valor_base):
        pass
```

---

## Estratégia Padrão

```python
class CalculoPadrao(EstrategiaCalculo):

    def calcular(self, valor_base):
        return valor_base
```

---

## Estratégia Urgente

```python
class CalculoUrgente(EstrategiaCalculo):

    def calcular(self, valor_base):
        return valor_base * 1.5
```

---

## Estratégia por Hora

```python
class CalculoPorHora(EstrategiaCalculo):

    def calcular(self, valor_base):
        return valor_base * 1.2
```

---

## Estratégia Domiciliar

```python
class CalculoDomiciliar(EstrategiaCalculo):

    def calcular(self, valor_base):
        return valor_base + 50
```

---

# 8. Padrão Factory Method

## Objetivo

Centralizar a criação das estratégias de cálculo.

---

## Classe Factory

```python
class EstrategiaFactory:

    @staticmethod
    def criar(tipo):

        if tipo == "urgente":
            return CalculoUrgente()

        if tipo == "hora":
            return CalculoPorHora()

        if tipo == "domiciliar":
            return CalculoDomiciliar()

        return CalculoPadrao()
```

---

# 9. Utilização dos Padrões

```python
tipo = "urgente"

estrategia = EstrategiaFactory.criar(tipo)

valor = estrategia.calcular(100)

print(valor)
```

Resultado:

```text
150.0
```

---

# 10. Benefícios Obtidos

## Strategy

* Permite trocar algoritmos de cálculo.
* Evita estruturas complexas de decisão.
* Facilita manutenção.

## Factory Method

* Centraliza a criação de objetos.
* Reduz acoplamento.
* Facilita inclusão de novas estratégias.

---

# 11. Princípios SOLID Aplicados

## SRP

Cada classe possui apenas uma responsabilidade.

## OCP

Novas estratégias podem ser criadas sem alterar as existentes.

## LSP

Todas as estratégias podem substituir a interface base.

## ISP

Interfaces pequenas e específicas.

## DIP

A Ordem de Serviço depende da abstração EstrategiaCalculo.

---

# 12. Testes Unitários

Utilização do Pytest para validar:

* Cadastro de clientes.
* Cadastro de aparelhos.
* Criação de ordens de serviço.
* Estratégias de cálculo.
* Factory Method.
* Controle de estoque.
* Pagamentos.

---

# 13. Estrutura de Pastas do Projeto

```text
assistencia-tecnica/
│
├── app/
│   │
│   ├── __init__.py
│   │
│   ├── models/
│   │   ├── cliente.py
│   │   ├── aparelho.py
│   │   ├── funcionario.py
│   │   ├── ordem_servico.py
│   │   ├── visita_tecnica.py
│   │   ├── equipamento.py
│   │   ├── estoque.py
│   │   ├── conta_receber.py
│   │   └── pagamento.py
│   │
│   ├── repositories/
│   │   ├── cliente_repository.py
│   │   ├── aparelho_repository.py
│   │   ├── funcionario_repository.py
│   │   ├── ordem_servico_repository.py
│   │   ├── visita_tecnica_repository.py
│   │   ├── equipamento_repository.py
│   │   ├── estoque_repository.py
│   │   ├── conta_receber_repository.py
│   │   └── pagamento_repository.py
│   │
│   ├── services/
│   │   ├── cliente_service.py
│   │   ├── aparelho_service.py
│   │   ├── funcionario_service.py
│   │   ├── ordem_servico_service.py
│   │   ├── visita_tecnica_service.py
│   │   ├── equipamento_service.py
│   │   ├── estoque_service.py
│   │   ├── conta_receber_service.py
│   │   └── pagamento_service.py
│   │
│   ├── controllers/
│   │   ├── cliente_controller.py
│   │   ├── aparelho_controller.py
│   │   ├── funcionario_controller.py
│   │   ├── ordem_servico_controller.py
│   │   ├── visita_tecnica_controller.py
│   │   ├── equipamento_controller.py
│   │   ├── estoque_controller.py
│   │   ├── conta_receber_controller.py
│   │   └── pagamento_controller.py
│   │
│   ├── strategies/
│   │   ├── estrategia_calculo.py
│   │   ├── calculo_padrao.py
│   │   ├── calculo_urgente.py
│   │   ├── calculo_por_hora.py
│   │   └── calculo_domiciliar.py
│   │
│   ├── factories/
│   │   └── estrategia_factory.py
│   │
│   ├── database/
│   │   └── database.py
│   │
│   └── config/
│       └── settings.py
│
├── tests/
│   ├── test_cliente.py
│   ├── test_aparelho.py
│   ├── test_funcionario.py
│   ├── test_ordem_servico.py
│   ├── test_visita_tecnica.py
│   ├── test_equipamento.py
│   ├── test_estoque.py
│   ├── test_conta_receber.py
│   ├── test_pagamento.py
│   ├── test_strategy.py
│   └── test_factory.py
│
├── docs/
│   ├── requisitos.md
│   ├── casos_de_uso.md
│   └── modelo.md
│
├── migrations/
│
├── requirements.txt
├── pytest.ini
├── .gitignore
├── README.md
└── run.py
```

# 14. Conclusão

O projeto utiliza conceitos fundamentais de Programação Orientada a Objetos, aplicando herança, polimorfismo, encapsulamento e abstração. Além disso, emprega os padrões de projeto Strategy e Factory Method para tornar o sistema flexível, extensível e aderente aos princípios SOLID, resultando em uma solução organizada e de fácil manutenção.
