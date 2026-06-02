# Sistema de Gestão de Assistência Técnica

## 1. Objetivo

Desenvolver um sistema web para gerenciar clientes, equipamentos e ordens de serviço de uma assistência técnica, permitindo o acompanhamento completo do processo de manutenção.

---

## 2. Funcionalidades

### Cliente

* Cadastrar cliente
* Consultar cliente
* Atualizar dados do cliente
* Excluir cliente

### Equipamento

* Cadastrar equipamento
* Associar equipamento a OS
* Consultar equipamentos cadastrados

### Ordem de Serviço

* Abrir ordem de serviço
* Registrar defeitos apresentados
* Atualizar status da manutenção
* Encerrar ordem de serviço
* Calcular valor total do serviço

### Funcionário

* Cadastrar técnico
* Cadastrar atendente
* Controlar permissões de acesso

---

## 3. Requisitos Funcionais

### RF01

O sistema deve permitir o cadastro de clientes.

### RF02

O sistema deve permitir o cadastro de equipamentos.

### RF03

O sistema deve permitir a abertura de ordens de serviço.

### RF04

O sistema deve permitir a atualização do status da ordem de serviço.

### RF05

O sistema deve permitir o encerramento de uma ordem de serviço.

### RF06

O sistema deve emitir notificações quando houver alteração no status da ordem.

---

## 4. Requisitos Não Funcionais

### RNF01

O sistema deve possuir interface amigável.

### RNF02

O sistema deve armazenar dados em banco de dados relacional.

### RNF03

O código deve seguir os princípios SOLID.

### RNF04

O sistema deve possuir testes unitários.

### RNF05

O sistema deve utilizar padrões de projeto.

---

## 5. Arquitetura do Sistema

O sistema seguirá o padrão MVC.

### Model

Responsável pelas entidades e regras de negócio.

### View

Responsável pela interface com o usuário.

### Controller

Responsável por receber as requisições e acionar os serviços.

### Service

Contém a lógica de negócio.

### Repository

Responsável pelo acesso ao banco de dados.

---

## 6. Entidades Principais

### Cliente

| Campo    | Tipo   |
| -------- | ------ |
| id       | Long   |
| nome     | String |
| cpf      | String |
| telefone | String |
| email    | String |

### Equipamento

| Campo   | Tipo    |
| ------- | ------- |
| id      | Long    |
| nome    | String  |
| marca   | String  |
| modelo  | String  |
| cliente | Cliente |

### OrdemServico

| Campo        | Tipo        |
| ------------ | ----------- |
| id           | Long        |
| dataAbertura | LocalDate   |
| defeito      | String      |
| status       | StatusOS    |
| valor        | Double      |
| equipamento  | Equipamento |

---

## 7. Padrões de Projeto Utilizados

### GRASP Expert

A classe OrdemServico será responsável por calcular o valor total do serviço.

### GRASP Creator

A classe Cliente poderá criar e gerenciar seus equipamentos.

### GRASP Controller

A classe OrdemServicoController coordenará as operações relacionadas às ordens de serviço.

### Strategy

Implementação de diferentes formas de pagamento:

* Pix
* Cartão
* Dinheiro

### Factory Method

Criação de diferentes tipos de usuários:

* Cliente
* Técnico
* Atendente

### Singleton

Gerenciamento da conexão com o banco de dados.

### Observer

Notificação automática quando a ordem de serviço mudar de status.

### Decorator

Adição de serviços extras:

* Limpeza
* Formatação
* Troca de peças

---

## 8. Tecnologias Utilizadas

* Java 21
* Spring Boot
* Spring Data JPA
* PostgreSQL
* JUnit 5
* Maven
* Git
* GitHub

---

## 9. Casos de Uso

### Abrir Ordem de Serviço

1. Cliente entrega equipamento.
2. Atendente registra o defeito.
3. Sistema cria uma nova ordem de serviço.
4. Ordem recebe status "Aberta".

### Atualizar Status

1. Técnico realiza manutenção.
2. Sistema atualiza o status.
3. Cliente recebe notificação.

### Encerrar Ordem de Serviço

1. Técnico conclui manutenção.
2. Sistema calcula valor final.
3. Ordem recebe status "Concluída".

---

## 10. Estrutura de Pacotes

```text
src/
├── controller
├── service
├── repository
├── model
├── dto
├── factory
├── strategy
├── observer
├── decorator
└── config
```

## 11. Resultado Esperado

O sistema deverá permitir o gerenciamento completo de uma assistência técnica, controlando clientes, equipamentos e ordens de serviço de forma organizada, aplicando os princípios SOLID e os padrões de projeto estudados na disciplina.
