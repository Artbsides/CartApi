# Cart Api

Serviço disponível para o gerenciamento de dados dos carrinhos de compras em um e-commerce.

# Banco de Dados

Para fins de armazenamento e consulta, o banco de dados utilizado por este serviço é o **MongoDB**. Ao instalar a aplicação, o banco é criado e populado com dados fictícios.

# Postman

Para utilizar os serviços sem a implementação de uma aplicação front-end, é necessário executar as rotas disponíveis via curl ou algum software de terceiros. Uma cópia da collection contendo exemplos de execução para uso no **Postman** pode ser importada através do arquivo ```postman-cart-api-collection.json```.

Para que todas as rotas fundionem corretamente, o serviço responsável pelos dados dos produtos deve estar disponível, como ele ainda não foi desenvolvido, é necessário utilizá-lo de forma mockada através da importação do arquivo ```postman-products-api-collection.json```.

Talvez algumas variáveis precisem ser criadas no Postman para que as requests funcionem como o esperado, são elas:

```
{{cart-api}}

var:   cart-api
value: http://localhost:5000
```

```
{{products-api}}

var:   products-api
value: https://3e50cd27-cf70-4c8b-89fd-869ec742555b.mock.pstmn.io
```

```
{{X-API-KEY}}

var:   X-API-KEY
value: PMAK-6137dfa173453700461a33da-8ecae3393710f0ceaff58d84c120d7cb90
```

# Instalação

É necessário que o ambiente escolhido para instalação possua o **Docker** e todas suas dependências previamente instaladas, uma vez instalado, basta seguir os seguintes passos:

Para instalar a aplicação, basta rodar o comando abaixo.

```
$ make install
```

O comando **make install** é responsável pela execução de todas as pendências do serviço, ao final, testes automatizados serão executados.

Caso seja necessário executar comandos individualmente, basta utilizar o comando ```make <option>```.

Para exibir a lista de comandos disponníveis, basta executar o comando ```make```.

# Inicialização

Para inicializar o serviço, basta executar o comando abaixo.

```
$ make run
```

Ao final da inicialização, o serviço estará disponível no seguinte endereço e porta ```http://localhost:5000```

# Rotas

- POST /v1/cart

Rota disponível para inserir o primeiro produto ao carrinho de compras ainda não existente.

Dados de entrada:

```
{
    "product_uuid": <:string>,
    "price": <:float>,
    "amount": <:int>
}
```

- POST /v1/cart/:cart_id/products

Rota disponível para inserir produtos em um carrinho de compras já existente.

Dados de entrada:

```
{
    "product_uuid": <:string>,
    "price": <:float>,
    "amount": <:int>
}
```

- PATCH /v1/cart/:cart_id/:product_id

Rota disponível para atualizar dados dos produtos inseridos em um carrinho de compras.

Dados de entrada:

```
{
    "price": <:float>,
    "amount": <:int>
}
```

- DELETE /v1/cart/:cart_id/:product_id

Rota disponível para remover produtos inseridos em um carrinho de compras.

- PUT /v1/cart/:cart_id/coupon

Rota disponível para inserir cupom de desconto em um carrinho de compras.

Dados de entrada:

```
{
    "code": <:string>
}
```

- DELETE /v1/cart/:cart_id/coupon

Rota disponível para remover cupom de desconto em um carrinho de compras.

- GET /v1/cart/:cart_id

Rota disponível para exibição do carrinho de compras, detalhes dos produtos inseridos e valores.

- DELETE /v1/cart/:cart_id

Rota disponível para remover carrinhos de compras e todos os seus produtos.

# CI/CD

O repositório desta aplicação foi configurado para que no on-push o workflow [on-push](.github/workflows/on-push.yml) que é responsável por realizar testes e análise de código seja disparado, caso algumas das ações falhe, não será possível realizar o merge da branch do PR com a main.

Para realização de deploy, seja em staging ou production, é necessária a criação de tags para que o workflow [on-push-tags](.github/workflows/on-push-tags.yml) seja disparado, porém é necessário alterar a versão da imagem da aplicação nos arquivos de deploy, tal como descrito logo abaixo.

O deploy em staging é realizado apenas quando a versão da imagem da alicação for alterada no arquivo [.secrets.yml](.k8s/staging/secrets/.secrets.yml) de staging, após a alteração, é necessário gerar uma nova tag da mesma versão a partir da branch do PR.

O deploy em production segue o mesmo principio, sendo assim, antes do merge da branch do PR com a main, certifique-se de alterar a versão da imagem da aplicação no arquivo [.secrets.yml](.k8s/production/secrets/.secrets.yml) de production, feito isso, faça o merge, aguarde os resutados dos testes e crie um `relase` a partir de uma nova tag de acordo com a versão setada previamente.

Para maiores dealhes a respeito das dependências para relazação do depoy ou ainda, como visualizar a aplicação devidamente aplicada, acesse o seguinte [repositório](https://github.com/Artbsides/ArgoCD.Deployment).

# Principais Tecnologias Utilizadas

- [Python](https://www.python.org)
- [MongoDB](https://www.mongodb.com)
- [Docker](https://www.docker.com)
- [Postman](https://www.postman.com)

# Melhorias

- Implementar ErrorHandler para tratamento de erros.
