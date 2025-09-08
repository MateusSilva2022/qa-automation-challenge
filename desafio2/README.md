--Desafio Frontend – Parte 2 (Python + Selenium)--

Automação dos cenários do DemoQA com Selenium + Pytest.
Projeto preparado para rodar no VS Code/Windows (funciona também em macOS/Linux).

------O que este projeto testa------

Forms

Practice Form: preenche com dados aleatórios, faz upload .txt, submete, valida o modal e fecha.

Alerts, Frame & Windows

Browser Windows: abre nova janela, valida “This is a sample page” e fecha.

Elements

Web Tables: cria, edita e exclui registro; bônus cria 12 registros e exclui todos.

Widgets

Progress Bar: start → para ≤ 25%, continua até 100%, e reseta (0%).

Interactions

Sortable: drag & drop para ordenar a lista One..Six em ordem crescente.

Extras de infraestrutura: webdriver-manager (driver automático), relatório HTML, screenshot automático em falha, remoção de banners/ads do site, suporte a Headless.

------Como rodar------
1) Preparar o ambiente

Requer Python 3.11+ e Google Chrome instalados.

Windows (PowerShell)

py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt


macOS / Linux

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

2) Executar os testes

Mostrar o navegador:

$env:HEADLESS="0"; pytest -q --html=reports/report.html --self-contained-html


Headless (padrão):

pytest -q --html=reports/report.html --self-contained-html


Rodar um grupo específico (exemplos):

pytest -q -k practice_form    # só o Practice Form
pytest -q -k browser_windows  # só Browser Windows
pytest -q -k web_tables       # só Web Tables
pytest -q -k progress_bar     # só Progress Bar
pytest -q -k sortable         # só Sortable
pytest -q -m e2e              # todos marcados como e2e


O relatório estará em: reports/report.html.

------Estrutura principal------
pages/
  alerts_page.py
  browser_windows_page.py
  practice_form_page.py
  progress_bar_page.py
  sortable_page.py
  web_tables_page.py
tests/
  conftest.py
  test_alerts.py
  test_browser_windows.py
  test_practice_form.py
  test_progress_bar.py
  test_sortable.py
  test_web_tables.py
utils/
  data.py
assets/
  upload.txt
pytest.ini
requirements.txt

------Configurações úteis------

Headless: controlado pela variável HEADLESS.

HEADLESS="0" → abre o Chrome

HEADLESS="1" (ou ausente) → roda sem UI

Screenshots em falha: salvos automaticamente em
reports/screenshots/<nome_do_teste>.png.

Remoção de banners/ads: cada Page Object remove elementos que podem bloquear cliques no DemoQA.

------Dicas e solução de problemas------

TimeoutException
Rede lenta? Aumente TIMEOUT no Page Object do cenário afetado.

Logs barulhentos do Chrome/Driver
Para silenciar, no tests/conftest.py adicione:

options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
options.add_argument("--log-level=3")
from subprocess import DEVNULL
service = Service(ChromeDriverManager().install(), log_output=DEVNULL)


Drivers
O webdriver-manager baixa o ChromeDriver compatível automaticamente.
Se a rede bloquear downloads, rode com internet liberada ao menos uma vez.

------Como os testes validam------

Practice Form: lê o modal e compara todas as colunas (nome, email, gênero, mobile, subjects, hobbies, endereço, estado e cidade).

Browser Windows: troca de janela e valida o #sampleHeading.

Web Tables: usa o searchBox por e-mail para localizar, edita e confirma colunas, e depois exclui.

Progress Bar: controla a barra até ≤ 25%, depois até 100% e verifica reset (0%).

Sortable: realiza drag & drop passo a passo (trocando com vizinhos) até alcançar a ordem final esperada.

------Comandos rápidos (cola e usa)------
# criar venv e instalar
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# rodar tudo com UI e gerar relatório
$env:HEADLESS="0"; pytest -q --html=reports/report.html --self-contained-html

# rodar só um cenário
pytest -q -k progress_bar --html=reports/report.html --self-contained-html