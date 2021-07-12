import os
import re
import bs4
import sys
from loguru import logger
import telegram.ext as tg
import logging
import datetime
import textwrap
import importlib
import jikanpy
from time import sleep
from typing import Dict, List
from telegram import InlineKeyboardButton
import requests
import html
from telegram.error import BadRequest
from HVAnimeBot.misc import pages
from telegram.utils.helpers import escape_markdown
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler, run_async
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update