@echo off
echo ========================================
echo  AI Research Assistant Setup
echo ========================================
echo.

echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate

echo.
echo Installing packages...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Downloading models (this may take a few minutes)...
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
python -c "from transformers import AutoTokenizer, AutoModelForCausalLM; AutoTokenizer.from_pretrained('microsoft/phi-2')"

echo.
echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo To run the application:
echo 1. Activate virtual environment: venv\Scripts\activate
echo 2. Run: streamlit run app.py
echo.
pause