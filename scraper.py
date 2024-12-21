from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def open_page(driver, url):
    driver.get(url)
    time.sleep(2)

def perform_initial_clicks(driver):
    
    try:        
        # Aceitar cookies
        try:
            wait = WebDriverWait(driver, 10)
            accept_cookies_button = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//button[contains(text(), 'ACEITAR TODOS OS COOKIES')]")
            ))
            accept_cookies_button.click()
            time.sleep(2)
        except:
            print("Botão de cookies não encontrado ou já aceito.")

        # Verificar idade
        try:
            age_verification_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Eu tenho mais de 18 anos')]")
            age_verification_button.click()
            time.sleep(2)
        except:
            print("Verificação de idade não encontrada ou já feita.")

        # Clicar no botão 'Entrar'
        try:
            enter_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Entrar')]")
            enter_link.click()
            time.sleep(2)
        except:
            print("Link 'Entrar' não encontrado.")

        # Preencher o formulário de login
        try:
            username_field = driver.find_element(By.XPATH, "//input[@name='username']")
            password_field = driver.find_element(By.XPATH, "//input[@name='password']")
            login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Entrar')]")

            # Substitua pelas suas credenciais
            username_field.send_keys("maurorajr@gmail.com")
            password_field.send_keys("*sAmsung1988*")
            login_button.click()

            print("Login realizado com sucesso.")
        except:
            print("Erro ao preencher ou encontrar o formulário de login.")

    finally:
        # Fechar o navegador após a execução
        time.sleep(5)  # Aguardar para visualização manual, se necessário
        #driver.quit()
          

def resume_deposits(driver, url):
    """
    Acessa a página de depósitos e extrai dados reais.
    """
    try:
        # Navega para a página de depósitos
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "user-table"))
        )

        # Rolagem para carregar todos os elementos
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Coleta os dados da tabela de depósitos
        rows = driver.find_elements(By.XPATH, "//table[@class='default user-table desktop-only']/tbody/tr")
        deposits = []

        for row in rows:
            data = row.find_elements(By.TAG_NAME, "td")
            if len(data) < 5:
                continue  # Ignora linhas incompletas

            # Extração e limpeza dos dados
            deposit_date = data[0].text.strip()  # Data
            deposit_id = data[1].text.strip()  # ID
            deposit_type = data[2].text.strip()  # Tipo
            deposit_amount = data[3].text.strip().replace('R$', '').replace(' ', '').replace(',', '.')  # Quantia
            deposit_status = data[4].text.strip()  # Status

            deposits.append({
                "date": deposit_date,
                "id": deposit_id,
                "type": deposit_type,
                "amount": float(deposit_amount),
                "status": deposit_status
            })

        return deposits
    except Exception as e:
        print(f"Erro ao extrair depósitos: {e}")
        return []

