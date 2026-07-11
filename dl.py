import os
import base64
import time
import re
from botasaurus.browser import Driver
import conf
import random

def ran():
    X = 1
    return random.uniform(0.5*x, 0.75*x)

def login(driver: Driver):
    driver.google_get("https://yurigarden.moe/login?redirect=%2Flogin", bypass_cloudflare=True)
    driver.wait_for_element('input[type="email"]')
    driver.click('input[type="email"]')
    driver.type('input[type="email"]', conf.EMAIL)
    driver.wait_for_element('input[type="password"]')
    driver.click('input[type="password"]')
    driver.type('input[type="password"]', conf.PASSWD)
    driver.click('button[type="submit"]')
    driver.short_random_sleep()

def cl_n(n):
    if not n:
        return "Unknown"
    
    n = n.strip()
    n = re.sub(r'[\\/*?:"<>|]', "", n)
    n = re.sub(r'\.+$', lambda match: '․' * len(match.group(0)), n)
    n = n.rstrip(" ")
    return n

def dl(driver: Driver, chapter_url):
    time.sleep(1)
    dl = "Downloads"
    driver.wait_for_element('title')
    tt = driver.get_text('title')
    s_tt = cl_n(tt)

    driver.wait_for_element('h1')
    cm_n = driver.get_text('h1')
    s_cm_n = cl_n(cm_n)

    opd = os.path.join(dl, s_tt, s_cm_n)
    if not os.path.exists(opd):
        os.makedirs(opd)

    sc = sec = lsy = sr = 0
    msr = 12
    pci = set()

    driver.run_js("window.scrollTo({ top: 0, behavior: 'smooth' });")
    time.sleep(ran())

    while True:
        try:
            c_url = driver.current_url
            if "login" in c_url.lower():
                try:
                    login(driver)
                    driver.short_random_sleep()
                    c_url = driver.current_url
                    if not "login" in c_url.lower():
                        driver.google_get(chapter_url)
                        driver.short_random_sleep()
                    else:
                        login(driver)

                    if lsy > 0:
                        driver.run_js(f"window.scrollTo(0, {lsy});")

                    sec = 0
                    continue

                except Exception as log_er:
                    print(f"Error: {log_er}")
                    continue

            if "yurigarden.moe" not in c_url:
                driver.google_get(chapter_url)
                if lsy > 0:
                    driver.run_js(f"window.scrollTo(0, {lsy});")

                sec = 0
                continue

            cs = driver.run_js("return window.scrollY;")

            if cs > lsy:
                lsy = cs

            cb = """
            return (window.innerHeight + window.scrollY) >= (document.documentElement.scrollHeight - 60);
            """
            ib = driver.run_js(cb) 

            fi = """
            const getCenteredCanvasId = () => {
                const canvases = Array.from(document.querySelectorAll('canvas'));
                const viewCenter = window.innerHeight / 2;
                for (const canvas of canvases) {
                    const id = canvas.id.toLowerCase();
                    const className = canvas.className.toLowerCase();
                    if (id.includes('trap') || className.includes('trap') || id.includes('hidden') || className.includes('hidden')) continue;
                    if (canvas.width < 400 || canvas.height < 400) continue; 
                    const rect = canvas.getBoundingClientRect();
                    if (rect.top <= viewCenter && rect.bottom >= viewCenter) {
                        return { found: true, id: canvas.id };
                    }
                }
                return { found: false };
            };
            return getCenteredCanvasId();
            """
            
            r = driver.run_js(fi)
            if r and r.get("found"):
                ci = r.get("id")
                if ci not in pci:
                    sc += 1
                    sec += 1
                    sr = 0 
                                        
                    es = f"""
                    const target = document.getElementById('{ci}');
                    if (target && target.width > 0 && target.height > 0) {{
                        return target.toDataURL('image/webp', 1.0);
                    }}
                    return "NOT_RENDERED";
                    """
                    d_url = driver.run_js(es)
                    if d_url and d_url.startswith("data:image"):
                        _, ed = d_url.split(",", 1)
                        ib = base64.b64decode(ed)
                        
                        fn = f"page_{str(sc).zfill(3)}.webp"
                        fp = os.path.join( opd, fn)
                        
                        with open(fp, "wb") as f:
                            f.write(ib)
                        pci.add(ci) 
                        if sec >= 8:
                            driver.google_get(chapter_url)
                            time.sleep(ran())
                            driver.run_js(f"window.scrollTo(0, {lsy});")
                            sec = 0
                            continue

                        driver.run_js("window.scrollBy({ top: window.innerHeight * 0.75, behavior: 'smooth' });")
                    else:
                        sc -= 1
                        sec -= 1
                else:
                    sr += 1
                    driver.run_js("window.scrollBy({ top: 250, behavior: 'smooth' });")
            else:
                sr += 1
                if ib and sr >= 3:
                    break

                driver.run_js("window.scrollBy({ top: 300, behavior: 'smooth' });")
            if sr >= msr:
                break
            
            time.sleep(ran())

        except Exception as e:
            er = str(e).lower()

            if "target tab or iframe is no longer available" in er or "connection" in er:
                print("Lost connect.")
                break
            else:
                print(f"Error: {e}")
                continue

    return {"status": "completed"}
