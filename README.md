# API com Web Scraper

Python project of an API that manages a small Database with users information and a web scraping application that will access the API and get the data.
(PT-BR)
Projeto Python de uma API que gerencia um pequeno banco de dados com informações de usuários e um Web Scraper que extrai os dados da API.

### Feito com

[![Python](https://img.shields.io/badge/Python-000?style=for-the-badge&logo=python)](https://docs.python.org/3/)
[![FastAPI](https://img.shields.io/badge/FastAPI-000?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)

### Instalação

 - `pip install -r requirements.txt`

* O arquivo `requirements.txt` vem no repositório e vai instalar todas as dependências da aplicação.

### Como usar

(PT-BR)
* Para ativar a API e iniciar o programa, abra o terminal e use o comando

  - `uvicorn api_app:app --reload` .

* Próximo passo é rodar o Web Scraper, usando o comando

  - `python3 get_from_api.py`

#### Acessando a API fora do Web Scraper:

* Após rodar o comando inicial, a URL a ser utilizada nos _requests_ será `http://127.0.0.1:8000`. A API aceita _requests_ no método _POST_ e _GET_ e os valores devem ser passados em uma variável json. Use método _GET_ para buscar as informações de usuários e o _POST_ para inserir informações no banco de dados, por exemplo:

* Inserindo dados no banco de dados:
  - `resp = post("http://127.0.0.1:8000/novo", json={"nome": 'nome_usuario', "nascimento": "dd/mm/aaaa", "cpf": "xxxxxxxxxxx", "genero": "F"})`

* Buscando informações dos usuários cadastrados no banco de dados (sendo _id_ a PK do usuário):
  - `resp = get("http://127.0.0.1:8000/usuario/id")`

* Os tipos de dados aceitos:

  - `"nome"` deve ser _string_
  - `"nascimento"` é a data de nascimento e deve ser uma _string_ no formato `dd/mm/aaaa`
  - `"cpf"` deve ser uma _string_ com apenas os digitos.
  - `"genero"` deve conter apenas 1 _char_ que pode ser: `"F"` - feminino, `"M"` - masculino ou `"N"` - não-binário/outros.

* Buscando dados sobre o banco de dados e seus usuários:
  - `resp = get("http://127.0.0.1:8000/dados")`
  - retornam da seguinte maneira:
  ```python
  {
   "total_usuarios": _string_ com o total de usuários,
   "media_idade": _string_ com a média de idade dos usuários cadastrados,
   "mulheres":_string_ com informação do total de usuários que se identificam como mulheres,
   "homens": _string_ com informação do total de usuários que se identificam como homens,
   "nao-binarios_outros": _string_ com informação do total de usuários que se identificam desse modo,
  }
  ```
* Os dados retornados podem ser extraídos usando a biblioteca `json`.

### Documentação

- `http://127.0.0.1:8000/docs`
