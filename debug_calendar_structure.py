# debug_calendar_structure.py
from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()
    
    print("🚀 Opening Kiwi.com...")
    page.goto("https://www.kiwi.com/en/")
    time.sleep(3)
    
    # Accept cookies
    try:
        page.click("button:has-text('Accept')")
        time.sleep(1)
    except:
        pass
    
    # Fill fields
    print("\n📍 Filling departure...")
    page.click("[data-test='SearchField-input']:first-of-type")
    time.sleep(1)
    page.keyboard.type("RTM")
    time.sleep(2)
    page.keyboard.press("Enter")
    time.sleep(2)
    
    print("📍 Filling arrival...")
    page.click("[data-test='PlacePickerInput-destination'] [data-test='SearchField-input']")
    time.sleep(1)
    page.keyboard.type("MAD")
    time.sleep(2)
    page.keyboard.press("Enter")
    time.sleep(2)
    
    # Close dropdowns
    page.keyboard.press("Escape")
    time.sleep(1)
    
    # Open date picker
    print("\n📅 Opening date picker...")
    page.click("[data-test='SearchDateInput']")
    time.sleep(2)
    
    # Calculate target date (1 week from now)
    target_date = datetime.now() + timedelta(weeks=1)
    day = target_date.day
    month = target_date.strftime("%B")
    date_string = target_date.strftime("%Y-%m-%d")
    
    print(f"\n🎯 Looking for date: {day} {month} (date-string: {date_string})")
    print("="*60)
    
    # Check different selectors
    selectors_to_try = [
        f"div[data-date='{date_string}']",
        f"button:has-text('{day}')",
        f"div[aria-label*='{month} {day}']",
        "div[class*='Day']",
        "button[class*='Day']",
        "div[role='button']"
    ]
    
    for selector in selectors_to_try:
        try:
            elements = page.locator(selector).all()
            print(f"\n✓ Selector: {selector}")
            print(f"  Found: {len(elements)} elements")
            
            if len(elements) > 0:
                # Show details of first few elements
                for i, elem in enumerate(elements[:3]):
                    try:
                        text = elem.inner_text() if elem.is_visible() else "[not visible]"
                        classes = elem.get_attribute("class")
                        data_date = elem.get_attribute("data-date")
                        aria_label = elem.get_attribute("aria-label")
                        
                        print(f"\n  Element {i}:")
                        print(f"    Text: {text}")
                        print(f"    Classes: {classes}")
                        print(f"    data-date: {data_date}")
                        print(f"    aria-label: {aria_label}")
                    except Exception as e:
                        print(f"    Error: {e}")
        except Exception as e:
            print(f"\n✗ Selector failed: {selector}")
            print(f"  Error: {e}")
    
    print("\n" + "="*60)
    print("📸 Calendar is open. Check the browser manually.")
    print("Press Enter to try clicking the date...")
    input()
    
    # Try to click the date
    print(f"\n🖱️  Attempting to click date {day}...")
    
    # Try the most promising selector
    try:
        # Method 1: data-date
        elem = page.locator(f"div[data-date='{date_string}']").first
        if elem.is_visible():
            elem.click()
            print("✓ Clicked using data-date!")
            time.sleep(2)
    except Exception as e:
        print(f"data-date click failed: {e}")
        
        # Method 2: Find by text
        try:
            buttons = page.locator(f"button:has-text('{day}')").all()
            print(f"Found {len(buttons)} buttons with text '{day}'")
            
            for btn in buttons:
                if btn.is_visible():
                    btn.click()
                    print(f"✓ Clicked button with text '{day}'")
                    time.sleep(2)
                    break
        except Exception as e2:
            print(f"Text click failed: {e2}")
    
    print("\n✅ Done. Browser stays open for inspection.")
    input("Press Enter to close...")
    browser.close()