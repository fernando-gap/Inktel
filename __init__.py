from aqt import gui_hooks, mw, qconnect
from aqt.qt import QCheckBox, QMenu, QWidgetAction
from aqt.reviewer import Reviewer
from aqt.webview import WebContent

def on_webview_will_set_content(web_content: WebContent, context) -> None:
    if not isinstance(context, Reviewer):
        return
    
    addon_package = mw.addonManager.addonFromModule(__name__)
    web_content.js.append(f"/_addons/{addon_package}/js/canvas.js")
    web_content.js.append(f"/_addons/{addon_package}/js/main.js")
    web_content.body = '<canvas id="inktel"></canvas>' + web_content.body


def enable_disable_inktel(state):
    pass

# load js files
mw.addonManager.setWebExports(__name__, r"js/.*js")

# load menu bar
checkbox = QCheckBox("Enable Inktel")
menu = QMenu("Inktel", parent=mw.form.menubar)
action = QWidgetAction(menu)
action.setDefaultWidget(checkbox)
qconnect(checkbox.stateChanged, enable_disable_inktel)
menu.addAction(action)
mw.form.menuTools.addMenu(menu)

# start drawing every time the user studies.
gui_hooks.webview_will_set_content.append(on_webview_will_set_content)
