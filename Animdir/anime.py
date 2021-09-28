from Moon import *
from Import import *
from HVAnimeBot import dispatcher

__anime__ = "🔥 Get Anime"

def t(milliseconds: int) -> str:
    """Inputs time in milliseconds, to get beautified time,
    as string"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + " Days, ") if days else "")
        + ((str(hours) + " Hours, ") if hours else "")
        + ((str(minutes) + " Minutes, ") if minutes else "")
        + ((str(seconds) + " Seconds, ") if seconds else "")
        + ((str(milliseconds) + " ms, ") if milliseconds else "")
    )
    return tmp[:-2]
def findanime(update: Update, context: CallbackContext):
    message = update.effective_message
    search = message.text.split(" ", 1)
    if len(search) == 1:
        update.effective_message.reply_text("Format : /findanime < findanime name >")
        return
    else:
        search = search[1]
    variables = {"search": search}
    json = requests.post(
        url, json={"query": anime_query, "variables": variables}
    ).json()
    if "errors" in json.keys():
        update.effective_message.reply_text("Anime not found")
        return
    if json:
        json = json["data"]["Media"]
        msg = f"""
*{json['title']['romaji']}*(`{json['title']['native']}`)

*Type*: {json['format']}

*Status*: {json['status']}

*Episodes*: {json.get('episodes', 'N/A')}

*Duration*: {json.get('duration', 'N/A')} Per Ep.

*Stars Given*: {json['averageScore']}

*Genres*: `

📺Ðêv Mêñ†ïðñ:
 @KrakinzBot | @Krakinz
—⚡️••÷[  Aռɨʍɛ-աɛɛɮɛʀ  ]÷••⚡️—"""
        for x in json["genres"]:
            msg += f"{x}, "
        msg = msg[:-2] + "`\n"
        msg += "*Studios*: `"
        for x in json["studios"]["nodes"]:
            msg += f"{x['name']}, "
        msg = msg[:-2] + "`\n"
        info = json.get("siteUrl")
        trailer = json.get("trailer", None)
        anime_id = json["id"]
        if trailer:
            trailer_id = trailer.get("id", None)
            site = trailer.get("site", None)
            if site == "youtube":
                trailer = "https://youtu.be/" + trailer_id
        description = (
            json.get("description", "N/A")
            .replace("<i>", "")
            .replace("</i>", "")
            .replace("<br>", "")
        )
        msg += shorten(description, info)
        image = json.get("bannerImage", None)
        if trailer:
            buttons=[[
                InlineKeyboardButton(
                "Get To Know More",
                url=info),
                InlineKeyboardButton(
                "Trailer 🎬",
                url=trailer)
                ]]
        else:
            buttons=[[
                InlineKeyboardButton(
                "Get To Know More",
                url=info)
                ]]
        if image:
            try:
                update.effective_message.reply_photo(
                photo=image,
                caption=msg,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(buttons))
            except:
                msg += f" [〽️]({image})"
                update.effective_message.reply_text(
                msg,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(buttons))
        else:
            update.effective_message.reply_text(
            msg,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(buttons))
def findmanga(update: Update, context: CallbackContext):
    message = update.effective_message
    search = message.text.split(" ", 1)
    if len(search) == 1:
        update.effective_message.reply_text(
        "Format : /findmanga < findmanga name >")
        return
    search = search[1]
    variables = {
    "search": search}
    json = requests.post(
    url, json={
    "query": manga_query,
    "variables": variables}
    ).json()
    msg = ""
    if "errors" in json.keys():
        update.effective_message.reply_text(
        "Manga not found")
        return
    if json:
        json = json["data"]["Media"]
        title,title_native = json["title"].get("romaji", False), json["title"].get(
        "native", False)
        start_date,status,score =(
        json["startDate"].get("year", False),
        json.get("status", False),
        json.get("averageScore", False))
        if title:
            msg += f"*{title}*"
            if title_native:
                msg += f"(`{title_native}`)"
        if start_date:
            msg += f"\n*Start Date* - `{start_date}`"
        if status:
            msg += f"\n*Status* - `{status}`"
        if score:
            msg += f"\n*Score* - `{score}`"
        msg += "\n*Genres* - "
        for x in json.get("genres", []):
            msg += f"{x}, "
        msg = msg[:-2]
        info = json["siteUrl"]
        buttons = [[InlineKeyboardButton("Get To Know More", url=info)]]
        image = json.get("bannerImage", False)
        msg += f"_{json.get('description', None)}_"
        if image:
            try:
                update.effective_message.reply_photo(
                photo=image,
                caption=msg,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(buttons))
            except:
                msg += f" [〽️]({image})"
                update.effective_message.reply_text(
                msg,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(buttons))
        else:
            update.effective_message.reply_text(
            msg,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(buttons))

def site_search(update: Update, context: CallbackContext, site: str):
    message = update.effective_message
    args = message.text.strip().split(" ", 1)
    more_results = True
    try:
        search_query = args[1]
    except IndexError:
        message.reply_text(
        "Give something to search")
        return
    if site == "download1":
        search_url = f"https://animekaizoku.com/?s={search_query}"
        html_text = requests.get(search_url).text
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("h2", {"class": "post-title"})
        if search_result:
            result = f"<b>Search results for</b> <code>{html.escape(search_query)}</code> <b>on</b> @KayoAnime: \n"
            for entry in search_result:
                post_link = "https://animekaizoku.com/" + entry.a["href"]
                post_name = html.escape(entry.text)
                result += f"• <a href='{post_link}'>{post_name}</a>\n"
        else:
            more_results = False
            result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> @KaizokuAnime"
    elif site == "download2":
        search_url = f"https://animekayo.com/?s={search_query}"
        html_text = requests.get(search_url).text
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("h2", {"class": "title"})
        result = f"<b>Search results for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKayo</code>: \n"
        for entry in search_result:
            if entry.text.strip() == "Nothing Found":
                result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKayo</code>"
                more_results = False
                break
            post_link = entry.a["href"]
            post_name = html.escape(entry.text.strip())
            result += f"• <a href='{post_link}'>{post_name}</a>\n"
    buttons =[[
        InlineKeyboardButton(
        "See all results",
        url=search_url)
        ]]
    if more_results:
        message.reply_text(
        result,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True)
    else:
        message.reply_text(
        result,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True)
def download1(update: Update, context: CallbackContext):
    site_search(
    update,
    context,
    "download1")
def download2(update: Update, context: CallbackContext):
    site_search(
    update,
    context,
    "download2")
def shorten(description, info="anilist.co"):
    msg = ""
    if len(description) > 700:
        description = description[0:500] + "...."
        msg += f"\n*Description*: _{description}_[Read More]({info})"
    else:
        msg += f"\n*Description*:_{description}_"
    return msg

OUT = UT

ANIME_HANDLER = CommandHandler("findanime", findanime, run_async=True)
MANGA_HANDLER = CommandHandler("findmanga", findmanga, run_async=True)
KAIZOKU_SEARCH_HANDLER = CommandHandler("download1", download1, run_async=True)
KAYO_SEARCH_HANDLER = CommandHandler("download2", download2, run_async=True)

dispatcher.add_handler(ANIME_HANDLER)
dispatcher.add_handler(MANGA_HANDLER)
dispatcher.add_handler(KAIZOKU_SEARCH_HANDLER)


__command_list__ = ["findanime","findmanga","download1","download2"]
__handlers__ = [ANIME_HANDLER,MANGA_HANDLER,KAIZOKU_SEARCH_HANDLER,KAYO_SEARCH_HANDLER]