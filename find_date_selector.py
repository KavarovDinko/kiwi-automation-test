# find_date_selector.py
from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=800)
    page = browser.new_page()
    
    page.goto("https://www.kiwi.com/en/")
    time.sleep(3)
    
    # Accept cookies
    try:
        page.click("button:has-text('Accept')", timeout=3000)
        time.sleep(1)
    except:
        pass
    
    # Fill departure
    page.click("[data-test='SearchField-input']:first-of-type")
    time.sleep(1)
    page.type("[data-test='SearchField-input']:first-of-type", "RTM")
    time.sleep(2)
    page.keyboard.press("Enter")
    time.sleep(2)
    
    # Fill arrival
    page.click("[data-test='PlacePickerInput-destination'] [data-test='SearchField-input']")
    time.sleep(1)
    page.type("[data-test='PlacePickerInput-destination'] [data-test='SearchField-input']", "MAD")
    time.sleep(2)
    page.keyboard.press("Enter")
    time.sleep(2)
    
    # Close dropdowns
    page.keyboard.press("Escape")
    time.sleep(1)
    
    # Open calendar
    print("Opening calendar...")
    page.click("[data-test='SearchDateInput']")
    time.sleep(3)
    
    # Calculate target date
    target = datetime.now() + timedelta(weeks=1)
    day = target.day
    
    print(f"\nLooking for day: {day}")
    print("="*60)
    
    # NOW - Open browser console and paste this to find what works:
    print("\n📋 MANUAL CHECK:")
    print("1. Look at the calendar")
    print(f"2. Find the date cell for day {day}")
    print("3. Right-click it → Inspect")
    print("4. Tell me the HTML structure you see")
    print("\nPress Enter after you've inspected...")
    input()
    
    # Let's try clicking all visible buttons/divs with the day number
    print(f"\nTrying to find clickable element with text '{day}'...")
    
    # Get ALL elements that contain the day number
    all_elements = page.locator(f"*:has-text('{day}')").all()
    print(f"Found {len(all_elements)} elements containing '{day}'")
    
    # Filter for small, clickable ones (likely date cells)
    for i, elem in enumerate(all_elements):
        try:
            text = elem.inner_text().strip()
            tag = elem.evaluate("el => el.tagName")
            classes = elem.get_attribute("class") or ""
            
            # Date cells are usually small, just the number
            if text == str(day):
                print(f"\nCandidate {i}:")
                print(f"  Tag: {tag}")
                print(f"  Text: {text}")
                print(f"  Classes: {classes[:100]}")
                print(f"  Visible: {elem.is_visible()}")
                
                # Try to click it
                if elem.is_visible() and "disabled" not in classes.lower():
                    print(f"  → Attempting click...")
                    elem.click()
                    print(f"  ✅ CLICKED!")
                    time.sleep(2)
                    break
        except Exception as e:
            continue
    
    print("\nCheck if date was selected. Press Enter to continue...")
    input()
    
    # Try to click Set dates
    try:
        page.click("[data-test='SearchFormDoneButton']")
        print("✅ Clicked Set dates button")
        time.sleep(2)
    except Exception as e:
        print(f"❌ Set dates button failed: {e}")
    
    print("\n✅ Check the results. Press Enter to close...")
    input()
    browser.close()