"""
•=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=•
                                                       GNU GENERAL PUBLIC LICENSE 
                                                         Version 3, 29 June 2007
                                                Copyright (C) 2007 Free Software Foundation
                                            Everyone is permitted to 𝗰𝗼𝗽𝘆 𝗮𝗻𝗱 𝗱𝗶𝘀𝘁𝗿𝗶𝗯𝘂𝘁𝗲 verbatim copies
                                                of this license document, 𝗯𝘂𝘁 𝗰𝗵𝗮𝗻𝗴𝗶𝗻𝗴 𝗶𝘁 𝗶𝘀 𝗻𝗼𝘁 𝗮𝗹𝗹𝗼𝘄𝗲𝗱.
                                                has been licensed under GNU General Public License
                                                𝐂𝐨𝐩𝐲𝐫𝐢𝐠𝐡𝐭 (𝐂) 𝟐𝟎𝟐𝟏 𝗞𝗿𝗮𝗸𝗶𝗻𝘇 | 𝗞𝗿𝗮𝗸𝗶𝗻𝘇𝗟𝗮𝗯 | 𝗞𝗿𝗮𝗸𝗶𝗻𝘇𝗕𝗼𝘁
•=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=••=•
"""
from Moon import *
from Import import *
from .help import send_help
from HVAnimeBot import dispatcher


def start(update: Update, context: CallbackContext):
    args = context.args
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("ghelp_"):
                mod = args[0].lower().split("_", 1)[1]
                if not HELPABLE.get(mod, False):
                    return
                send_help(
                    update.effective_chat.id,
                    HELPABLE[mod].__help__,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(
                            text="Back", callback_data="help_back")]]
                    ),
                )
            elif args[0].lower() == "markdownhelp":
                IMPORTED["extras"].markdown_help_sender(update)
        else:
            first_name = update.effective_user.first_name
            update.effective_message.reply_photo(
                ASTRAKOBOT_IMG,
                PM_START_TEXT.format(
                    escape_markdown(first_name), escape_markdown(
                        context.bot.first_name)
                ),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Add HVAnimeBot to your group",
                                url="t.me/{}?startgroup=true".format(
                                    context.bot.username
                                ),
                            )
                        ],
                    ]
                ),
            )
    else:
        update.effective_message.reply_text(
            "I'm awake already!\n<b>Haven't slept since:</b> <code>{}</code>",
            parse_mode=ParseMode.HTML,
        )


start_handler = CommandHandler("start", start, run_async=True)
dispatcher.add_handler(start_handler)
