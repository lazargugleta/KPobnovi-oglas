from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from credentials import email, password
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import glob
import os

DRIVER_PATH = '/home/veloce/Downloads/KPobnovi-oglas/chromedriver'
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

root_dir = '/home/veloce/Documents/KP/'


def login():
    try:
        driver.get("https://novi.kupujemprodajem.com/login")
        sleep(1)
        email_input = driver.find_element(By.ID, "email")
        email_input.send_keys(email)
        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys(password)
        try:
            WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div/section/div[2]/form/button"))).click()
            driver.find_element(By.XPATH, "//button[contains(text(), 'Ulogujte se')]").click()
        except:
            print("Nije uspelo")
            # TODO: Napraviti bolje stabilnije logovanje
            exit()
        sleep(1.5)
        print("Ulogovan")
        return 1

    except Exception as e:
        print(e)
        driver.quit()

def postavi_oglas(naslov, kategorija, grad, stanje, fiksno = False, zamena = False):
    driver.get("https://novi.kupujemprodajem.com/postavljanje-oglasa?action=new")
    sleep(5)
    # ODABIR KATEGORIJE
    # funkcionise na osnovu naslova oglasa i bira prvu kategoriju koju KP ponudi
    # TODO: Custom kategorija
    driver.find_element(By.ID, "groupSuggestText").send_keys(naslov)
    sleep(0.5)
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div/div/form/div[2]/div/div[1]/div[2]/section/section[1]/div/section/div/div/button").click()
    sleep(1)
    # nakon unosa naslova, prva kategorija se automatski selektuje
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div/div/form/div[2]/div/div[1]/div[2]/section/section[1]/div/section/section/button[1]").click()
    sleep(2)
    # TODO: dodati nudim/trazim
    # Slike
    # TODO: Take in multiple different formats of images
    slike_upload = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div/div/form/div[2]/div/div[2]/div[2]/section/section[1]/div/section[2]/div/div/div/div/input")
    slike = []
    for filename in sorted(glob.iglob(root_dir + naslov + '/*.jpg', recursive=False)):
        slike.append(filename)
    slike_upload.send_keys('\n'.join(slike))
    # cena_valuta = glob.iglob(root_dir + naslov + '/cena.txt', recursive=False)
    cena_valuta_text = open(root_dir + naslov + '/cena.txt', 'r').read().split(' ')
    cena = cena_valuta_text[0]
    valuta = cena_valuta_text[1].strip()
    driver.find_element(By.ID, "price").send_keys(cena)
    currency = driver.find_elements(By.NAME, "currency")
    if valuta == "din":
        currency[0].click()
    elif valuta == "eur":
        currency[1].click()

    # STANJE
    stanje_section = driver.find_element(By.CLASS_NAME, "AdSaveCondition_conditionHolder__S9bfd")
    buttons = stanje_section.find_elements(By.TAG_NAME, "button")
    if stanje == 1: # KAO NOVO
        buttons[0].click()
    elif stanje == 2: # KORIŠĆENO
        buttons[1].click()
    elif stanje == 3: # NOVO
        buttons[2].click()
    elif stanje == 4: # OŠTEĆENO
        buttons[3].click()
    sleep(1)

    # OPIS
    driver.switch_to.frame(driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div/div/form/div[2]/div/div[2]/div[2]/section/section[1]/div/section[3]/section[5]/section/div/div/div[1]/div[1]/div[1]/iframe"))
    opis_text = open(root_dir + naslov + '/opis.txt', 'r').read()
    opis_textarea = driver.find_element(By.XPATH, '/html/body/p')
    opis_textarea.click()
    opis_textarea.clear()

    opis_textarea.send_keys(opis_text)
    sleep(1)
    driver.switch_to.default_content()
    sleep(5)

    sledece_btn = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div/div/form/div[1]/section/div/button[2]")
    sledece_btn.click()
    sleep(1)
    
    # TODO: odabir specijalnih oglasa
    sledece_btn.click()
    sleep(1)

    # TODO: Fizicko lice / firma

    # PRIHVATAM USLOVE
    driver.find_element(By.XPATH, '//span[label/input[@name="accept"]]').click()
    sleep(1)

    # Postavite oglas
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div/div/form/div[2]/div/div[4]/div[2]/section/div/section/div/button[2]").click()
    sleep(5)

naslovi = os.listdir('/home/veloce/Documents/KP')
# TODO: Dodati citanje iz baze / csv file-a za naslov, opis i cenu

if login() == True:
    for naslov in naslovi:
        if naslov == "ARHIVA":
            continue
        postavi_oglas(naslov, "kategorija", "grad" , 1, True)