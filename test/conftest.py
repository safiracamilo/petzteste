import os

import pytest
from selenium import webdriver

from . import config, credentials


def pytest_addoption(parser):
    parser.addoption(
        '--baseurl',
        action ='store',
        default ='https://www.petz.com.br/',
        help='Url base da aplicacao alvo do teste'
    )
    parser.addoption(
        '--host',
        action = 'store',
        default ='saucelabs',
        help = 'Onde vamos executar nossos testse: localhost ou saucelabs'
    )
    parser.addoption(
        '--browser',
        action='store',
        default='chrome',
        help='Onde vamos executar nossos teste: localhost ou saucelabs'
    )
    parser.addoption(
        '--browserversion',
        action='store',
        default='101.0',
        help='Versão do browser'
    )
    parser.addoption(
        '--platform',
        action='store',
        default='Windows 10',
        help='Sistema Operacional a ser ultizado durant os teste(apenas no saucelabs)'
    )

@pytest.fixture # inicialização dos testes - similiar a um Before
def driver(request):
    config.baseurl = request.config.getoption('--baseurl')
    config.host = request.config.getoption('--host')
    config.browser = request.config.getoption('--browser')
    config.browserversion= request.config.getoption('--browserversion')
    config.platform = request.config.getoption('--platform')

    if config.host == 'saucelabs':
        test_name = request.node.name #nome do teste
        capabilities = {
            'browserName': config.browser,
            'browserVersion': config.browserversion,
            'platformName': config.platform,
            'sauce:options': {
                'name': test_name
            }
        }
        #_credentials = os.environ['Safira'] + ':' + os.environ['2104662c-ea5a-4957-8d1a-79908ff0899e'] # as informações estão no site saucelabs
        _credentials = credentials.SAUCE_USERNAME + ':' + credentials.SAUCE_ACCESS_KEYS
        _url = 'https://Safira:2104662c-ea5a-4957-8d1a-79908ff0899e@ondemand.eu-central-1.saucelabs.com:443/wd/hub'
        #_url = 'https://' + _credentials + '@ondemand.eu-central-1.saucelabs.com:443/wd/hub'  # copiar do site na parte driver creation e apagar tudo antes do @
        driver_ = webdriver.Remote(_url, capabilities)

    else:# execução local
        if config.browser == 'chrome':
            _chromedriver = os.path.join(os.getcwd(), 'vendor', 'chromedriver.exe')
            if os.path.isfile(_chromedriver):
                driver_ = webdriver.Chrome(_chromedriver)
            else:
                driver_ = webdriver.Chrome()
        elif config.browser == 'firefox':
            _geckodriver = os.path.join(os.getcwd(), 'vendor', 'geckodriver.exe')
            if os.path.isfile(_geckodriver):
                driver_ = webdriver.Firefox(_geckodriver)
            else:
                driver_ = webdriver.Firefox()

    def quit(): # Finalização dos testes - Simular ao After ou TearDown
        # sinalização de passou ou falhou conforme o retorno da requisição
        sauce_result = 'failed' if request.node.rep_call.failed else 'passed'
        driver_.execute_script('sauce:job-result={}'.format(sauce_result))
        driver_.quit()

    request.addfinalizer(quit)
    return driver_

@pytest.hookimpl(hookwrapper= True, tryfirst=True) # Implmentação do gatilho de comunicação com SL
def pytest_runtest_makereport(item, call):
    # parametros paa geração do relatório / informações dos resultados
    outcome = yield
    rep = outcome.get_result()

    #definir atribuitos par ao resultado
    setattr(item, 'rep_' + rep.when, rep)