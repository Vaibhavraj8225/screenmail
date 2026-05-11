import asyncio
import os
import email
from pathlib import Path
from playwright.async_api import async_playwright

EMAIL_DIR = "emails"
SCREENSHOT_DIR = "screenshots"
RENDER_DIR = "rendered"

os.makedirs(SCREENSHOT_DIR, exist_ok=True)
os.makedirs(RENDER_DIR, exist_ok=True)


# ----------------------------------------
# Extract HTML from EML
# ----------------------------------------

def extract_html_from_eml(eml_path):
    with open(eml_path, 'rb') as f:
        msg = email.message_from_binary_file(f)

    html_content = None

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()

            if content_type == "text/html":
                payload = part.get_payload(decode=True)
                charset = part.get_content_charset() or 'utf-8'
                html_content = payload.decode(charset, errors='ignore')
                break
    else:
        if msg.get_content_type() == "text/html":
            payload = msg.get_payload(decode=True)
            charset = msg.get_content_charset() or 'utf-8'
            html_content = payload.decode(charset, errors='ignore')

    return html_content


# ----------------------------------------
# Render email and take screenshot
# ----------------------------------------

async def render_email(browser, html_path, screenshot_path):

    page = await browser.new_page(
        viewport={
            "width": 1400,
            "height": 1200
        }
    )

    await page.goto(
        f"file://{os.path.abspath(html_path)}",
        wait_until="networkidle"
    )

    # ------------------------------------------------
    # Remove default margins
    # ------------------------------------------------

    await page.add_style_tag(content="""
        body {
            margin: 0 !important;
            padding: 20px !important;
            background: #ffffff !important;
        }
    """)

    # ------------------------------------------------
    # FIX BROKEN EMAIL HEIGHTS
    # ADD THIS BLOCK HERE
    # ------------------------------------------------

    await page.evaluate("""
    () => {

        const all = document.querySelectorAll('*');

        all.forEach(el => {

            const style = window.getComputedStyle(el);

            if (
                style.minHeight === '100vh' ||
                el.style.height === '100%'
            ) {
                el.style.minHeight = 'auto';
                el.style.height = 'auto';
            }
        });
    }
    """)

    # ------------------------------------------------
    # ZOOM EMAIL CONTENT
    # ADD THIS BLOCK HERE
    # ------------------------------------------------

    await page.evaluate("""
    () => {
        document.body.style.zoom = "1.3";
    }
    """)

    # Wait after modifications
    await page.wait_for_timeout(1500)

    # ------------------------------------------------
    # Measure actual content
    # ------------------------------------------------

    dimensions = await page.evaluate("""
    () => {

        const body = document.body;
        const html = document.documentElement;

        const width = Math.max(
            body.scrollWidth,
            body.offsetWidth,
            html.clientWidth,
            html.scrollWidth,
            html.offsetWidth
        );

        const height = Math.max(
            body.scrollHeight,
            body.offsetHeight,
            html.clientHeight,
            html.scrollHeight,
            html.offsetHeight
        );

        return {
            width: Math.min(width, 1600),
            height: Math.min(height, 5000)
        };
    }
    """)

    await page.set_viewport_size({
        "width": dimensions["width"],
        "height": min(dimensions["height"], 5000)
    })

    body = await page.query_selector("body")

    await body.screenshot(
        path=screenshot_path
    )

    await page.close()

# ----------------------------------------
# Process single email
# ----------------------------------------

async def process_email(browser, eml_file):

    try:
        print(f"Processing: {eml_file}")

        html_content = extract_html_from_eml(eml_file)

        if not html_content:
            print(f"No HTML found: {eml_file}")
            return

        filename = Path(eml_file).stem

        html_path = os.path.join(RENDER_DIR, f"{filename}.html")
        screenshot_path = os.path.join(
            SCREENSHOT_DIR,
            f"{filename}.png"
        )

        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        await render_email(
            browser,
            html_path,
            screenshot_path
        )

        print(f"Saved: {screenshot_path}")

    except Exception as e:
        print(f"Error processing {eml_file}: {e}")


# ----------------------------------------
# Main
# ----------------------------------------

async def main():

    eml_files = [
        os.path.join(EMAIL_DIR, f)
        for f in os.listdir(EMAIL_DIR)
        if f.endswith(".eml")
    ]

    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=True
        )

        tasks = [
            process_email(browser, eml)
            for eml in eml_files
        ]

        await asyncio.gather(*tasks)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
