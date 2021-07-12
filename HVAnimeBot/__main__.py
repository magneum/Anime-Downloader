from Moon import *
from Import import *
from Animdir import ALL_MODULES
from HVAnimeBot import updater,LOGGER




for module_name in ALL_MODULES:
    imported_module = importlib.import_module("Animdir." + module_name)
    if not hasattr(imported_module, "__anime__"):
        imported_module.__anime__ = imported_module.__name__

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__anime__.lower()] = imported_module
 


    

updater.start_polling(timeout=15, read_latency=4, drop_pending_updates=True)
LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
LOGGER.info("Ready")
updater.idle()
LOGGER.info("Offline .... Powered Off")