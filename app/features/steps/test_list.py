from behave import given, when, then
import requests

api_url = None
bff_url = None


@given('a pagina de gerenciar usuarios')
def step_impl_given(context):
    global api_url
    api_url = 'https://smartvit-user-dev.herokuapp.com/user'
    print('url :'+api_url)


@when('ele visualizar os usuarios desejados')
def step_impl_when(context):
    response = requests.get('https://smartvit-user-dev.herokuapp.com/user')
    assert response.status_code == 200


@then('o bff requisita o microsservico desejado')
def step_impl_then(context):
    global bff_url
    bff_url = 'https://smartvit-admin-bff-dev.herokuapp.com/user/'
    response = requests.get(bff_url)
    assert response.status_code == 200
