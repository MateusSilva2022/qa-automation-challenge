from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SortablePage:
    URL = "https://demoqa.com/sortable"
    TIMEOUT = 40  

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.TIMEOUT)

   
    def open(self):
        self.driver.get(self.URL)
        self._hide_ads()
        self._ensure_list_tab()

    def _hide_ads(self):
        self.driver.execute_script("""
            for (let id of ['fixedban','adplus-anchor']) { const el = document.getElementById(id); if (el) el.remove(); }
            const foot = document.querySelector('footer'); if (foot) foot.remove();
        """)

    def _ensure_list_tab(self):
        try:
            list_tab = self.driver.find_element(By.ID, "demo-tab-list")
            if "active" not in list_tab.get_attribute("class"):
                list_tab.click()
        except Exception:
            pass

  
    def _items(self):
        self.wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "#demo-tabpane-list .list-group-item")
        ))
        return self.driver.find_elements(By.CSS_SELECTOR, "#demo-tabpane-list .list-group-item")

    def get_order(self):
        return [e.text.strip() for e in self._items()]

    def _scroll_into_view(self, el):
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)

    def move_item_to_index(self, text, index):
        """
        Move 'text' até a posição 'index' (0-based), trocando com o vizinho
        a cada passo. Isso evita offsets frágeis.
        """
        actions = ActionChains(self.driver)

        for _ in range(30): 
            order = self.get_order()
            cur_idx = order.index(text)
            if cur_idx == index:
                return

            items = self._items()  
            src = items[cur_idx]
            self._scroll_into_view(src)

            if cur_idx > index:
                dst = items[cur_idx - 1]
                actions.move_to_element(src).click_and_hold(src).pause(0.1) \
                       .move_to_element(dst).pause(0.1).move_by_offset(0, -10) \
                       .release().perform()
            else:
                dst = items[cur_idx + 1]
                actions.move_to_element(src).click_and_hold(src).pause(0.1) \
                       .move_to_element(dst).pause(0.1).move_by_offset(0, 10) \
                       .release().perform()

            self.wait.until(lambda d: self.get_order() != order)

        raise AssertionError(f"Não consegui posicionar '{text}' no índice {index}")

    def sort_ascending(self):
        """Ordena para: One, Two, Three, Four, Five, Six."""
        alvo = ["One", "Two", "Three", "Four", "Five", "Six"]
        for i, label in enumerate(alvo):
            self.move_item_to_index(label, i)
        return self.get_order()
