import itertools
from bs4 import BeautifulSoup

from cloudomate.gateway import coinbase
from cloudomate.vps.clientarea import ClientArea
from cloudomate.vps.solusvm_hoster import SolusvmHoster
from cloudomate.vps.vpsoption import VpsOption
from cloudomate.wallet import determine_currency


class Cinfu(SolusvmHoster):
    name = "cinfu"
    website = "https://www.cinfu.com/"
    clientarea_url = "https://panel.cinfu.com/clientarea.php"
    required_settings = [
        'firstname',
        'lastname',
        'email',
        'phonenumber',
        'address',
        'city',
        'countrycode',
        'state',
        'zipcode',
        'password',
        'hostname',
        'rootpw'
    ]
    gateway = coinbase

    def __init__(self):
        super(Cinfu, self).__init__()

    def get_status(self, user_settings):
        clientarea = ClientArea(self.br, self.clientarea_url, user_settings)
        clientarea.print_services()

    def set_rootpw(self, user_settings):
        clientarea = ClientArea(self.br, self.clientarea_url, user_settings)
        clientarea.set_rootpw_client_data()

    def get_ip(self, user_settings):
        clientarea = ClientArea(self.br, self.clientarea_url, user_settings)
        return clientarea.get_client_data_ip(self.client_data_url)

    def info(self, user_settings):
        clientarea = ClientArea(self.br, self.clientarea_url, user_settings)
        info_dict = clientarea.get_client_data_info_dict(self.client_data_url)
        self._print_info_dict(info_dict)

    def register(self, user_settings, vps_option):
        self.br.open(vps_option.purchase_url)
        self.server_form(user_settings)
        self.br.open('https://panel.cinfu.com/cart.php?a=view')
        self.br.follow_link(text_regex="Checkout")
        self.br.select_form(nr=4)
        self.user_form(self.br, user_settings, 'bitcoin')
        page = self.br.response()
        print page.geturl
        return self.get_bitcoin_info(page.get_data())

    def get_bitcoin_info(self, br):
        soup = BeautifulSoup(br, 'lxml')
        info = soup.find('div', {'class': 'payment-btn-container'})
        btcinfo = info.find('a').text
        tempamount = btcinfo.split('?')[1]
        tempaddress = btcinfo.split('?')[0]
        amount = tempamount.split('X')[0]
        amount = float(amount.split('=')[1])
        address = tempaddress.split(':')[1]
        return amount, address

    def server_form(self, user_settings):
        """
                Fills in the form containing server configuration
                :param user_settings: settings
                :return: 
                """
        self.select_form_id(self.br, 'frmConfigureProduct')
        self.fill_in_server_form(self.br.form, user_settings, nameservers=False)
        self.br.form['configoption[234]'] = ['1522']  # Ubuntu
        self.br.submit()

    def start(self):
        cinfu_page = self.br.open('https://www.cinfu.com/vps/')
        return self.parse_options(cinfu_page)

    def parse_options(self, page):
        soup = BeautifulSoup(page, 'lxml')
        tables = soup.findAll('table', {'class': 'table1'})
        options = list(self.parse_german_options(tables[0]))
        options = itertools.chain(options, self.parse_bulg_usa_options(tables[1]), self.parse_french_options(tables[2]),
                                  self.parse_bulg_usa_options(tables[3]), self.parse_dutch_options(tables[4]))
        return options

    def parse_dutch_options(self, table):
        info = table.findAll('tr')
        head = True
        j = 1
        names = [""] * 6
        ram = [""] * 6
        storage = [""] * 6
        cpu = [""] * 6
        price = [""] * 6
        link = [""] * 6
        for item in info:
            if head:
                self.fill_array(names, 'th', item, False)
                head = False
            else:
                if j == 1:
                    self.fill_array(ram, 'td', item, False)
                if j == 2:
                    self.fill_array(storage, 'td', item, False)
                if j == 4:
                    self.fill_array(cpu, 'td', item, False)
                if j == 9:
                    self.fill_array(price, 'td', item, False)
                if j == 13:
                    self.fill_array(link, 'td', item, True)
                j = j + 1
        for k in range(6):
            yield self.fill_options(names[k], ram[k], storage[k], cpu[k], price[k], link[k])

    def parse_french_options(self, table):
        info = table.findAll('tr')
        head = True
        j = 1
        names = [""] * 10
        ram = [""] * 10
        storage = [""] * 10
        cpu = [""] * 10
        price = [""] * 10
        link = [""] * 10
        for item in info:
            if head:
                self.fill_array(names, 'th', item, False)
                head = False
            else:
                if j == 1:
                    self.fill_array(ram, 'td', item, False)
                if j == 2:
                    self.fill_array(storage, 'td', item, False)
                if j == 4:
                    self.fill_array(cpu, 'td', item, False)
                if j == 9:
                    self.fill_array(price, 'td', item, False)
                if j == 13:
                    self.fill_array(link, 'td', item, True)
                j = j + 1
        for k in range(10):
            yield self.fill_options(names[k], ram[k], storage[k], cpu[k], price[k], link[k])

    def parse_bulg_usa_options(self, table):
        info = table.findAll('tr')
        head = True
        j = 1
        names = [""] * 8
        ram = [""] * 8
        storage = [""] * 8
        cpu = [""] * 8
        price = [""] * 8
        link = [""] * 8
        for item in info:
            if head:
                self.fill_array(names, 'th', item, False)
                head = False
            else:
                if j == 1:
                    self.fill_array(ram, 'td', item, False)
                if j == 2:
                    self.fill_array(storage, 'td', item, False)
                if j == 4:
                    self.fill_array(cpu, 'td', item, False)
                if j == 9:
                    self.fill_array(price, 'td', item, False)
                if j == 13:
                    self.fill_array(link, 'td', item, True)
                j = j + 1
        for k in range(8):
            yield self.fill_options(names[k], ram[k], storage[k], cpu[k], price[k], link[k])

    def parse_german_options(self, table):
        info = table.findAll('tr')
        head = True
        j = 1
        names = [""] * 8
        ram = [""] * 8
        storage = [""] * 8
        cpu = [""] * 8
        price = [""] * 8
        link = [""] * 8
        for item in info:
            if head:
                self.fill_array(names, 'th', item, False)
                head = False
            else:
                if j == 1:
                    self.fill_array(ram, 'td', item, False)
                if j == 2:
                    self.fill_array(storage, 'td', item, False)
                if j == 4:
                    self.fill_array(cpu, 'td', item, False)
                if j == 8:
                    self.fill_array(price, 'td', item, False)
                if j == 12:
                    self.fill_array(link, 'td', item, True)
                j = j + 1
        for k in range(8):
            yield self.fill_options(names[k], ram[k], storage[k], cpu[k], price[k], link[k])

    @staticmethod
    def fill_options(names, rams, storages, cpus, prices, links):
        return VpsOption(
            name=names,
            price=float(prices.split('$')[1]),
            currency=determine_currency(prices),
            cpu=int(cpus.split("x")[0]),
            ram=float(rams.split("M")[0]) / 1024,
            storage=float(storages.split("G")[0]),
            bandwidth='unmetered',
            connection=100,
            purchase_url=links
        )

    @staticmethod
    def fill_array(array, type, item, link):
        if link:
            temp = item.findAll(type)
            i = 0
            for name in temp[1:]:
                array[i] = name.find('a')['href']
                i = i + 1
        else:
            temp = item.findAll(type)
            i = 0
            for name in temp[1:]:
                if name.find('strong'):
                    ram = name.find('strong')
                    array[i] = ram.text
                else:
                    array[i] = name.text
                i = i + 1
