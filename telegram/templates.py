# -- IMPORTS --
from telegram import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


# -- ANSWER TEMPLATES --
def not_found_answer() -> InlineQueryResultArticle:
    keyboard_button = InlineKeyboardButton(
        text="🎵 Add sounds",
        url="http://127.0.0.1:8000/api/sounds/download",
    )
    return InlineQueryResultArticle(
        id="no_results_prompt",
        title="No sounds found...",
        description="Click here to open the web panel and add new sounds!",
        reply_markup=InlineKeyboardMarkup([[keyboard_button]]),
        input_message_content=InputTextMessageContent("Add your sounds on the website"),
    )


def error_answer() -> InlineQueryResultArticle:
    return InlineQueryResultArticle(
        id="error_prompt",
        title="Oops! Error fetching sounds.",
        description="Try again later!",
        input_message_content=InputTextMessageContent("Sorry, something is broken..."),
    )
