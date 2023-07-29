"""Make some requests to OpenAI's chatbot"""

import time
import os
import flask
from flask import g
from flask import request

from playwright.sync_api import sync_playwright


def create_dir():
    # Get the current directory
    current_dir = os.getcwd()

    # Create the playwright directory if not exist
    playwright_dir = os.path.join(current_dir, 'playwright')
    if not os.path.exists(playwright_dir):
        os.makedirs(playwright_dir)

    return playwright_dir

playwright_dir = create_dir()

APP = flask.Flask(__name__)
PLAY = sync_playwright().start()
BROWSER = PLAY.chromium.launch_persistent_context(
    user_data_dir=playwright_dir,
    headless=False,
)
PAGE = BROWSER.new_page()

def get_input_box():
    """Get the child textarea of `PromptTextarea__TextareaWrapper`"""
    return PAGE.query_selector("textarea")

def is_logged_in():
    # See if we have a textarea with data-id="root"
    return get_input_box() is not None

def is_button_visible_and_correct():
    """Check if a button with a specific class"""
    button = PAGE.query_selector(".btn.relative.btn-neutral.whitespace-nowrap.-z-0.border-0.md\\:border")

    # Check visibility and text
    if button and button.is_visible(): # and button.inner_text() == "Regenerate":
        return True

    return False

def is_loading_response() -> bool:
    """See if the regenerate button is visible, if it does, we're not loading"""
    return not is_button_visible_and_correct()

def send_message(message):
    # Send the message
    box = get_input_box()
    box.click()
    box.fill(message)
    box.press("Enter")

def get_last_message():
    """Get the latest message"""
    while is_loading_response():
        time.sleep(0.25)
    print('wait for response over')
    page_elements = PAGE.query_selector_all(".markdown.prose.w-full.break-words.dark\\:prose-invert.light")
    if page_elements:  # Check if any elements were found
        last_element = page_elements[-1]  # -1 returns the last element in the list, last message
        return last_element.inner_text()
    else:
        return None

def regenerate_response():
    """Clicks on the Try again button.
    Returns None if there is no button"""
    try_again_button = PAGE.query_selector("button:has-text('Regenerate')")
    if try_again_button is not None:
        try_again_button.click()
    return try_again_button

def get_reset_button():
    """Returns the reset thread button (it is an a tag not a button)"""
    return PAGE.query_selector("a:has-text('Reset thread')")

@APP.route("/chat", methods=["POST"])
def chat():
    message = request.json['message']
    print("Sending message: ", message)
    send_message(message)
    response = get_last_message()
    print("Response: ", response)
    return response

# create a route for regenerating the response
@APP.route("/regenerate", methods=["POST"])
def regenerate():
    print("Regenerating response")
    if regenerate_response() is None:
        return "No response to regenerate"
    response = get_last_message()
    print("Response: ", response)
    return response

@APP.route("/reset", methods=["POST"])
def reset():
    print("Resetting chat")
    get_reset_button().click()
    return "Chat thread reset"

@APP.route("/restart", methods=["POST"])
def restart():
    global PAGE,BROWSER,PLAY
    PAGE.close()
    BROWSER.close()
    PLAY.stop()
    time.sleep(0.25)
    PLAY = sync_playwright().start()
    BROWSER = PLAY.chromium.launch_persistent_context(
        user_data_dir=playwright_dir,
        headless=False,
    )
    PAGE = BROWSER.new_page()
    PAGE.goto("https://chat.openai.com/")
    return "API restart!"


def start_browser():
    PAGE.goto("https://chat.openai.com/")
    if not is_logged_in():
        print("Please log in to OpenAI Chat")
        print("Press enter when you're done")
        input()
    else:
        print("Logged in")
        APP.run(port=5001, threaded=False)

if __name__ == "__main__":
    start_browser()
