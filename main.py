from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
import sqlite3


class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        image = Image(source='cbo.png')
        layout.add_widget(image)

        welcome_label = Label(text='Bem-vindo')
        employee_auth_button = Button(text='Autenticação do Funcionário do Call Center')
        employee_auth_button.bind(on_press=self.go_to_employee_auth)
        main_system_button = Button(text='Acesso ao Sistema Principal')
        main_system_button.bind(on_press=self.go_to_main_system)
        layout.add_widget(welcome_label)
        layout.add_widget(employee_auth_button)
        layout.add_widget(main_system_button)
        self.add_widget(layout)

    def go_to_employee_auth(self, instance):
        #Tira o que está no ecrã
        self.clear_widgets()
        
        #Elementos da autenticação do funcionário
        auth_layout = BoxLayout(orientation='vertical')
        username_input = TextInput(hint_text='Nome de usuário')
        password_input = TextInput(hint_text='Senha', password=True)
        confirm_button = Button(text='Confirmar')
        
        def authenticate(instance):
            #verifica usuario e pass
            if username_input.text == 'admin' and password_input.text == '123456':
                #mostra as opçoes
                auth_layout.clear_widgets()
                options_label = Label(text='Selecione uma opção:')
                view_orders_button = Button(text='Ver Pedidos')
                view_customers_button = Button(text='Ver Clientes')
                view_hamburguers_button = Button(text='Ver Hamburguers')

                #açoes dos botoes
                def view_orders(instance):
                    conn = sqlite3.connect('hamburgueria.db')
                    cursor = conn.cursor()
                    cursor.execute('''
                        SELECT p.id, c.nome, p.nome_hamburguer, p.quantidade, p.tamanho, p.valor_total 
                        FROM Pedidos p
                        JOIN Clientes c ON p.id_cliente = c.id
                    ''')
                    orders_data = cursor.fetchall()
                    conn.close()

                    #mostra informaçoes dos pedidos
                    orders_layout = BoxLayout(orientation='vertical')
                    for order in orders_data:
                        order_label = Label(text=f'Pedido ID: {order[0]}, Cliente: {order[1]}, Hambúrguer: {order[2]}, Quantidade: {order[3]}, Tamanho: {order[4]}, Valor: {order[5]}€')
                        orders_layout.add_widget(order_label)

                    self.clear_widgets()
                    self.add_widget(orders_layout)
                
                def view_customers(instance):
                    #mostra os clientes
                    conn = sqlite3.connect('hamburgueria.db')
                    cursor = conn.cursor()
                    cursor.execute('SELECT nome, morada, telefone FROM Clientes')
                    customers_data = cursor.fetchall()
                    conn.close()

                    for customer in customers_data:
                        customer_label = Label(text=f'Nome: {customer[0]}, Morada: {customer[1]}, Telefone: {customer[2]}')
                        instance.parent.add_widget(customer_label)  #adiciona a tela atual

                
                def view_hamburguers(instance):
                    conn = sqlite3.connect('hamburgueria.db')
                    cursor = conn.cursor()
                    cursor.execute('SELECT nome_hamburguer, ingredientes, preco FROM Hamburguers')
                    hamburguers_data = cursor.fetchall()
                    conn.close()

                    hamburguers_layout = BoxLayout(orientation='vertical')
                    for hamburguer in hamburguers_data:
                        hamburguer_label = Label(text=f'Nome: {hamburguer[0]}, Ingredientes: {hamburguer[1]}, Preço: {hamburguer[2]}€')
                        hamburguers_layout.add_widget(hamburguer_label)

                    self.clear_widgets()
                    self.add_widget(hamburguers_layout)
                
                view_orders_button.bind(on_press=view_orders)
                view_customers_button.bind(on_press=view_customers)
                view_hamburguers_button.bind(on_press=view_hamburguers)
                
                #adiciona os elementos na tela
                auth_layout.add_widget(options_label)
                auth_layout.add_widget(view_orders_button)
                auth_layout.add_widget(view_customers_button)
                auth_layout.add_widget(view_hamburguers_button)
            
            else:
                invalid_label = Label(text='Credenciais inválidas. Tente novamente.')
                auth_layout.add_widget(invalid_label)

        #clica para a função authenticate
        confirm_button.bind(on_press=authenticate)
        
        auth_layout.add_widget(username_input)
        auth_layout.add_widget(password_input)
        auth_layout.add_widget(confirm_button)
        self.add_widget(auth_layout)


    def go_to_main_system(self, instance):
        self.manager.current = 'order'

class OrderScreen(Screen):
    def __init__(self, **kwargs):
        super(OrderScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)
        self.populate_hamburguers()

    def populate_hamburguers(self):
        self.layout.clear_widgets()
        hamburguers_label = Label(text='Escolha um Hambúrguer:')
        self.layout.add_widget(hamburguers_label)

        conn = sqlite3.connect('hamburgueria.db')
        cursor = conn.cursor()
        cursor.execute('SELECT nome_hamburguer, preco FROM Hamburguers')
        hamburguers_data = cursor.fetchall()
        conn.close()

        for hamburguer in hamburguers_data:
            hamburguer_button = Button(text=f'{hamburguer[0]} - {hamburguer[1]}€',
                                       size_hint_y=None,
                                       height=40)
            hamburguer_button.bind(on_press=self.select_hamburguer)
            self.layout.add_widget(hamburguer_button)

        review_button = Button(text='Revisar Pedido')
        review_button.bind(on_press=self.review_order)
        self.layout.add_widget(review_button)

    def select_hamburguer(self, instance):
        hamburguer_name = instance.text.split('-')[0].strip()  #amrmazena apenas o nome do hamburguer
        self.manager.current = 'details'
        details_screen = self.manager.get_screen('details')
        details_screen.load_hamburguer_details(hamburguer_name)
        details_screen.previous_screen = self.name  #armazena o nome da tela anterior

    def review_order(self, instance):
        self.manager.current = 'review'

class HamburguerDetailsScreen(Screen):
    def __init__(self, **kwargs):
        super(HamburguerDetailsScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.hamburguer_name_label = Label(text='Nome do Hambúrguer:')
        self.hamburguer_ingredients_label = Label(text='Ingredientes:')
        self.hamburguer_price_label = Label(text='Preço:')
        self.layout.add_widget(self.hamburguer_name_label)
        self.layout.add_widget(self.hamburguer_ingredients_label)
        self.layout.add_widget(self.hamburguer_price_label)

        self.back_button = Button(text='Voltar')
        self.continue_button = Button(text='Continuar')
        self.back_button.bind(on_press=self.go_back)
        self.continue_button.bind(on_press=self.continue_order)
        self.layout.add_widget(self.back_button)
        self.layout.add_widget(self.continue_button)

        self.add_widget(self.layout)

    def load_hamburguer_details(self, hamburguer_name):
        self.hamburguer_name = hamburguer_name
        conn = sqlite3.connect('hamburgueria.db')
        cursor = conn.cursor()
        cursor.execute('SELECT ingredientes, preco FROM Hamburguers WHERE nome_hamburguer=?', (hamburguer_name,))
        hamburguer_data = cursor.fetchone()
        conn.close()

        if hamburguer_data:
            self.hamburguer_name_label.text = f'Nome do Hambúrguer: {hamburguer_name}'
            self.hamburguer_ingredients_label.text = f'Ingredientes: {hamburguer_data[0]}'
            self.hamburguer_price_label.text = f'Preço: {hamburguer_data[1]}€'
            self.hamburguer_price = hamburguer_data[1]  #armazena o preço
        else:
            self.hamburguer_name_label.text = 'Erro ao carregar detalhes do hambúrguer.'

    def go_back(self, instance):
        if hasattr(self, 'previous_screen'):
            self.manager.current = self.previous_screen

    def continue_order(self, instance):
        #selecionamento do tamanho
        self.layout.clear_widgets() 
        type_label = Label(text=f'Tipo de Hambúrguer: {self.hamburguer_name}')
        self.layout.add_widget(type_label)

        size_label = Label(text='Selecione o tamanho do hambúrguer:')
        self.size_spinner = Spinner(text='Escolha o tamanho', values=('infantil', 'normal', 'duplo'))
        size_layout = GridLayout(cols=2)
        size_layout.add_widget(size_label)
        size_layout.add_widget(self.size_spinner)
        self.layout.add_widget(size_layout)

        #quantidade com + e -
        quantity_label = Label(text='Selecione a quantidade:')
        self.quantity_label = Label(text='1')
        plus_button = Button(text='+')
        minus_button = Button(text='-')
        plus_button.bind(on_press=self.increment_quantity)
        minus_button.bind(on_press=self.decrement_quantity)
        quantity_layout = BoxLayout()
        quantity_layout.add_widget(quantity_label)
        quantity_layout.add_widget(minus_button)
        quantity_layout.add_widget(self.quantity_label)
        quantity_layout.add_widget(plus_button)
        self.layout.add_widget(quantity_layout)

        #preço atual
        self.total_price_label = Label(text=f'Preço total: {self.hamburguer_price}€')
        self.layout.add_widget(self.total_price_label)

        confirm_button = Button(text='Confirmar')
        confirm_button.bind(on_press=self.confirm_order)
        self.layout.add_widget(confirm_button)

    def increment_quantity(self, instance):
        quantity = int(self.quantity_label.text)
        quantity += 1
        self.quantity_label.text = str(quantity)
        self.update_total_price()

    def decrement_quantity(self, instance):
        quantity = int(self.quantity_label.text)
        if quantity > 1:
            quantity -= 1
            self.quantity_label.text = str(quantity)
            self.update_total_price()

    def update_total_price(self):
        quantity = int(self.quantity_label.text)
        total_price = self.hamburguer_price * quantity
        self.total_price_label.text = f'Preço total: {total_price}€'

    def confirm_order(self, instance):
        selected_size = self.size_spinner.text  #obtém o tamanho selcionado do spinner
        quantity = int(self.quantity_label.text)
        total_price = self.hamburguer_price * quantity
        order_screen = self.manager.get_screen('order')
        order_screen.layout.add_widget(Button(text=f'{self.hamburguer_name} - {selected_size} x{quantity} - {total_price}€'))
        review_screen = self.manager.get_screen('review')
        review_screen.add_order(f'{self.hamburguer_name} - {selected_size} x{quantity} - {total_price}€', total_price)
        self.manager.current = 'order'


class ReviewOrderScreen(Screen):
    def __init__(self, **kwargs):
        super(ReviewOrderScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.orders_label = Label(text='Seu Pedido:')
        self.total_price_label = Label(text='Preço total do pedido: 0€')
        self.layout.add_widget(self.orders_label)
        self.layout.add_widget(self.total_price_label)
        self.add_widget(self.layout)
        self.orders = []
        self.total_price = 0

        # informaçoes cliente
        self.name_input = TextInput(hint_text='Nome')
        self.address_input = TextInput(hint_text='Morada')
        self.phone_input = TextInput(hint_text='Telemóvel')
        self.layout.add_widget(self.name_input)
        self.layout.add_widget(self.address_input)
        self.layout.add_widget(self.phone_input)

        self.buttons_layout = BoxLayout(size_hint_y=None, height=50)
        self.confirm_button = Button(text='Confirmar Pedido')
        self.back_button = Button(text='Voltar')
        self.confirm_button.bind(on_press=self.confirm_order)
        self.back_button.bind(on_press=self.go_back)
        self.buttons_layout.add_widget(self.back_button)
        self.buttons_layout.add_widget(self.confirm_button)
        self.layout.add_widget(self.buttons_layout)

    def add_order(self, order_text, price):
        self.orders.append(order_text)
        self.total_price += price
        self.orders_label.text += f'\n{order_text}'
        self.total_price_label.text = f'Preço total do pedido: {self.total_price}€'

    def confirm_order(self, instance):
    #obtem dados clientes
        name = self.name_input.text
        address = self.address_input.text
        phone = self.phone_input.text

        # Conectar e salva o pedido ao banco de dados
        conn = sqlite3.connect('hamburgueria.db')
        cursor = conn.cursor()

        #insere dados de cliente
        cursor.execute('INSERT INTO Clientes (nome, morada, telefone) VALUES (?, ?, ?)', (name, address, phone))
        cliente_id = cursor.lastrowid  #obtem o id recem inserido
        print(f"Cliente registrado com ID {cliente_id}")

        #dados dos pedidos
        for order in self.orders:
            nome_hamburguer = order.split(' - ')[0]
            quantidade = int(order.split(' x')[1].split(' - ')[0])
            tamanho = order.split(' - ')[1].lower()
            valor_str = order.split(' - ')[2][:-1]
            valor_float = float(valor_str)

            #verifica se tamnhao valido
            if tamanho not in ('infantil', 'normal', 'duplo'):
                print(f"Tamanho de hambúrguer inválido: {tamanho}. Pedido não foi registrado.")
                continue

            #insere dados pedidos ##erro
            cursor.execute('INSERT INTO Pedidos (id_cliente, nome_hamburguer, quantidade, tamanho, valor_total) VALUES (?, ?, ?, ?, ?)',
                        (cliente_id, nome_hamburguer, quantidade, tamanho, valor_float))
            pedido_id = cursor.lastrowid  #obtem o id recem inserido
            print(f"Pedido registrado com ID {pedido_id} para o cliente {cliente_id}")

        conn.commit()
        conn.close()


        #limpa o pedido apos confirmaçao
        self.orders.clear()
        self.total_price = 0
        self.orders_label.text = 'Seu Pedido:'
        self.total_price_label.text = 'Preço total do pedido: 0€'
        self.name_input.text = ''
        self.address_input.text = ''
        self.phone_input.text = ''

        self.manager.current = 'welcome'

    def go_back(self, instance):
        self.manager.current = 'order'


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(OrderScreen(name='order'))
        sm.add_widget(HamburguerDetailsScreen(name='details'))
        sm.add_widget(ReviewOrderScreen(name='review'))
        return sm
    
    
if __name__ == '__main__':
    MyApp().run()
