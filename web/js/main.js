
window.addEventListener("load", () => {
    const canvas = new ContextCanvas()
    canvas.strategy = new StrategyPaint();

    const buttons = document.getElementsByClassName("inktel-item")
    let current_button = null;
    for (const button of buttons) {
        button.addEventListener("click", (e) => {
            if (current_button === null) {
                current_button = button;
            } else {
                current_button.classList.remove("inktel-clicked");
                current_button = button;
            }
            
            current_button.classList.add("inktel-clicked")
        })
    }
    canvas.draw()
})
