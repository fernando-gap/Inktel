from aqt import gui_hooks, mw, qconnect
from aqt.qt import QCheckBox, QMenu, QWidgetAction
from aqt.reviewer import Reviewer
from aqt.webview import WebContent

import os

class Application:
    def __init__(self) -> None:
        self.addon_path = os.path.dirname(__file__)
        self.config = mw.addonManager.getConfig(__name__)
        mw.addonManager.setWebExports(__name__, r"web/.*(css|js|html)")

        if not self.config:
            self.config = { "enable": False }

            with open(f"{self.addon_path}/config.json", "w") as f:
                f.write("{}")

            mw.addonManager.writeConfig(__name__, self.config)

        self._menubar()

        gui_hooks.webview_will_set_content.append(
            self.on_webview_will_set_content)

    def on_webview_will_set_content(self, web_content: WebContent, context) -> None:
        if not isinstance(context, Reviewer):
            return
        
        addon_package = mw.addonManager.addonFromModule(__name__)
        web_content.js.append(f"/_addons/{addon_package}/web/js/canvas.js")
        web_content.js.append(f"/_addons/{addon_package}/web/js/main.js")
        web_content.js.append(f"/_addons/{addon_package}/web/js/paint.js")
        web_content.css.append(f"/_addons/{addon_package}/web/css/style.css")

        # inject html file
        with open(f"{self.addon_path}/web/html/index.html") as f:
            web_content.body += f.read()
            # disable extension when "enable" is off
            web_content.body += f'<script>{self._set_visible(self.config["enable"])}</script>'

    
    def enable_disable_inktel(self):
        self.config["enable"] = not self.config["enable"]
        mw.web.eval(self._set_visible(self.config["enable"]))
        mw.addonManager.writeConfig(__name__, self.config)
    
    def _set_visible(self, is_visible: bool) -> str:
        return f"""
            document.getElementById("inktel-addon")
                .style.display = {str(is_visible).lower()} 
                    ? "block" 
                    : "none" 
            """

    def _menubar(self):
        checkbox = QCheckBox("Enable Inktel Extension")
        checkbox.setChecked(self.config["enable"])
        menu = QMenu("Inktel", parent=mw.form.menubar)
        action = QWidgetAction(menu)
        action.setDefaultWidget(checkbox)
        qconnect(checkbox.stateChanged, self.enable_disable_inktel)
        menu.addAction(action)
        mw.form.menuTools.addMenu(menu)
    
app = Application()