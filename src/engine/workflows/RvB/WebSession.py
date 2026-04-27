from playwright.sync_api import sync_playwright


class PlaywrightSession:
    def __init__(self):
        self.browser = None
        self.page = None
        self.playwright = None

    def __enter__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True, slow_mo=1500)
        self.page = self.browser.new_page()
        self.page.goto(
            "https://www1.agenziaentrate.gov.it/servizi/Consultazione/ricerca.htm"
        )
        return self.page

    def __exit__(self, exc_type, exc_valeu, exc_traceback):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
