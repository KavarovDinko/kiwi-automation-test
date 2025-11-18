"""
Enhanced debug script to find exact date selectors
"""
from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
import time

def find_date_selectors():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
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
        print("STEP 1: Open Date Picker")
        print("="*60)
        
        # Click date field
        date_field = page.locator("[data-test='SearchDateInput']").first
        print(f"✓ Found date field, clicking...")
        date_field.click()
        time.sleep(2)
        
        print("\n" + "="*60)
        print("STEP 2: Find Day Cells")
        print("="*60)
        
        # Calculate target date (1 week from now)
        target_date = datetime.now() + timedelta(weeks=1)
        target_day = str(target_date.day)
        date_string = target_date.strftime("%Y-%m-%d")
        
        print(f"Looking for: {target_date.strftime('%B %d, %Y')} ({date_string})")
        print(f"Target day: {target_day}")
        
        # Strategy 1: data-date attribute
        print("\n📅 Strategy 1: data-date attribute")
        selector1 = f"div[data-date='{date_string}']"
        try:
            elements = page.locator(selector1).all()
            print(f"   Found {len(elements)} elements with: {selector1}")
            if len(elements) > 0:
                print(f"   ✓ Can use this selector!")
                elem = elements[0]
                print(f"   Class: {elem.get_attribute('class')}")
                print(f"   Text: {elem.inner_text()}")
        except Exception as e:
            print(f"   ✗ Failed: {e}")
        
        # Strategy 2: Look for all divs in calendar with data-date
        print("\n📅 Strategy 2: All data-date elements")
        try:
            all_dates = page.locator("div[data-date]").all()
            print(f"   Found {len(all_dates)} total date elements")
            print(f"   First 5 dates:")
            for elem in all_dates[:5]:
                date_val = elem.get_attribute('data-date')
                text = elem.inner_text()
                print(f"      - data-date='{date_val}', text='{text}'")
        except Exception as e:
            print(f"   ✗ Failed: {e}")
        
        # Strategy 3: Click by text content
        print("\n📅 Strategy 3: Text content matching")
        try:
            # Find all calendar day elements
            day_elements = page.locator("[data-test*='Calendar'] div").all()
            print(f"   Scanning {len(day_elements)} calendar elements...")
            
            matches = []
            for elem in day_elements:
                try:
                    text = elem.inner_text().strip()
                    if text == target_day:
                        matches.append(elem)
                        elem_class = elem.get_attribute('class')
                        print(f"   Found match: text='{text}', class='{elem_class[:50]}...'")
                except:
                    continue
            
            print(f"   ✓ Found {len(matches)} elements with day '{target_day}'")
            
        except Exception as e:
            print(f"   ✗ Failed: {e}")
        
        # Strategy 4: Use XPath
        print("\n📅 Strategy 4: XPath")
        try:
            xpath = f"//div[@data-date='{date_string}']"
            elements = page.locator(f"xpath={xpath}").all()
            print(f"   Found {len(elements)} elements with XPath")
            if len(elements) > 0:
                print(f"   ✓ XPath works!")
        except Exception as e:
            print(f"   ✗ Failed: {e}")
        
        print("\n" + "="*60)
        print("STEP 3: Test Accommodation Checkbox")
        print("="*60)
        
        # Close calendar first
        page.keyboard.press("Escape")
        time.sleep(1)
        
        checkbox_selector = "[data-test='accommodationCheckbox']"
        try:
            checkbox = page.locator(checkbox_selector).first
            if checkbox.is_visible():
                is_checked = checkbox.is_checked()
                print(f"✓ Checkbox found!")
                print(f"   Selector: {checkbox_selector}")
                print(f"   Is checked: {is_checked}")
                print(f"   Type: {checkbox.get_attribute('type')}")
                print(f"   Name: {checkbox.get_attribute('name')}")
                
                if is_checked:
                    print(f"\n   Testing uncheck...")
                    checkbox.uncheck()
                    time.sleep(1)
                    print(f"   ✓ Unchecked! New state: {checkbox.is_checked()}")
        except Exception as e:
            print(f"✗ Checkbox error: {e}")
        
        print("\n✅ Analysis complete!")
        print("\nBrowser will stay open. Inspect elements manually if needed.")
        input("Press Enter to close...")
        
        browser.close()

if __name__ == "__main__":
    find_date_selectors()