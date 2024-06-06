# TP10
 
O aplicativo de Hamburgueria foi desenvolvida em Python utilizando o Kivy, com o objetivo de criar uma interface gráfica para a gestão de pedidos de uma hamburgueria com a inspiração do McDonalds, tanto para os clientes como para os funcionários do call center. 

A aplicação permite aos clientes fazer pedidos de hambúrgueres e aos funcionários visualizar os pedidos, clientes e detalhes dos hambúrgueres que o mesmo vende.

Para os clientes, a aplicação oferece a possibilidade de escolher entre 7 hambúrgueres, com os ingredientes bem especificados, onde depois podem escolher entre opções de tamanho e quantidade. Após a escolha do hambúrguer, é possível visualizar os detalhes do mesmo, como ingredientes e preço em euros.
Um cliente pode escolher vários hamburgueres, e pode revisar todas as escolhas feitas e inserir as suas informações pessoais, como nome, morada e telefone, para concluir o pedido.

Os funcionários do call center têm acesso a uma área restrita mediante autenticação, com o usuário e senha. 
Após a autenticação, os funcionários podem visualizar todos os pedidos realizados, consultar informações dos clientes e verificar os detalhes dos hambúrgueres disponíveis na Hamburgueria.

A estrutura do projeto inclui um banco de dados SQLite (hamburgueria.db) que armazena informações sobre clientes, pedidos e hambúrgueres, o código da aplicação (main.py), um código do flask (app.py) e um arquivo README.md com a descrição do projeto e instruções de utilização. 

Para utilizar a aplicação, é necessário ter Python 3.11 e Kivy instalados. 
Após clonar o repositório e instalar as dependências, deve-se criar o banco de dados e as tabelas necessárias com os comandos SQL fornecidos.

Na tela inicial da aplicação, há opções para autenticação do funcionário do call center e para acesso ao sistema principal pelos clientes. Onde funcionários podem autenticar-se e clientes podem navegar pelo sistema, escolher hambúrgueres, ajustar quantidade e tamanho, revisar o pedido, inserir suas informações pessoais e confirmar o pedido.

O aplicativo de Hamburgueria, facilita a gestão de pedidos e clientes, oferecendo uma solução fácil de usar tanto para clientes como para funcionários do call center.