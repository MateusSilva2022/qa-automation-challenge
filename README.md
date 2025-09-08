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




Desafio 2 — UI (Selenium + Pytest)



Stack: Python 3.11 · Selenium 4 · Pytest · Webdriver-Manager · Pytest-HTML

Cenários cobertos (DemoQA):


Forms (Practice Form): preenche com dados aleatórios, faz upload .txt, envia, valida o modal e fecha.

Browser Windows: abre uma nova janela e valida o texto “This is a sample page”.

Alerts: simple alert, timer alert, confirm (OK/Cancel) e prompt com texto.

Web Tables: cria/edita/exclui um registro; cria 12 registros e exclui todos.

Progress Bar: inicia e para antes/igual a 25%; vai a 100% e reseta para 0.

Sortable (List): ordena a lista no modo List para a sequência crescente usando drag-and-drop.


Como rodar localmente

Windows (PowerShell)

Entre em: desafio2\desafio2-selenium

Crie o venv: py -3.11 -m venv .venv

Ative: .\.venv\Scripts\Activate.ps1

Instale deps: pip install -r requirements.txt

Com interface gráfica:
\$env:HEADLESS="0" e depois python -m pytest -q --html=reports/report.html --self-contained-html

Em headless (igual ao CI):
\$env:HEADLESS="1" e depois pytest -q

macOS / Linux

Entre em: desafio2/desafio2-selenium

Crie o venv: python3.11 -m venv .venv

Ative: source .venv/bin/activate

Instale deps: pip install -r requirements.txt

Com interface gráfica:
HEADLESS=0 pytest -q --html=reports/report.html --self-contained-html

Em headless (CI):
HEADLESS=1 pytest -q

Rodando apenas partes (atalhos)

Somente formulário: pytest -q -k practice_form

Somente Web Tables: pytest -q -k web_tables

Somente Progress Bar: pytest -q -k progress_bar

Somente Sortable: pytest -q -k sortable

Somente Alerts: pytest -q -k alerts

Somente Browser Windows: pytest -q -k browser_windows


Relatório

Um relatório HTML é gerado em: desafio2/desafio2-selenium/reports/report.html.

Estrutura resumida

pages/ — Page Objects (PO)

tests/ — testes test_*.py e conftest.py (fixture do driver e screenshot automático em falha)

utils/ — geração de dados aleatórios

assets/ — arquivos de apoio (ex.: upload.txt)

requirements.txt, pytest.ini, README.md

Notas técnicas

O conftest.py maximiza a janela quando HEADLESS="0" e usa --window-size=1920,1080 no headless.

O ChromeDriver é resolvido automaticamente pelo webdriver-manager (não precisa baixar driver manualmente).

As POs removem elementos de anúncio do DemoQA (#fixedban, #adplus-anchor, footer) para evitar interferências no clique/scroll.








