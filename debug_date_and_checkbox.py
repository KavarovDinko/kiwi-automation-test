"""
Debug script to find date picker and checkbox selectors
"""
from playwright.sync_api import sync_playwright
import time

def debug_selectors():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()
        
        print("🚀 Opening Kiwi.com...")
        page.goto("https://www.kiwi.com/en/")
        page.wait_for_load_state("domcontentloaded")
        time.sleep(3)
        
        # Handle cookies
        try:
            cookie_btn = page.locator("button:has-text('Accept')").first
            if cookie_btn.is_visible(timeout=3000):
                cookie_btn.click()
                time.sleep(1)
        except:
            pass
        
        print("\n" + "="*60)
        print("DATE PICKER DEBUG")
        print("="*60)
        
        # Find date field
        date_selectors = [
            "[data-test='SearchDateInput']",
            "[data-test='SearchFieldDateInput']",
            "div[data-test*='Date']"
        ]
        
        print("\n1️⃣ Looking for date field...")
        for selector in date_selectors:
            try:
                element = page.locator(selector).first
                if element.is_visible(timeout=1000):
                    print(f"✓ Found date field: {selector}")
                    print(f"   HTML: {element.get_attribute('outerHTML')[:100]}...")
            except:
                print(f"✗ Not found: {selector}")
        
        print("\n2️⃣ Click date field manually and press Enter when calendar is open...")
        input()
        
        # Check calendar structure
        print("\n3️⃣ Analyzing calendar structure...")
        
        # Look for calendar container
        calendar_containers = [
            "div[class*='Calendar']",
            "div[data-test*='Calendar']",
            "div[class*='DatePicker']"
        ]
        
        for selector in calendar_containers:
            try:
                elements = page.locator(selector).all()
                if len(elements) > 0:
                    print(f"✓ Found {len(elements)} calendar elements: {selector}")
                    # Get classes
                    for i, elem in enumerate(elements[:2]):  # First 2 only
                        print(f"   Element {i}: class='{elem.get_attribute('class')}'")
            except Exception as e:
                print(f"✗ {selector}: {e}")
        
        # Look for day cells
        print("\n4️⃣ Looking for day cells...")
        day_selectors = [
            "div[class*='Day']",
            "button[class*='Day']",
            "div[data-date]",
            "td[class*='Day']"
        ]
        
        for selector in day_selectors:
            try:
                elements = page.locator(selector).all()
                if len(elements) > 0:
                    print(f"✓ Found {len(elements)} day cells: {selector}")
                    # Show first few
                    for i, elem in enumerate(elements[:3]):
                        text = elem.inner_text()
                        data_date = elem.get_attribute('data-date')
                        print(f"   Cell {i}: text='{text}', data-date='{data_date}'")
            except Exception as e:
                print(f"✗ {selector}: {e}")
        
        print("\n" + "="*60)
        print("ACCOMMODATION CHECKBOX DEBUG")
        print("="*60)
        
        # Find accommodation checkbox
        print("\n5️⃣ Looking for accommodation checkbox...")
        checkbox_selectors = [
            "[data-test='accommodationCheckbox']",
            "[data-test*='ccommodation']",
            "input[type='checkbox']",
            "label:has-text('accommodation')"
        ]
        
        for selector in checkbox_selectors:
            try:
                elements = page.locator(selector).all()
                if len(elements) > 0:
                    print(f"✓ Found {len(elements)} elements: {selector}")
                    for i, elem in enumerate(elements[:2]):
                        is_visible = elem.is_visible()
                        print(f"   Element {i}: visible={is_visible}")
                        if elem.get_attribute('type') == 'checkbox':
                            is_checked = elem.is_checked()
                            print(f"              checked={is_checked}")
                        html = elem.get_attribute('outerHTML')
                        print(f"              HTML: {html[:150]}...")
            except Exception as e:
                print(f"✗ {selector}: {e}")
        
        print("\n✅ Debugging complete. Browser will stay open for manual inspection.")
        print("Press Enter to close...")
        input()
        
        browser.close()

if __name__ == "__main__":
    debug_selectors()