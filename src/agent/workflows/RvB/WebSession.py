from playwright.sync_api import sync_playwright


class PlaywrightSession:
    def __init__(self):
        self.browser = None
        self.page = None

    def __enter__(self):
        return self
    
    def get_page(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless = True)
        self.page = self.browser.new_page()
        self.page.goto("https://www1.agenziaentrate.gov.it/servizi/Consultazione/ricerca.htm")
        return self.page
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.browser is not None:
            self.browser.close()