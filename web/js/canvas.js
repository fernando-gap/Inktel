class ContextCanvas {
    constructor() {
        this._id = "inktel"
        this._canvas = document.getElementById(this._id)

        if (this._canvas.getContext) {
            this._ctx = this._canvas.getContext("2d")
        } else {
            throw new Error("Canvas Unsupported")
        }

        window.addEventListener("resize", () => {
            this._canvas.width = window.innerWidth;
            this._canvas.height = window.innerHeight;
        });

        this.isMouseDown = false;

        this._mousedown()
        this._mouseup()
    }

    set strategy(newStrategy) {
        this._currentStrategy = newStrategy
    }

    _mouseup() {
        window.addEventListener("mouseup", (e) => {
            this.isMouseDown = false;
        })
    }

    _mousedown() {
        window.addEventListener("mousedown", (e) => {
            this.isMouseDown = true;
        })
    }

    draw() {
        window.addEventListener("mousemove", (e) => {
            if (this._currentStrategy !== undefined) {
                const canvasRect = this._canvas.getBoundingClientRect();

                /* All strategies must be relative to the viewport */
                const mouse_event = {
                    clientX: e.clientX - canvasRect.left,
                    clientY: e.clientY - canvasRect.top,
                    event: e,
                }

                this._currentStrategy.draw(mouse_event, this)
            }
        })
    }

    save() {
        this._ctx.save()
    }

    restore() {
        this._ctx.restore()
    }

    clear() {
        this._ctx.clearRect(0, 0, this._canvas.height, this._canvas.width)
    }
}