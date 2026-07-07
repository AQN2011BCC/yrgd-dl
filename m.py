import re
import time
import unicodedata
from botasaurus.browser import browser, Driver
import conf
from dl import dl, login, ran

@browser(
        profile="test",
        reuse_driver=False,
        wait_for_complete_page_load=True,
        add_arguments=[
            "--disable-notifications",
            "--disable-popup-blocking",
            "--disable-infobars",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-features=Translate",
            "--test-type", 
            "--disable-web-security"
        ]
)

def run(driver: Driver, data):
    result = {}
    driver.google_get("https://yurigarden.moe/", bypass_cloudflare=True)
    if "/login" in driver.current_url:
        print("Login required. Logging in...")
        login(driver)
    else:
        print("Already logged in. Proceeding to open the comic...")
    open_comic(driver, data)
    
    if conf.CHAPTER_LINK in driver.current_url:
        print("Direct link opened successfully.")
    else:
        print("non-direct link opened.")
        if conf.extract_information == 1:
            result = extract_information(driver, data)
        else:
            print("Information extraction is disabled.")
                
        driver.wait_for_element('div.group')        
        script = """
        return Array.from(document.querySelectorAll('div.group'))
                    .map(group => {
                        var span = group.querySelector('span.line-clamp-1');
                        return span ? span.innerText.trim() : null;
                    })
                    .filter(name => name !== null && name !== "");
        """
        all_chapter_names = driver.run_js(script)
        
        def extract_num(name: str) -> float | None:
            match = re.search(r'\d+(?:\.\d+)?', name)
            return float(match.group()) if match else None

        first_num = next((extract_num(n) for n in all_chapter_names if extract_num(n) is not None), None)
        last_num = next((extract_num(n) for n in reversed(all_chapter_names) if extract_num(n) is not None), None)

        is_newest_to_oldest = False
        if first_num is not None and last_num is not None:
            is_newest_to_oldest = first_num > last_num

        def get_chapter_index(user_input: str, is_start: bool) -> int | None:
            cleaned = unicodedata.normalize("NFC", user_input).lower().strip()
            if cleaned == "~":
                if is_start:
                    return (len(all_chapter_names) - 1) if is_newest_to_oldest else 0
                else:
                    return 0 if is_newest_to_oldest else (len(all_chapter_names) - 1)

            try:
                val_float = float(user_input)
                for i, name in enumerate(all_chapter_names):
                    if extract_num(name) == val_float:
                        return i
            except ValueError:
                pass

            for i, name in enumerate(all_chapter_names):
                if cleaned in unicodedata.normalize("NFC", name).lower():
                    return i

            return None

        start_idx = get_chapter_index(conf.START_CHAPTER, is_start=True)
        end_idx = get_chapter_index(conf.END_CHAPTER, is_start=False)

        if start_idx is None:
            print(f"Not found start chapter '{conf.START_CHAPTER}'.")
            return result
        if end_idx is None:
            print(f"Not found end chapter '{conf.END_CHAPTER}'.")
            return result

        if start_idx <= end_idx:
            chapters_to_process = all_chapter_names[start_idx : end_idx + 1]
        else:
            chapters_to_process = all_chapter_names[end_idx : start_idx + 1]
            chapters_to_process.reverse()
        
        for chapter_name in chapters_to_process:
            print(f"Processing chapter: {chapter_name}")
            if open_chapter(driver, chapter_name):
                chapter_url = driver.current_url
                time.sleep(ran())
                dl_result = dl(driver, chapter_url)
                if dl_result.get("status") == "completed":
                    print(f"Chapter '{chapter_name}' downloaded successfully.")
                else:
                    print(f"Failed to download chapter: {chapter_name}")
                time.sleep(ran())
                driver.google_get(conf.HOME_LINK, bypass_cloudflare=True)
                driver.wait_for_element('div.group')
            else:
                print(f"Failed to open chapter: {chapter_name}")
    
    return result

def open_comic(driver: Driver, _):
    if conf.direct_link == 1:
        driver.google_get(conf.HOME_LINK, bypass_cloudflare=True)
    elif conf.direct_chapter_link == 1:
        driver.google_get(conf.CHAPTER_LINK, bypass_cloudflare=True)
        chapter_url = conf.CHAPTER_LINK
        dl(driver, chapter_url)
    else:
        driver.wait_for_element('button[data-slot="button"][data-variant="ghost"][data-size="icon"]')
        driver.click('button[data-slot="button"][data-variant="ghost"][data-size="icon"]')
        driver.wait_for_element('input[data-slot="input"]')
        driver.click('input[data-slot="input"]')
        driver.type('input[data-slot="input"]', conf.NAME)
        driver.wait_for_element("a.search-dropdown")
        driver.click('a.search-dropdown')
        driver.short_random_sleep()

def extract_information(driver: Driver, _):
    name = description = author = translation_team = ""
    if conf.extract_information == 1:
        print("Extracting information...")
        if conf.name == 1:
            driver.wait_for_element('h1')
            name = driver.get_text('h1')
            if name == "":
                print("Failed to extract name.")
            else:
                print(f"Extracted name complete")
                
        if conf.description == 1:
            driver.wait_for_element('div.overflow-hidden p')
            description = driver.get_text('div.overflow-hidden p')
            if description == "":
                print("Failed to extract description.")
            else:
                print(f"Extracted description complete")
                
        if conf.author == 1:
            driver.wait_for_element('a')
            author = driver.get_text('a')
            if author == "":
                print("Failed to extract author.")
            else:
                print(f"Extracted author complete")
                
        if conf.translation_team == 1:
            driver.wait_for_element('a[href*="/team/"]')
            translation_team = driver.get_text('a[href*="/team/"]')
            if translation_team == "":
                print("Failed to extract translation team.")
            else:
                print(f"Extracted translation team complete")
                
        return {
            "tên": name,
            "mô tả": description,
            "tác giả": author,
            "nhóm dịch": translation_team
        }
    
def open_chapter(driver: Driver, chapter_name: str):
    escaped_name = chapter_name.replace('"', '\\"')
    script = f"""
        var targetName = "{escaped_name}".trim().toLowerCase().normalize("NFC");
        var groups = Array.from(document.querySelectorAll('div.group'));
        var found = false;
        for (var group of groups) {{
            var span = group.querySelector('span.line-clamp-1');
            if (span) {{
                var currentText = span.innerText.trim().toLowerCase().normalize("NFC");
                if (currentText === targetName) {{
                    group.scrollIntoView();
                    group.click();
                    found = true;
                    break;
                }}
            }}
        }}
        return found;
    """
    
    success = driver.run_js(script)
    if not success:
        print(f"Failed to open chapter: {chapter_name}")
        return False
    else:
        print(f"Opened chapter: {chapter_name}")
        return True

if __name__ == "__main__":
    run() # pyright: ignore[reportCallIssue]
