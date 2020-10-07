def validate_fields(request):
    fields = ['name', 'cpf', 'email', 'password', 'type', 'situation']
    return all(field in request.keys() for field in fields)


def validate_name(request):
    return request["name"]


def validate_cpf(request):
    return request["cpf"]


def validate_email(request):
    return request["email"]


def validate_password(request):
    return request["password"]


def validate_type(request):
    return request["type"]


def validate_situation(request):
    return request["situation"]
