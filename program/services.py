from .browsers import BrowserTradeLock


class TradeLockService:

    def __init__(self, user, password):
        self.browser = BrowserTradeLock()
        self.browser.login(user, password)

    def get_item_data(self, item_name: str) -> dict:
        self.browser.make_search(item_name)
        self.browser.choose_item()
        count = self.browser.get_count()
        price = self.browser.get_price()
        return {'count': count, 'price': price}

    def quit(self):
        self.browser.quit()
