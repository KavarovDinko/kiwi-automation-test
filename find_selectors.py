"""
Helper script to manually discover correct selectors on Kiwi.com
Run this to find the right selectors for your test
"""
from playwright.sync_api import sync_playwright
import time

def find_selectors():
    """Interactive script to find selectors"""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()
        
        print("🚀 Opening Kiwi.com...")
        page.goto("https://www.kiwi.com/en/")
        page.wait_for_load_state("domcontentloaded")
        time.sleep(3)
        
        # Handle cookies
        print("\n1️⃣  Checking for cookie popup...")
        try:
            cookie_btn = page.locator("button:has-text('Accept')").first
            if cookie_btn.is_visible(timeout=3000):
                cookie_btn.click()
                print("✓ Cookie accepted")
                time.sleep(1)
        except:
            print("ℹ️  No cookie popup")
        
        # Find one-way button
        print("\n2️⃣  Looking for One-way button...")
        input("Press Enter after you manually click 'One-way' button...")
        
        # Find departure field
        print("\n3️⃣  Looking for departure (From) field...")
        departure_selectors = [
            "[data-test*='origin']",
            "input[placeholder*='From']",
            "[data-test='SearchField-input']:first-of-type"
        ]
        
        for selector in departure_selectors:
            try:
                element = page.locator(selector).first
                if element.is_visible(timeout=2000):
                    print(f"✓ Found departure field: {selector}")
                    element.click()
                    time.sleep(1)
                    element.type("RTM", delay=100)
                    print(f"✓ Typed RTM")
                    time.sleep(2)
                    
                    # Try to click suggestion
                    try:
                        suggestion = page.locator("[data-test='PlacePickerRow']:has-text('RTM')").first
                        if suggestion.is_visible(timeout=2000):
                            suggestion.click()
                            print("✓ Selected from dropdown")
                    except:
                        page.keyboard.press("Enter")
                        print("✓ Pressed Enter")
                    
                    break
            except Exception as e:
                print(f"✗ {selector} failed: {e}")
        
        time.sleep(2)
        
        # Find arrival field
        print("\n4️⃣  Looking for arrival (To) field...")
        arrival_selectors = [
            "[data-test*='destination']",
            "input[placeholder*='To']",
            "[data-test='SearchField-input']:last-of-type"
        ]
        
        for selector in arrival_selectors:
            try:
                element = page.locator(selector).first
                if element.is_visible(timeout=2000):
                    print(f"✓ Found arrival field: {selector}")
                    element.click()
                    time.sleep(1)
                    element.type("MAD", delay=100)
                    print(f"✓ Typed MAD")
                    time.sleep(2)
                    
                    # Try to click suggestion
                    try:
                        suggestion = page.locator("[data-test='PlacePickerRow']:has-text('MAD')").first
                        if suggestion.is_visible(timeout=2000):
                            suggestion.click()
                            print("✓ Selected from dropdown")
                    except:
                        page.keyboard.press("Enter")
                        print("✓ Pressed Enter")
                    
                    break
            except Exception as e:
                print(f"✗ {selector} failed: {e}")
        
        time.sleep(2)
        
        # Date picker
        print("\n5️⃣  Looking for date picker...")
        print("ℹ️  Manually inspect the date picker and tell me what you see")
        input("Press Enter after you've looked at the date picker...")
        
        # Search button
        print("\n6️⃣  Looking for search button...")
        search_selectors = [
            "[data-test='LandingSearchButton']",
            "button:has-text('Search')",
            "button[type='submit']"
        ]
        
        for selector in search_selectors:
            try:
                element = page.locator(selector).first
                if element.is_visible(timeout=2000):
                    print(f"✓ Found search button: {selector}")
                    break
            except Exception as e:
                print(f"✗ {selector} failed")
        
        print("\n✅ Script finished. Keep browser open to inspect elements...")
        input("Press Enter to close browser...")
        
        browser.close()

if __name__ == "__main__":
    print("="*60)
    print("Kiwi.com Selector Discovery Tool")
    print("="*60)
    find_selectors()