# Modelo de Dados

## 📊 Diagrama de Classes usando Mermaid

```mermaid
classDiagram

class Cliente {
    +Long id
    +String nome
    +String cpf
    +String telefone
    +String email
}

class Equipamento {
    +Long id
    +String nome
    +String marca
    +String modelo
}

class OrdemServico {
    +Long id
    +LocalDate dataAbertura
    +String defeito
    +StatusOS status
    +Double valor
}

class Funcionario {
    +Long id
    +String nome
    +String login
    +String senha
}

class Tecnico

class Administrador 

class OrdemServico {
    +Long id 
    +LocalDate 
    dataAbertura 
    +LocalDate 
    dataEncerramento 
    +String 
    descricaoProblema 
    +String status 
    +Double valorTotal 
} 

class VisitaTecnica { 
    +Long id 
    +LocalDate 
    dataAgendamento 
    +LocalDate 
    dataRealizacao 
    +String resultado 
    +String status 
} 

class Equipamento { 
    +Long id 
    +String nome 
    +Integer quantidade 
    +Double valorUnitario 
} 

class ContaReceber { 
    +Long id 
    +Double valor 
    +LocalDate vencimento 
    +String status 
} 

class Pagamento { 
    +Long id 
    +Double 
    valorPago 
    +LocalDate 
    dataPagamento 
    +String 
    formaPagamento 
}


Funcionario <|-- Tecnico
Funcionario <|-- Administrador 

Funcionario <|-- Tecnico 
Funcionario <|-- Administrador 
Cliente "1" --> "*" Aparelho : possui 
Aparelho "1" --> "*" OrdemServico : gera 
Tecnico "1" --> "*" OrdemServico : executa 
OrdemServico "1" --> "*" VisitaTecnica : possui 
OrdemServico "1" --> "1" ContaReceber : gera 
ContaReceber "1" --> "0..1" Pagamento : recebe 
OrdemServico "*" --> "*" Equipamento : utiliza
```
---

### Descrição das Entidades

Entidade       |	Descrição   |
-------------- |  ------------ |
Cliente	       | Entidade que representa um cliente do sistema. Contém informações cadastrais: nome, endereco, contato.|
Funcionário	   | Especialização de funcionário para técnico. Contém dados como nome, cpf, contato, salario, data_admissao, horario_expediente e status.|
Técnico        | Especialização de FUNCIONARIO para técnicos especializados.|
Administrador  | Especialização de FUNCIONARIO para administradores do sistema.|
Aparelho       | Entidade que representa os aparelhos dos clientes que serão reparados. Contém informações técnicas: tipo, marca, modelo, numero_serie, cor, observacoes e cliente_id e status.|
Ordem_Serviço  | Entidade central que representa uma ordem de serviço aberta para reparo. Contém id, data_abertura, data_encerramento, descricao_problema, status, valor_total, cliente_id, tecnico_id e aparelho_id.|
Equipamento	   | Entidade que representa insumos, ferramentas ou peças do estoque da assistência.|
Visita_Técnica | Entidade que representa visitas realizadas por técnicos na residência do cliente. Contém data_agendamento, data_realizacao, resultado, os_id e tecnico_id e status. |
Conta_Receber  | Entidade que representa as obrigações financeiras geradas pelas ordens de serviço. |
Pagamento      | Representa o ato do pagamento em si (transação, comprovante, processamento). Uma CONTA_RECEBER gerar um PAGAMENTO. |

---
