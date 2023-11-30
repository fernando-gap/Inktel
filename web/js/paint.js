class StrategyPaint {
    constructor() {
        this.last_point = {
            x: null,
            y: null,
        }
    }

    start(clientX, clientY, ctx) {
        if (this.last_point.x === null) {
            this.last_point = {
                x: clientX,
                y: clientY,
            }
        } else {
            ctx.beginPath()
            ctx.moveTo(this.last_point.x, this.last_point.y)
            ctx.lineTo(clientX, clientY)
            ctx.stroke()
            this.last_point = {
                x: clientX,
                y: clientY,
            }
        }
    }

    draw(event, canvas) {
        if (canvas.isMouseDown) {
            this.start(event.clientX, event.clientY, canvas._ctx)
        } else {
            this.last_point = {
                x: null, 
                y: null,
            }
        }
    }
}
