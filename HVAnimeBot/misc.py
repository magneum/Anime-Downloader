from time import sleep
from typing import Dict, List
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardButton



class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text

def pages(page_n: int, module_dict: Dict, prefix, chat=None) -> List:
    if not chat:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x.__anime__,
                    callback_data="{}_module({})".format(
                        prefix, x.__anime__.lower()
                    ),
                )
                for x in module_dict.values()
            ]
        )
    else:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x.__anime__,
                    callback_data="{}_module({},{})".format(
                        prefix, chat, x.__anime__.lower()
                    ),
                )
                for x in module_dict.values()
            ]
        )

    pairs = [modules[i * 3 : (i + 1) * 3] for i in range((len(modules) + 3 - 1) // 3)]

    round_num = len(modules) / 3
    calc = len(modules) - round(round_num)
    if calc in [1, 2]:
        pairs.append((modules[-1],))
    return pairs




def is_module_loaded(name):
    return name


def delete(delmsg, timer):
    sleep(timer)
    try:
        delmsg.delete()
    except:
        return
