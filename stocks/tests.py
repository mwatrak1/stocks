from unittest import TestCase
from .models import User, Notification, Stock
import yfinance as yf
from bokeh.plotting import figure
from bokeh.embed import json_item
import json


# Create your tests here.
class UserModelTest(TestCase):
    def setUp(self) -> None:
        self.user = User(username="John", email="john@gmail.com", password="dog123")

    def test_user(self):
        self.assertEqual(self.user.username, "John")
        self.assertEqual(self.user.email, 'john@gmail.com')


class NotificationModelTest(TestCase):
    pass


class StockModelTest(TestCase):
    def setUp(self) -> None:
        info = yf.Ticker("AAPL").get_info()
        self.stock = Stock(
            abbreviation=info.get("symbol"),
            name=info.get("longName"),
            logo_url=info.get("logo_url"),
            description=info.get("longBusinessSummary"),
            country=info.get("country"),
            industry=info.get("industry"),
            sector=info.get("sector")
        )
        print(vars(self.stock))

    def test_all_fields_nonempty(self):
        self.assertTrue(self.stock.name)
        self.assertTrue(self.stock.abbreviation)
        self.assertTrue(self.stock.description)
        self.assertTrue(self.stock.country)
        self.assertTrue(self.stock.industry)
        self.assertTrue(self.stock.sector)
        self.assertTrue(self.stock.logo_url)


class GraphCreationTest(TestCase):
    def setUp(self) -> None:
        self.stock_names = ["AAPL", "XPEV", "MSFT"]

    def test_create_graph(self):
        for stock in self.stock_names:
            stock_data_history = yf.download(stock, period="ytd", interval="15m")
            x = stock_data_history.get('High').keys()
            y = stock_data_history.get('High').values
            self.assertTrue(len(x) > 0)
            self.assertTrue(len(y) > 0)

            graph = figure()
            graph.line(x, y)

            html_graph = json.dumps(json_item(graph))
            self.assertIsInstance(html_graph, str)
            self.assertIsNotNone(html_graph)
            self.assertIn(html_graph, stock)
