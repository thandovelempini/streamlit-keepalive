import sys
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

APPS = [
    "https://psl-scouting.streamlit.app/",
    "https://f1-talent-pipeline.streamlit.app/",
]

WAKE_TEXT = "get this app back up"


def visit(page, url):
    print(f"Visiting {url}")
    page.goto(url, wait_until="domcontentloaded", timeout=90_000)
    page.wait_for_timeout(8_000)

    button = page.get_by_role("button", name=WAKE_TEXT)
    if button.count() > 0:
        print("  App was asleep, waking it up...")
        button.first.click()
        page.wait_for_timeout(60_000)  # give it time to boot
    else:
        print("  App is awake.")
        page.wait_for_timeout(15_000)  # stay on the page so the visit counts
    return True


def main():
    failures = 0
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        for url in APPS:
            try:
                visit(page, url)
            except PWTimeout:
                print(f"  Timed out loading {url}")
                failures += 1
        browser.close()
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
