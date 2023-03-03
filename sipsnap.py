"""
IMPORTS AND SETTINGS
"""

import time
import random

#import selenium
import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#setup the browser
options = Options()
options.binary_location = "path to your browser exe"
driver = webdriver.Edge()
driver.get("https://mcdonalds.fast-insight.com/voc/de/de")

#import for openai api
import os
import openai 
from flask import Flask, redirect, render_template, request, url_for

"""
VARIABLES
'$' as the seperator | website parts in german
"""

#splashscreen
splashscreen_xpath = '//*[@id="loading"]/div/div[1]'

#general buttons
camera_button_xpath = '//*[@id="welcomeMessage"]/div[4]/div'
accepted_button_xpath = '//*[@id="sectionHome"]/div[3]/div/label/input'
next_page_xpath = '//*[@id="next-sbj-btn"]'

#Wo hast Du Deine komplette Bestellung erhalten?
headline1 = '//*[@id="118"]/div[3]/h3'
question1 = [
    'Theke$//*[@id="118"]/div[5]/div[1]/div[2]/span', 
    'Tischservice$//*[@id="118"]/div[5]/div[2]/div[2]/span']

#Bitte beurteile Deine Gesamtzufriedenheit basierend auf der Erfahrung Deines letzten Besuches.
headline2 = '//*[@id="67"]/div[3]/h3'
question2 = [
    '1 Stern$//*[@id="67"]/div[5]/div/div[1]/div[1]', 
    '2 Sterne$//*[@id="67"]/div[5]/div/div[1]/div[2]', 
    '3 Sterne$//*[@id="67"]/div[5]/div/div[1]/div[3]', 
    '4 Sterne$//*[@id="67"]/div[5]/div/div[1]/div[4]', 
    '5 Sterne$//*[@id="67"]/div[5]/div/div[1]/div[5]']

#Wie zufrieden warst Du mit der Freundlichkeit unserer Mitarbeiter?
headline3 = '//*[@id="68"]/div[3]/h3'
question3 = [
    '1 Stern$//*[@id="68"]/div[5]/div/div[1]/div[1]', 
    '2 Sterne$//*[@id="68"]/div[5]/div/div[1]/div[2]', 
    '3 Sterne$//*[@id="68"]/div[5]/div/div[1]/div[3]', 
    '4 Sterne$//*[@id="68"]/div[5]/div/div[1]/div[4]', 
    '5 Sterne$//*[@id="68"]/div[5]/div/div[1]/div[5]']

#Wie zufrieden warst Du mit der Schnelligkeit unseres Services?
headline4 = '//*[@id="69"]/div[3]/h3'
question4 = [
    '1 Stern$//*[@id="69"]/div[5]/div/div[1]/div[1]', 
    '2 Sterne$//*[@id="69"]/div[5]/div/div[1]/div[2]', 
    '3 Sterne$//*[@id="69"]/div[5]/div/div[1]/div[3]', 
    '4 Sterne$//*[@id="69"]/div[5]/div/div[1]/div[4]', 
    '5 Sterne$//*[@id="69"]/div[5]/div/div[1]/div[5]']

#Wie zufrieden warst Du mit der Qualität der erhaltenen Speisen und Getränke?
headline5 = '//*[@id="70"]/div[3]/h3'
question5 = [
    '1 Stern$//*[@id="70"]/div[5]/div/div[1]/div[1]', 
    '2 Sterne$//*[@id="70"]/div[5]/div/div[1]/div[2]', 
    '3 Sterne$//*[@id="70"]/div[5]/div/div[1]/div[3]', 
    '4 Sterne$//*[@id="70"]/div[5]/div/div[1]/div[4]', 
    '5 Sterne$//*[@id="70"]/div[5]/div/div[1]/div[5]']

#Wie zufrieden warst Du mit der Sauberkeit des Restaurants?
headline6 = '//*[@id="71"]/div[3]/h3'
question6 = [
    '1 Stern$//*[@id="71"]/div[5]/div/div[1]/div[1]', 
    '2 Sterne$//*[@id="71"]/div[5]/div/div[1]/div[2]', 
    '3 Sterne$//*[@id="71"]/div[5]/div/div[1]/div[3]', 
    '4 Sterne$//*[@id="71"]/div[5]/div/div[1]/div[4]', 
    '5 Sterne$//*[@id="71"]/div[5]/div/div[1]/div[5]']

#Wurde Deine Bestellung ordnungsgemäß zusammengestellt und bearbeitet?
headline7 = '//*[@id="10"]/div[3]/h3'
question7 = [
    'Ja$//*[@id="10"]/div[5]/div[1]/div[2]/span', 
    'Nein$//*[@id="10"]/div[5]/div[2]/div[2]/span']

reason7 = [
    'bestelltes Produkt fehlte$//*[@id="11"]/div[5]/div[1]/div[2]/span', 
    'falsche Speise erhalten$//*[@id="11"]/div[5]/div[2]/div[2]/span', 
    'falsches Getränk erhalten$//*[@id="11"]/div[5]/div[3]/div[2]/span', 
    'falsche Produktgröße erhalten$//*[@id="11"]/div[5]/div[4]/div[2]/span', 
    'Zutaten fehlten$//*[@id="11"]/div[5]/div[5]/div[2]/span', 
    'Servietten etc. nicht vorhanden$//*[@id="11"]/div[5]/div[6]/div[2]/span']

#Gab es während Deines Besuches ein Problem?
headline8 = '//*[@id="81"]/div[3]/h3'
question8 = [
    'Ja$//*[@id="81"]/div[5]/div[1]/div[2]/span', 
    'Nein$//*[@id="81"]/div[5]/div[2]/div[2]/span']

#Basierend auf Deinem Restaurantbesuch, wie wahrscheinlich würdest Du uns auf einer Skala von 0-10 an Freunde und Bekannte weiterempfehlen?
headline9 = '//*[@id="35"]/div[3]/h3'
question9 = [
    '10 - auf alle Fälle$//*[@id="35"]/div[5]/div[1]/div[2]/span',
    '9$//*[@id="35"]/div[5]/div[2]/div[2]/span', 
    '8$//*[@id="35"]/div[5]/div[3]/div[2]/span', 
    '7$//*[@id="35"]/div[5]/div[4]/div[2]/span', 
    '6$//*[@id="35"]/div[5]/div[5]/div[2]/span', 
    '5$//*[@id="35"]/div[5]/div[6]/div[2]/span', 
    '4$//*[@id="35"]/div[5]/div[7]/div[2]/span', 
    '3$//*[@id="35"]/div[5]/div[8]/div[2]/span', 
    '2$//*[@id="35"]/div[5]/div[9]/div[2]/span', 
    '1$//*[@id="35"]/div[5]/div[10]/div[2]/span', 
    '0 - auf keinen Fall$//*[@id="35"]/div[5]/div[11]/div[2]/span']

#Es freut uns, dass Du mit Ihrem letzten Besuch zufrieden warst. Wem oder wofür dürfen wir ein Lob aussprechen?
headline10 = '//*[@id="21"]/div[3]/h3'
chatgpt_storage = [
    'Köstliche Gerichte, angenehme Umgebung.',
    'Tolles Essen, schöne Stimmung.',
    'Leckeres Essen, gemütliche Atmosphäre.',
    'Schmackhaftes Essen, entspannte Atmosphäre.',
    'Gutes Essen, einladende Atmosphäre.',
    'Genießbares Essen, freundliches Ambiente.',
    'Wohlschmeckendes Essen, angenehme Atmosphäre.',
    'Hochwertige Küche, schöne Atmosphäre.',
    'Köstliche Speisen, gemütliches Ambiente.',
    'Leckere Gerichte, entspannte Stimmung.',
    'Gutes Essen, schöne Einrichtung.',
    'Feines Essen, angenehmes Ambiente.',
    'Erstklassiges Essen, ansprechende Atmosphäre.',
    'Schmackhaftes Essen, stilvolles Ambiente.',
    'Leckeres Essen, charmantes Ambiente.',
    'Wohlschmeckende Gerichte, einladendes Ambiente.',
    'Geschmackvolles Essen, herzliche Atmosphäre.',
    'Ausgezeichnetes Essen, stilvolle Einrichtung.',
    'Köstliche Küche, gastfreundliche Atmosphäre.',
    'Hervorragende Gerichte, einladende Stimmung.',
    'Gutes Essen, gastfreundliches Ambiente.',
    'Delikates Essen, ansprechende Einrichtung.',
    'Leckere Speisen, gemütliche Einrichtung.',
    'Hochwertige Speisen, schöne Einrichtung.',
    'Genussvolles Essen, freundliches Ambiente.',
    'Wohlschmeckendes Essen, entspannende Atmosphäre.',
    'Schmackhaftes Essen, einladende Stimmung.',
    'Leckere Gerichte, stilvolle Atmosphäre.',
    'Gutes Essen, warme Atmosphäre.',
    'Köstliche Speisen, geschmackvolle Einrichtung.',
    'Erstklassige Küche, entspannende Atmosphäre.',
    'Feine Gerichte, einladendes Ambiente.',
    'Schmackhafte Küche, ansprechende Stimmung.',
    'Leckere Mahlzeiten, gemütliche Stimmung.',
    'Wohlschmeckendes Essen, herzliche Einrichtung.',
    'Geschmackvolles Essen, stilvolle Stimmung.',
    'Ausgezeichnetes Essen, charmantes Ambiente.',
    'Köstliche Gerichte, freundliche Stimmung.',
    'Hervorragende Küche, einladende Einrichtung.',
    'Gutes Essen, stilvolle Atmosphäre.',
    'Delikate Speisen, ansprechende Einrichtung.',
    'Leckere Mahlzeiten, gastfreundliche Stimmung.',
    'Hochwertige Küche, entspannte Stimmung.',
    'Genießbares Essen, einladende Atmosphäre.',
    'Wohlschmeckende Gerichte, gemütliche Atmosphäre.',
    'Geschmackvolles Essen, freundliche Atmosphäre.',
    'Erstklassige Speisen, entspannte Stimmung.',
    'Schmackhafte Gerichte, ansprechende Atmosphäre.',
    'Köstliche Küche, einladende Stimmung.',
    'Leckeres Essen, stilvolle Einrichtung.']


#Du bist
headline11 = '//*[@id="22"]/div[3]/h3'
question11 = [
    'weiblich$//*[@id="22"]/div[5]/div[1]/div[2]/span', 
    'männlich$//*[@id="22"]/div[5]/div[2]/div[2]/span', 
    'divers$//*[@id="22"]/div[5]/div[3]/div[2]/span']

#Bitte nenne Dein Alter:
headline12 = '//*[@id="23"]/div[3]/h3'
question12 = [
    'bis 14 Jahre$//*[@id="23"]/div[5]/div[1]/div[2]/span', 
    '14-19$//*[@id="23"]/div[5]/div[2]/div[2]/span', 
    '20-29$//*[@id="23"]/div[5]/div[3]/div[2]/span', 
    '30-49$//*[@id="23"]/div[5]/div[4]/div[2]/span', 
    '50+$//*[@id="23"]/div[5]/div[5]/div[2]/span']

#Für wie viele Personen, einschließlich Dir und all Deinen Begleitern/Innen, hast Du heute bezahlt?
headline13 = '//*[@id="56"]/div[3]/h3'
dropdown_page_13 = '//*[@id="56"]/div[5]/div/select'

#Für wie viele Kinder (unter 14 Jahren) hast Du heute bezahlt?
headline14 = '//*[@id="57"]/div[3]/h3'
dropdown_page_14 = '//*[@id="57"]/div[5]/div/select'

#Was war der Besuch bei McDonald's heute für Dich?
headline15 = '//*[@id="58"]/div[3]/h3'
question15 = [
    'eine vollständige Mahlzeit$//*[@id="58"]/div[5]/div[1]/div[2]/span', 
    'eine kleine Zwischenmahlzeit$//*[@id="58"]/div[5]/div[2]/div[2]/span', 
    'nur ein Getränk$//*[@id="58"]/div[5]/div[3]/div[2]/span']

#Wie oft besuchst Du ein McDonald's Restaurant?
headline16 = '//*[@id="24"]/div[3]/h3'
question16 = [
    '1 Mal pro Woche oder öfter$//*[@id="24"]/div[5]/div[1]/div[2]/span', 
    '2-3 Mal im Monat$//*[@id="24"]/div[5]/div[2]/div[2]/span', 
    '1 Mal pro Monat$//*[@id="24"]/div[5]/div[3]/div[2]/span', 
    '1 Mal alle 2-3 Monate$//*[@id="24"]/div[5]/div[4]/div[2]/span', 
    '1 Mal alle 4-6 Monate$//*[@id="24"]/div[5]/div[5]/div[2]/span', 
    'weniger als 2 Mal im Jahr$//*[@id="24"]/div[5]/div[6]/div[2]/span']

#poll finished
chapta_xpath = '//*[@id="recaptcha-anchor"]/div[1]'
send_poll_xpath = '//*[@id="submit-wrapper"]/div[3]/button/span'

#voucher
qr_code_xpath = '//*[@id="imgQRCode"]'
confirm_voucher_xpath = '//*[@id="lblCode1"]'

"""
GENERAL FUNCTIONS
"""

def get_xpath(listname, element):
    return(listname[element].split('$', 1)[-1])

#searching button with xpath and click it
def find_and_click_button(xpath):
    page_button = driver.find_element("xpath", xpath)
    driver.execute_script("arguments[0].click();", page_button)

#returns number of stars
def how_much_stars(a, b, c):#a = weight of three stars, b = weight of four stars, c = weight of five stars
    range_of_choices = ["three_stars", "four_stars", "five_stars"]
    return(random.choices(range_of_choices, weights= [a, b, c], k = 1))

def next_page():
    find_and_click_button(next_page_xpath)
    print('next page')#debug

def delay_poll():
    time.sleep(0.5)

#good or bad feedback?
def how_likely(chance):
    if random.randint(0,100) < chance:
        answer = True
    else:
        answer = False
    print(f'how likely (chance {chance}): {answer}')#debug
    return(answer)

weight_3_stars = 3
weight_4_stars = 10
weight_5_stars = 10

#fill out page with star rating
def star_rating(list):
    given_stars = how_much_stars(weight_3_stars, weight_4_stars, weight_5_stars)
    print(f'stars: {given_stars}')#debug
    if given_stars == ['three_stars']:
        xpath_of_star_button = get_xpath(list, 2)
        find_and_click_button(xpath_of_star_button)
    if given_stars == ['four_stars']:
        xpath_of_star_button = get_xpath(list, 3)
        find_and_click_button(xpath_of_star_button)
    if given_stars == ['five_stars']:
        xpath_of_star_button = get_xpath(list, 4)
        find_and_click_button(xpath_of_star_button)
    return(given_stars)

def check_and_run_question_page(runpage, xpath_headline):
    try:
        driver.find_element("xpath", xpath_headline)
        print(f"{runpage}: Running page")
        runpage()
    except:
        print(f"{runpage}: Page not found")

"""
FUNCTIONS FOR PROCESSING POLL
"""

def run_landingpage():
    find_and_click_button(camera_button_xpath)
    accepted_button = driver.find_element("xpath", accepted_button_xpath)
    accepted_button.send_keys("path to receipt")#path of receipt (picture)

def uncertified_picture():
    input_gap = driver.find_element("xpath", '//*[@id="receiptCode"]')
    input_gap.clear()
    feedback_code = input('The picture was not certified. Please type it in:\n')
    feedback_code.replace('-', '')
    
    while feedback_code.isalnum() == False:#input contains special characters
        feedback_code = input('\nNot valid. Type it in again:\n\n') 
        feedback_code.replace('-', '')
    
    #send code to website     
    input_gap.send_keys(feedback_code)
    find_and_click_button('//*[@id="welcomeMessage"]/div[4]/button')
    time.sleep(3)
    picture_validation()

def picture_validation():
    try:
        invalid_picture = driver.find_element('xpath', ('//*[@id="receiptCode"]')).is_displayed()
        if invalid_picture == True:
            uncertified_picture()
        invalid_picture_counter = invalid_picture_counter + 1
    except:
        None

def wait_for_poll():
    poll_loading = True
    while (poll_loading == True):
        try:
            poll_loading = driver.find_element('xpath', ('//*[@id="loading"]/div/div[1]')).is_displayed()
        except:
            print("poll loaded successfully")
            poll_loading = False
            time.sleep(0.1)

def run_page_1():
#page1
    print('where service?')
    if how_likely(70) == True:
        find_and_click_button(get_xpath(question1, 1))
        print('page1: Tischservice')#debug
    else:
        find_and_click_button(get_xpath(question1, 0))
        print('page1: Thekenservice')#debug
    delay_poll()
    next_page()

def run_page_2():
#page2
    find_and_click_button('//*[@id="67"]/div[5]/div/div[1]/div[5]')
    delay_poll()
    next_page()

def run_page_3():
#page3
    star_rating(question3)
    delay_poll()
    next_page()

def run_page_4():
#page4
    star_rating(question4)
    delay_poll()
    next_page()

def run_page_5():
#page5
    star_rating(question5)
    delay_poll()
    next_page()

def run_page_6():
#page6
    star_rating(question6)
    delay_poll()
    next_page()

def run_page_7():
#page7
    find_and_click_button(get_xpath(question7, 0))
    print(f'page7: Ja')#debug
    delay_poll()
    next_page()

def run_page_8():
#page8
    find_and_click_button(get_xpath(question8, 1))
    print(f'page8: Nein')#debug
    delay_poll()
    next_page()

def run_page_9():
#page9
    answer_page_9 = random.choices([0, 1, 2, 3, 4], weights= [10, 9, 8, 7, 6], k = 1)
    element_page_9 = list(map(int, answer_page_9))
    find_and_click_button(get_xpath(question9, element_page_9[0]))
    print(f'page9: {answer_page_9}')#debug
    delay_poll()
    next_page()

def run_page_10():
#page 10
    try:
        openai.api_key = 'your OpenAI API key'
        answer_page_10 = openai.Completion.create(
        model="text-davinci-003",
        prompt="Beschreibe in sehr wenigen Worten, was dir am Restaurantbesuch gefallen hat.",
        temperature=0.7,
        max_tokens=150,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=1
        )
        print(f'page10: {answer_page_10["choices"][0]["text"]}')#debug
    except:
        answer_page_10 = chatgpt_storage[random.randint(0, 49)]
        print(f'page10: {answer_page_10["choices"][0]["text"]}')#debug
    text_box_page_10 = driver.find_element("xpath", '//*[@id="21"]/div[5]/div/input')
    text_box_page_10.send_keys(answer_page_10["choices"][0]["text"])
    delay_poll()
    next_page()

def run_page_11():
#page11
    if how_likely(1) == True:
        find_and_click_button(get_xpath(question11, 2))
        print(f'page11: divers')#debug
    else:
        if how_likely(50) == True:
                find_and_click_button(get_xpath(question11, 0))
                print(f'page11: weiblich')#debug
        else:
                find_and_click_button(get_xpath(question11, 1))
                print(f'page11: männlich')#debug
    delay_poll()
    next_page()

def run_page_12():
#page12
    answer_page_12 = random.randint(0, 4)
    find_and_click_button(get_xpath(question12, answer_page_12))
    print(f"page12:{question12[answer_page_12].split('$', 1)[0]}")
    delay_poll()
    next_page()

def run_page_13():
#page13
    select_page_13 = Select(driver.find_element("xpath", dropdown_page_13))
    dropdown_choice_page_13 = random.choices(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10 oder mehr'], weights= [100, 65, 40, 30, 20, 15, 10, 5, 5, 1], k = 1)
    element_page_13 = list(map(str, dropdown_choice_page_13))
    print(f'page13: {element_page_13[0]}')#debug
    select_page_13.select_by_visible_text(dropdown_choice_page_13[0])
    delay_poll()
    next_page()

def run_page_14():
#page14
    select_page_14 = Select(driver.find_element("xpath", dropdown_page_14))
    dropdown_choice_page_14 = random.choices(['0', '1', '2', '3', '4 oder mehr'], weights= [20, 5, 5, 5, 1], k = 1)
    element_page_14 = list(map(str, dropdown_choice_page_14))
    print(f'page14: {element_page_14[0]}')#debug
    select_page_14.select_by_visible_text(element_page_14[0])
    delay_poll()
    next_page()

def run_page_15():
#page15
    if how_likely(10) == True:
        find_and_click_button(get_xpath(question15, 2))
        print(f'page15: nur ein Getränk')#debug
    else:
        if how_likely(50) == True:
                find_and_click_button(get_xpath(question15, 0))
                print(f'page15: eine vollständige Mahlzeit')#debug
        else:
                find_and_click_button(get_xpath(question15, 1))
                print(f'page15: eine kleine Zwischenmahlzeit')#debug
    delay_poll()
    next_page()

def run_page_16():
#page16
    answer_page_16 = random.choices([0, 1, 2, 3, 4, 5], weights= [10, 15, 25, 20, 10, 5], k = 1)
    element_page_16 = list(map(int, answer_page_16))
    print(f"page16: {element_page_16[0]}")#debug
    find_and_click_button(get_xpath(question16, element_page_16[0]))
    delay_poll()
    next_page()

def run_page_voucher():
#voucher page
    time.sleep(10)
    path_store_voucher = "path to store the qr code"
    reward_saved = False
    reward_counter = 0
    if driver.find_element('xpath', '//*[@id="imgQRCode"]').is_displayed() == True:
        while reward_saved == False:
            try:
                complete_name_qr = os.path.join(path_store_voucher, f"qr{reward_counter}.png")
                complete_name_code = os.path.join(path_store_voucher, f"code{reward_counter}.txt")         
                qr = open(complete_name_qr, "xb")
                code = open(complete_name_code, "xt")
                qr.write(driver.find_element('xpath', '//*[@id="imgQRCode"]').screenshot_as_png)
                code.write(driver.find_element('xpath', '//*[@id="lblCode1"]').text)
                qr.close()
                code.close()
                reward_saved = True
                input(f'QR Code and Voucher Code saved in "{path_store_voucher}". Enter to close browser.')
            except:
                os.remove(f"{path_store_voucher}/qr{reward_counter}.png")
                os.remove(f"{path_store_voucher}/code{reward_counter}.txt")
                reward_counter = reward_counter + 1
    else:
        print('No voucher displayed')

"""
EXECUTED STEPS
"""

time.sleep(2)

run_landingpage()

time.sleep(8)

picture_validation()

wait_for_poll()

check_and_run_question_page(run_page_1, headline1)

check_and_run_question_page(run_page_2, headline2)

check_and_run_question_page(run_page_3, headline3)

check_and_run_question_page(run_page_4, headline4)

check_and_run_question_page(run_page_5, headline5)

check_and_run_question_page(run_page_6, headline6)

check_and_run_question_page(run_page_7, headline7)

check_and_run_question_page(run_page_8, headline8)

check_and_run_question_page(run_page_9, headline9)

check_and_run_question_page(run_page_10, headline10)

check_and_run_question_page(run_page_11, headline11)

check_and_run_question_page(run_page_12, headline12)

check_and_run_question_page(run_page_13, headline13)

check_and_run_question_page(run_page_14, headline14)

check_and_run_question_page(run_page_15, headline15)

check_and_run_question_page(run_page_16, headline16)

input('Captcha solved? Enter to continue')

run_page_voucher()

driver.quit()
driver.close()
