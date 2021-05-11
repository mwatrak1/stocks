from djongo import models
import yfinance as yf


class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=80)
    phone_number = models.BigIntegerField(primary_key=True)
    
    objects = models.DjongoManager()

    def __hash__(self):
        return hash(self.phone_number)

    def __repr__(self):
        return f'User({self.username}, {self.pk}, {self.email})'

    def to_json(self):
        user_data = {
            "email": self.email,
            "username": self.username
        }
        notifications = Notification.objects.filter(user_id=self)
        user_data['notifications_count'] = len(notifications)
        return user_data

    @classmethod
    def get_users_with_notifications(cls):
        return cls.objects.filter(notifications__isnull=False)


class Notification(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    stock_name = models.CharField(max_length=50)
    stock_abbreviation = models.CharField(max_length=10)
    percentage_change = models.FloatField()
    stock_value = models.FloatField()
    notification_setup_date = models.CharField(max_length=50)

    def __hash__(self):
        return hash(self.stock_abbreviation)

    def check_stock_reached_percentage(self):
        notification_value = self.stock_value * (100 + self.percentage_change) / 100

    def to_dict(self):
        object_dict = self.__dict__
        object_dict.pop('_state')
        return object_dict

    objects = models.DjongoManager()


class Stock(models.Model):
    abbreviation = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    logo_url = models.CharField(max_length=100)
    description = models.CharField(max_length=10000)
    country = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    
    objects = models.DjongoManager()

    def __hash__(self):
        return hash(self.abbreviation)

    @staticmethod
    def add_stock(symbol):
        stock = yf.Ticker(symbol)

        if Stock.check_stock_exists(stock):
            stock_info = stock.get_info()
            Stock.create_new_stock_from_info(stock_info)

    @staticmethod
    def check_stock_exists(stock):
        try:
            stock.get_info()
        except ValueError:
            print("No stock under this symbol")
            return False
        return True

    @staticmethod
    def create_new_stock_from_info(info):
        stock = Stock(
            abbreviation=info.get("symbol"),
            name=info.get("longName"),
            logo_url=info.get("logo_url"),
            description=info.get("longBusinessSummary"),
            country=info.get("country"),
            industry=info.get("industry"),
            sector=info.get("sector")
        )
        if Stock.check_stock_values(stock):
            stock.save()
        else:
            print("There are missing stock attributes! Cannot create a new Stock")

    @staticmethod
    def check_stock_values(stock):
        stock_values = [stock.name, stock.abbreviation, stock.logo_url, stock.description,
                        stock.country, stock.industry, stock.sector]
        truthiness_map = map(lambda x: bool(x) is True, stock_values)
        return all(truthiness_map)
