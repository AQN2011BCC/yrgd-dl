from botasaurus.browser import browser, Driver
from botasaurus.soupify import soupify

b = str(input("link: "))

@browser(
        profile="test"
)
def run(driver: Driver, b):
    driver.google_get("https://yurigarden.moe/login?redirect=%2Flogin", bypass_cloudflare=True)
    driver.prompt("pls login, enter to continue...")
    driver.short_random_sleep()
    driver.google_get(b, bypass_cloudflare=True)
    driver.short_random_sleep()
    driver.scroll_to_bottom()
    html = driver.page_html
    soup = soupify(html)
    a =  soup.prettify()
    with open("yrgd_c.html", "w", encoding="utf-8") as c:
        c.write(a)

run(b)  # pyright: ignore[reportCallIssue]
