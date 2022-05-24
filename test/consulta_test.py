#import os
import time

import pytest
from selenium import webdriver

from pages import consulta_page
from pages.consulta_page import ConsultaPage


@pytest.fixture  # como se fosse configuração
def consulta(driver):
   return consulta_page.ConsultaPage(driver) #instanciando a classe ConsultaPage e passando o selenium


def testarpreco(consulta):
    #atime.sleep(7)
    consulta.buscar_('Biscoito Golden Cookie para Cães Adultos 350g')
    #consulta.buscar_('Ração Premier para Cães Adultos de Raças Grandes Sabor Carne 15kg')


    assert consulta._encontrartext('Biscoito Golden Cookie para Cães Adultos 350g')
    #assert consulta._encontrar('Biscoito Golden Cookie para Cães Adultos 350g')
