#!/usr/bin/env python3
"""
Madness Card Generator for Klutz's Card Factory
Uses Selenium to automate card creation and save each card image.

Requirements:
    pip install selenium webdriver-manager pandas

Usage:
    python create_cards.py <csv_file> [output_dir] --type <card_type>

    Example:
    python create_cards.py "../Madness/cards.csv" --type "Madness"
    python create_cards.py "../Madness/cards.csv" "my_cards" --type "Madness"

Requirements:
    pip install selenium webdriver-manager pandas
"""

import time
import os
import base64
import argparse
#import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

import base64
import io
#from PIL import Image # Pillow library is useful for image manipulation

# ── Configuration ─────────────────────────────────────────────────────────────
URL        = "https://cardfactory.kbelisle.ca/"
import pandas as pd

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Generate cards for Klutz\'s Card Factory')
    parser.add_argument('csv', type=str,
                       help='Path to the CSV file containing card data')
    parser.add_argument('output', type=str, nargs='?', default='output',
                       help='Output directory for generated card images (default: output)')
    parser.add_argument('--type', type=str, required=True,
                       choices=['Injury', 'Madness', 'Mutation'],
                       help='Type of cards to generate')
    return parser.parse_args()

# Global variables to store parsed arguments
args = parse_arguments()
CSV_FILE   = args.csv
CARDS = pd.read_csv(CSV_FILE, na_filter=False)
CARDS = CARDS.to_dict(orient='records')
#print(CARDS)
OUTPUT_DIR = args.output
CARD_TYPE = args.type
# ──────────────────────────────────────────────────────────────────────────────


def wait_and_find(driver, by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )


def clear_and_type(element, text):
    element.clear()
    element.send_keys(text)


def click_button_by_text(driver, text):
    """Click a button/input whose visible text or aria-label matches."""
    # Try <button> first
    buttons = driver.find_elements(By.XPATH, f"//button[normalize-space()='{text}']")
    if not buttons:
        # Try <input type="button"> or role="button"
        buttons = driver.find_elements(
            By.XPATH,
            f"//input[@value='{text}' or @aria-label='{text}']"
        )
    if buttons:
        driver.execute_script("arguments[0].scrollIntoView(true);", buttons[0])
        time.sleep(0.2)
        buttons[0].click()
        return True
    return False


def get_body_component_count(driver):
    """Return how many body components are currently in the list."""
    return len(driver.find_elements(By.CSS_SELECTOR, ".bodyComponentRow, [class*='bodyComponent']"))

def get_text_field(driver, label_text):
    """Get a text field by its label text."""
    return driver.find_element(By.XPATH, f"//label//span[@class='title'][.='{label_text}']/following-sibling::input[@type='text']")

def save_base64_image(image_base64, filename):
    # Remove the "data:image/png;base64," prefix if present
    if "base64," in image_base64:
        _, base64_data = image_base64.split(",", 1)
    else:
        base64_data = image_base64

    # Decode the base64 string to bytes
    image_bytes = base64.b64decode(base64_data)

    # Save the image using Pillow or standard file operations
    #try:
    #    image = Image.open(io.BytesIO(image_bytes))
    #    image.save(filename)
    #except Exception as e:
    #    print(f"Failed to save image: {e}")
        # Or simply write the bytes to a file
    with open(filename, "wb") as f:
        f.write(image_bytes)

def save_image_from_element(driver, element, filename):
    js_script = """
    const blobUrl = arguments[0];
    const callback = arguments[1];
    fetch(blobUrl)
        .then(response => response.blob())
        .then(blob => {
            const reader = new FileReader();
            reader.onloadend = function() {
                callback(reader.result);
            };
            reader.readAsDataURL(blob);
        });
    """
    image_base64 = driver.execute_async_script(js_script, element)

    # Save the base64 image
    save_base64_image(image_base64, filename)


def save_image_from_element_screenshot(driver, element, filename):
    """Save an image element as a file."""
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    time.sleep(0.2)
    screenshot = element.screenshot_as_png
    with open(filename, "wb") as f:
        f.write(screenshot)

def make_condition_card(driver, wait, card, card_type):
    """Fill in and render one Condition card."""
    number   = card["Number rolled"]
    title     = card["Name"]
    keyword = card_type
    if keyword.lower() == "injury":
        dice = "Red 2D6"
    elif keyword.lower()  == "madness":
        dice = "Blue 2D6"
    elif keyword.lower()  == "mutation":
        dice = "Green D36"
        number = str(number)[0]+","+str(number)[1]
    else:
        raise f"Invalid type {type}"
    file_prefix = keyword.lower()
    #dice_labels = ["Green D36", "Green 2D6", "Blue D36", "Blue 2D6", "Orange D36", "Orange 2D6"]
    #bg_labels = ["Mutation Card", "Madness Card", "Injury Card"]

    background = f"{keyword} Card"
    body_components = [
        [ "Add Fluff Text", card["Description (green text)"] ],
        [ "Add Flourish Top", None ],
        [ "Add Card Text", card["Details (black text)"] ],
        [ "Add Flourish Bottom", None ],
    ]

    print(f"\n→ Creating card {number}: {title}")

    # ── Navigate to Condition Card (resets form) ───────────────────────────
    condition_link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[normalize-space()='Condition Card'] | //a[.//img[contains(@src,'mutation')]]")
    ))
    condition_link.click()
    time.sleep(0.5)

    # ── Title & Keywords ───────────────────────────────────────────────────
    title_input = wait.until(EC.presence_of_element_located((By.XPATH, "//label//span[@class='title'][.='Title:']/following-sibling::input[@type='text']")))
    #title_input = driver.find_element(By.XPATH, "//label//span[@class='title'][.='Title:']/following-sibling::input[@type='text']")
    clear_and_type(title_input, title)

    keywords_input = get_text_field(driver, 'Keywords:')
    clear_and_type(keywords_input, keyword)

    # ── Body components ────────────────────────────────────────────────────
    for component in body_components:
        button = component[0]
        text = component[1]

        click_button_by_text(driver, button)
        time.sleep(0.3)
        if text is not None:
            ta = driver.find_elements(By.XPATH, "//div[@id='bodyText']/ul/li[last()]/label/textarea") # last created text area
            clear_and_type(ta[0], text)

    # ── Toggleable Text Components ─────────────────────────────────────────

    ttc_checkboxes = driver.find_elements(
        By.XPATH,
        "//h3[contains(.,'Toggleable Text Components')]/following-sibling::*//input[@type='checkbox']"
    )
    for cb in ttc_checkboxes:
        try:
            label_text = cb.find_element(By.XPATH, "following-sibling::span[@class='title']").text
            if label_text == dice+":":
                if not cb.is_selected():
                    cb.click()

                # Fill value
                input_field = cb.find_element(By.XPATH, "following-sibling::input | ../following-sibling::*/input | ../..//input[not(@type='checkbox')]")
                clear_and_type(input_field, number)
            else:
                if cb.is_selected():
                    cb.click()
        except Exception as e:
            print(f"  Warning: could not handle toggle '{label_text}': {e}")

    # ── Background ─────────────────────────────────────────────────────────
    bo_checkboxes = driver.find_elements(
        By.XPATH,
        "//h3[contains(.,'Background Options')]/following-sibling::*//input[@type='checkbox']"
    )
    for cb in bo_checkboxes:
        try:
            label_text = cb.find_element(By.XPATH, "..").text
            if label_text == background:
                if not cb.is_selected():
                    cb.click()
            else:
                if cb.is_selected():
                    cb.click()
        except Exception as e:
            print(f"  Warning: could not handle background '{label_text}': {e}")

    # ── Draw Card ──────────────────────────────────────────────────────────
    draw_btn = wait.until(EC.element_to_be_clickable((By.ID, "drawCard")))
    driver.execute_script("arguments[0].scrollIntoView(true);", draw_btn)
    time.sleep(0.3)
    draw_btn.click()
    time.sleep(1.5)  # Wait for canvas to render
    #time.sleep(60)  # Wait for canvas to render

    # ── Save image ─────────────────────────────────────────────────────────
    try:
        img_element = wait.until(EC.presence_of_element_located((By.ID, "cardImg")))
        img_src = img_element.get_attribute("src")

        filename = f"{file_prefix}_{number}.png"
        filepath = os.path.join(OUTPUT_DIR, filename)

        save_image_from_element(driver, img_src, filepath)
    except Exception as e:
        print(f"  ✗ Failed to save image: {e}")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    options = Options()
    # options.add_argument("--headless")  # Uncomment to run without browser window
    options.add_argument("--window-size=1400,900")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage") # overcome limited resource problems
    options.add_argument("--no-sandbox") # Bypass OS security model

    service = Service(ChromeDriverManager().install())
    driver  = webdriver.Chrome(service=service, options=options)
    wait    = WebDriverWait(driver, 15)

    try:
        driver.get(URL)
        time.sleep(2)

        for card in CARDS:
            make_condition_card(driver, wait, card, CARD_TYPE)

        print(f"\n✓ All {len(CARDS)} cards created in '{OUTPUT_DIR}/'")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
