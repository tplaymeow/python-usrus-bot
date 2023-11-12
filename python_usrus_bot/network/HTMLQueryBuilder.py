from selenium.webdriver.common.by import By


class HTMLQueryBuilder:
    webDriver = None
    query = None

    def __init__(self, webDriver):
        self.webDriver = webDriver

    def filterID(self, id: str):
        if self.query is None:
            self.query = self.webDriver.find_elements(By.ID, id)
        else:
            self.query = list(filter(lambda x: id in x.get_attribute("id"), self.query))

    def filterClass(self, class_name: str):
        if self.query is None:
            self.query = self.webDriver.find_elements(By.CLASS_NAME, class_name)
        else:
            self.query = list(filter(lambda x: class_name in x.get_attribute("class"), self.query))

    def build(self):
        if self.query is not None:
            return self.query
        else:
            return self.webDriver.find_element(By.XPATH, "//*")
