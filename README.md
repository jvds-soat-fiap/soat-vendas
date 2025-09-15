
# Plataforma de Venda de Veículos - FIAP

Este projeto implementa uma **plataforma de revenda de veículos automotores** baseada em **microsserviços**, utilizando **arquitetura hexagonal** e o padrão de transações distribuídas **SAGA (Orquestrador)**. A solução expõe APIs RESTful que poderão ser integradas futuramente por uma interface web (frontend).

---

## 🏗️ Arquitetura

A arquitetura é composta por múltiplos serviços independentes:

- `soat-vendas`: Faz toda a orquestração para venda de veículos e pagamentos.

Cada serviço segue o padrão **Hexagonal (Ports & Adapters)** para isolamento de regras de negócio.

---

## 🔁 Orquestração SAGA Vendas

O fluxo de cadastro veículo é o serviço responsável em cadastrar os veículos para venda tendo a seguintes funcionalidade

1. Cadastrar veículos através do verbo HTTP Post.
2. Efetuar busca pelo ID do veículo para trazer os dados cadastrais utilizando o verbo HTTP Get.
3. Listagem dos veículos disponível para venda pôr ordem do menor valor.
4. Listagem dos veículos vendidos pôr ordem do menor valor.
5. Atualização do status do veículos para DISPONIVEL.
6. Atualização do status do veículos para RESERVADO.
7. Atualização do status do veículos para VENDIDO.

---

## 🚀 Como executar o projeto

Pré-requisitos:
- Python 3.9+
- Docker e Docker Compose (opcional, mas recomendado)

### ▶️ Iniciar a execução com o DOCKER dos serviços
1. Deve baixar os seguintes projetos estando na mesma estrutura de diretorio
   - [soat-veiculos](https://github.com/jvds-soat-fiap/soat-vendas)
   - [soat-compradores](https://github.com/jvds-soat-fiap/soat-compradores.git)
   - [soat-pagamentos](https://github.com/jvds-soat-fiap/soat-pagamentos.git)
   - [soat-vendas](https://github.com/jvds-soat-fiap/soat-vendas.git)
2. Após baixar os projetos deve seguir conforme as instruções abaixo
```bash
cd soat-vendas/ci
docker-compose -f docker-compose-local.yml up -d
```
3. Deve importar a collection **soat-veiculos-collection.json** do Insomnia que existe no projeto **soat-vendas**


### ▶️ Iniciar a execução LOCAL somente do serviço específico
1. Deve ir até a raiz do diretório do serviço específico
```
python -m venv .venv
```
2. Ativar o ambiente virtual do serviço desejado
```
source .venv/bin/activate
export PYTHONPATH=$PWD/app
```
3. Instalar as libs do serviço específico no ambiente ativado virtual
```
pip install -r requirements.txt
pip freeze > requirements.txt
```
4. Executar o serviço específico no ambiente virtual
```
.venv/bin/python app/main.py
```

**Desativando Ambiente Virtual**
```
deactivate
```
---


## 📚 Endpoints Principais

### Vendas (`localhost:8003`)
- `GET /soat-veiculo/v1/vendas/health/actuator`
- `POST /soat-veiculo/v1/vendas`
- `PATCH /soat-veiculo/v1/vendas/{venda_id}/concluir`

---

## 🔐 Segurança de Dados

- Dados sensíveis de compradores são **criptografados** em repouso.
- A comunicação entre os microsserviços pode ser protegida por mTLS (não implementado nesta versão).
- O sistema é projetado para garantir **confidencialidade e integridade** no tratamento de dados pessoais.

---

## MongoDB Local
- Acesso a database: http://localhost:8081.

## 📦 Organização de Código

Cada serviço segue a estrutura:

```
app/
├── adapters/          # Entrada e saída (ex: API REST, clients HTTP, repository DATABASE)
├── application/       # Casos de uso
├── domain/            # Regras de negócio (entidades)
├── infrastructure/    # Integração com serviços externos
├── main.py            # Inicialização do app
```

---

## 👨‍💻 Desenvolvido por

Projeto acadêmico desenvolvido por João Vitor da Silva como parte da prova substitutiva Pós-Tech de Arquitetura de Software (FIAP).  

---
