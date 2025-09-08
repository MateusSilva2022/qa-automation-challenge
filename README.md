# QA Automation Challenge

Monorepo para os desafios de automação.  
O **Desafio 1** (DemoQA) já está implementado com **API + UI + BDD (pytest-bdd)**.  
A pasta **desafio2/** está reservada para a próxima etapa.

---

## Estrutura

qa-automation-challenge/
├─ desafio1/
│  └─ demoqa_qa_challenge/      # projeto do Desafio 1 (API + UI + BDD)
└─ desafio2/                     # Desafio 2

---

## Requisitos

- Python 3.11+ (testado com 3.12)
- Google Chrome instalado (para os testes de UI)
- Windows, macOS ou Linux

> Windows/PowerShell: se houver erro ao ativar o venv, rode uma vez:
> Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

---

## Instalação

Clone o repositório e entre no projeto do Desafio 1:

git clone https://github.com/MateusSilva2022/qa-automation-challenge.git
cd qa-automation-challenge/desafio1/demoqa_qa_challenge

Crie e ative o ambiente virtual e instale as dependências.

Windows (PowerShell):
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

macOS/Linux (bash/zsh):
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

Opcional: existe um arquivo .env.example. Se quiser alterar variáveis (ex.: base URL), copie para .env e ajuste os valores.

---

## Como executar

Todos os comandos abaixo devem ser executados dentro de:
qa-automation-challenge/desafio1/demoqa_qa_challenge

Tudo (API + UI + BDD) — gera report_all.html na raiz do projeto:
pytest --html=report_all.html --self-contained-html

Somente API:
pytest -k api --html=report_api.html --self-contained-html

Somente BDD:
pytest tests/bdd --html=report_bdd.html --self-contained-html

Somente UI:
pytest -k ui --html=report_ui.html --self-contained-html

Obs.: os testes de UI executam em modo headless por padrão.

---

## Relatórios

Após a execução, os arquivos HTML ficam na raiz do projeto (Desafio 1):

- report_all.html — execução completa
- report_api.html — testes de API
- report_bdd.html — cenários BDD
- report_ui.html — testes de UI

Abra o arquivo desejado no navegador para visualizar.

---

## Observações

- Os testes de UI usam webdriver-manager, que baixa e gerencia o ChromeDriver automaticamente.
- Se o DemoQA estiver indisponível, é esperado que testes de API/UI falhem por indisponibilidade do ambiente alvo.








