from behave import given, when, then
import requests

request_headers = {}
request_bodies = {}
api_url = None


@given('a pagina de criar novo usuario')
def step_impl_given(context):
    global api_url
    api_url = 'https://smartvit-user-dev.herokuapp.com/user'
    print('url :'+api_url)


@when('ele regista novo conteúdo da solicitação')
def step_impl_when(context):
    request_bodies['POST'] = {"name": "Joao Ninguem",
                              "cpf": "3654128900",
                              "email": "teste@gmail.com",
                              "password": "30061998",
                              "type": "Agricultor",
                              "situation": "Ativo"}
    response = requests.post(
                            'https://smartvit-user-dev.herokuapp.com/user',
                            json=request_bodies['POST']
                            )
    assert response.status_code == 200


@then('o bff requisita o microsservico para criar informacao')
def step_impl_then(context):
    api_bff_url = 'https://smartvit-admin-bff-dev.herokuapp.com/user/'
    response = requests.post(
                            api_bff_url,
                            json=request_bodies['POST']
                            )
    assert response.status_code == 200
