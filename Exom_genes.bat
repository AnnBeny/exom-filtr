:: verze pro Win s WSL
@echo off
::start "" wsl bash -lc "cd /mnt/d/ann/exom_genes && ./run.sh"
start "" wsl -e bash -lc "source /mnt/d/ann/exom_genes/venv/bin/activate && cd /mnt/d/ann/exom_genes && streamlit run app/app.py --server.port=8501"
::pause
timeout /t 5 /nobreak >null
start "" http://localhost:8501
 
:: verze pro Win bez WSL <- odkomentovat
::@echo off
::cd /d D:\cesta\ke\slozce\exom_genes
::call D:\cesta\ke\slozce\exom_genes\venvn\Scripts\activate
::start "" streamlit run app\app.py --server.port=8501
::timeout /t 5 /nobreak >nul
::start "" http://localhost:8501

:: nastaveni pouziti konkretniho configu Streamlitu - zatim nepotrebuju
::set STREAMLIT_CONFIG_DIR=%~dp0\.streamlit

:: spusteni Streamlitu z binarky (na Linux bin misto Scripts)
::"%CD%\venv\Scripts\streamlit.exe" run app\app.py
::"%~dp0venv\Scripts\streamlit.cmd" run "%~dp0app\app.py"

:: pouziti, kdyz Streamlit neni v PATH nebo potrebuju konkretni Python
::wsl -e python3 -m streamlit run /mnt/hdd2/ann/exome_genes/app/app.py

::pause
