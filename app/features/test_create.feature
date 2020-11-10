Feature: criar requisicao e enviar ao microsservico user atraves do BFF 
  Como Sistema, quero registrar um usuario na aplicacao atraves,
  e armazenar no meu servico.

  Context: O administrador criar os usuarios na aplicacao
    Dado que os dados sejam resgistrados e utilizem o servico atraves do BFF

    Scenario: Administrador cadastra os usuarios na aplicacao
        Given a pagina de criar novo usuario
        When ele regista novo conteúdo da solicitação
        Then o bff requisita o microsservico para criar informacao