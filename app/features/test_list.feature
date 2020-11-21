Feature: aptar requisicao feita no frontend e enviar ao microsservico user atraves do BFF 
  Como Sistema, quero pegar os dados informados no frontend pelo administrador,
  e visualiza-los no meu servico.

  Context: O administrador ver os usuarios cadastrados 
    Dado que os dados que foram resgistrados utilizem o servico atraves do BFF

    Scenario: Administrador visualiza os usuarios cadastrados na aplicacao
        Given a pagina de gerenciar usuarios
        When ele visualizar os usuarios desejados
        Then o bff requisita o microsservico desejado