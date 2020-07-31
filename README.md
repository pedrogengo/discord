<h1 align='center'>
    <img src='https://raw.githubusercontent.com/micebot/assets/master/images/logo-256x256.png' height="150">
    <img src='https://raw.githubusercontent.com/micebot/assets/master/images/discord-256x256.png' height="150"><br>
    MiceBot
</h1>
<br>
<div align='center'>
    <a href='https://github.com/psf/black'>
        <img src='https://img.shields.io/badge/code%20style-black-000000.svg'/>
    </a>
    <a href='https://github.com/micebot/discord/issues'>
        <img src='https://badgen.net/github/open-issues/micebot/discord'>
    </a>
    <a href='https://github.com/micebot/discord/commits/development'>
        <img src='https://badgen.net/github/last-commit/micebot/discord/development'>
    </a>
</div>
<br>

Integração com o Discord que permite o gerenciamento de códigos dos produtos
a serem resgatado durante as lives.

## Comandos

### `!mice orders`

Exibe os últimos pedidos entregues, isto é, pode-se visualizar a data da
entrega, o nome do moderador responsável e o nome do usuário que recebeu
a premiação.

*Parâmetros:*
- `limite`: número máximo de itens para exibir. Se nenhum valor for
especificado, por padrão, 5 itens serão exibidos.

*Exemplos de uso:*

`!mice orders`

`!mice orders 2`


### `!mice ls`

Exibe os produtos registrados.

*Parâmetros:*
- `limite`: número máximo de itens para exibir. Se nenhum valor for
especificado, por padrão, 5 itens serão exibidos.

*Exemplos de uso:*

`!mice ls`

`!mice ls 2`


### `!mice add`

Insere um novo produto para ser entregue.

*Parâmetros:*
- `código` **(requerido)**: código que será disponibilizado para o usuário.
- `descrição`: algum valor para identificar o código posteriormente, nos
relatórios. Se nenhum valor for especificado, por padrão será assumido E-Book.

*Restrições:*
- não é possível adicionar um código que já foi inserido anteriormente.

*Exemplos de uso:*

`!mice add 5f3e922a-cef6-4db7-bf40-4d7b9cf66da0`

`!mice add 5f3e922a-cef6-4db7-bf40-4d7b9cf66da0 Kindle`


### `!mice edit`

Permite editar um produto cadastrado anteriormente.

*Parâmetros:*
- `uuid`: **(requerido)**: identificador único do produto.
- `código` **(requerido)**: novo código para ser atribuído ao produto.
- `descrição`: algum valor para identificar o código posteriormente, nos
relatórios. Se nenhum valor for especificado, por padrão será assumido E-Book.

*Restrições:*
- não é possível editar o produto utilizando um código já presente em outro.

*Exemplos de uso:*

`!mice edit uuid_do_produto 5f3e922a-cef6-4db7-bf40-4d7b9cf66da0`

`!mice edit uuid_do_produto 5f3e922a-cef6-4db7-bf40-4d7b9cf66da0 Kindle`


### `!mice remove`

Remove um produto cadastrado para resgate.

*Parâmetros:*
- `uuid`: **(requerido)**: identificador único do produto.

*Restrições:*
- não é possível remover um produto que já foi resgatado.

*Exemplos de uso:*

`!mice remove uuid_do_produto`


-----


## Development status

| Branch | Pipeline | Coverage |
| ------ | ----- | ----- |
| **Development** | [![pipeline status][1]][2] | [![coverage report][3]][4] |
| **Master** | [![pipeline status][5]][6] | [![coverage report][7]][8] |

[1]:https://gitlab.com/micebot/discord-ci/badges/development/pipeline.svg
[2]:https://gitlab.com/micebot/discord-ci/-/pipelines?page=1&scope=all&ref=development
[3]:https://gitlab.com/micebot/discord-ci/badges/development/coverage.svg
[4]:https://gitlab.com/micebot/discord-ci/-/commits/development
[5]:https://gitlab.com/micebot/discord-ci/badges/master/pipeline.svg
[6]:https://gitlab.com/micebot/discord-ci/-/pipelines?page=1&scope=all&ref=master
[7]:https://gitlab.com/micebot/discord-ci/badges/master/coverage.svg
[8]:https://gitlab.com/micebot/discord-ci/-/commits/master
