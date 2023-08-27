from aqt import gui_hooks, mw, qconnect
from aqt.qt import QCheckBox, QMenu, QWidgetAction
from aqt.reviewer import Reviewer
from aqt.webview import WebContent

import os

class Application:
    is_running = False

    def __init__(self) -> None:
        self._load_addon_files()
        self._menubar()

    def on_webview_will_set_content(self, web_content: WebContent, context) -> None:
        if not isinstance(context, Reviewer):
            return
        
        addon_package = mw.addonManager.addonFromModule(__name__)
        web_content.js.append(f"/_addons/{addon_package}/js/canvas.js")
        web_content.js.append(f"/_addons/{addon_package}/js/main.js")

        
        # inject html file
        with open(f"{os.path.dirname(__file__)}/html/index.html") as f:
            web_content.body += f.read()
    
    def enable_disable_inktel(self):
        """Disable extension by removing hook. 
           Changes only apply on the next webview_will_set_content event.
        """

        self.is_running = not self.is_running

        # if self.is_running:
        #     gui_hooks.webview_will_set_content.append(self.on_webview_will_set_content)
        # else:
        #     gui_hooks.webview_will_set_content.remove(self.on_webview_will_set_content)

    def _menubar(self):
        checkbox = QCheckBox("Enable Inktel Extension")
        menu = QMenu("Inktel", parent=mw.form.menubar)
        action = QWidgetAction(menu)
        action.setDefaultWidget(checkbox)
        qconnect(checkbox.stateChanged, self.enable_disable_inktel)
        menu.addAction(action)
        mw.form.menuTools.addMenu(menu)
    
    def _load_addon_files(self):
        mw.addonManager.setWebExports(__name__, r"js/.*js")
        gui_hooks.webview_will_set_content.append(self.on_webview_will_set_content)


app = Application()