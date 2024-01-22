import { useRef, useEffect, useState } from "react"
import { createUseStyles } from 'react-jss'


const useStyles = createUseStyles({
    borderCanvas: {
        border: '2px solid black',
        borderRadius: '10px',
        marginBottom: '10px',
        marginTop: '10px',
        width: '90vw',
        height: '55vh',
        overflow: 'auto',
    }
});

const Canvas = ({ setPolygonFrame, inputsRef, imagePath }) => {

    const css = useStyles();

    const canvasRef = useRef(null);

    const [isDrawing, setIsDrawing] = useState(false);
    const [lastPoint, setLastPoint] = useState([]);
    const [img, setImg] = useState("");

    useEffect(() => {
        
        const createImage = () => {
            const imgOnCanvas = new Image();
            imgOnCanvas.onload = () => {
                const canvas = canvasRef.current;
                const context = canvas.getContext("2d");
                canvas.width = imgOnCanvas.width;
                canvas.height = imgOnCanvas.height;
                context.drawImage(imgOnCanvas, 0, 0, imgOnCanvas.width, imgOnCanvas.height);
            };
            imgOnCanvas.src = imagePath;
            setImg(imgOnCanvas);
        };

        if (imagePath) {
            createImage();
            setPolygonFrame([])
        }
    }, [imagePath, setPolygonFrame]);

    const startDrawing = (e) => {
        setIsDrawing(true);
        const { offsetX, offsetY } = e.nativeEvent;
        const canvas = canvasRef.current;
        const context = canvas.getContext("2d");
        context.beginPath();
        context.arc(offsetX, offsetY, 3, 0, 2 * Math.PI);
        context.moveTo(offsetX, offsetY);
        context.arc(lastPoint[0], lastPoint[1], 3, 0, 2 * Math.PI);
        context.stroke();
        context.fillStyle = "black";
        context.fill();
        setLastPoint([offsetX, offsetY]);
    };

    const draw = (e) => {
        if (!isDrawing) return;
        const canvas = canvasRef.current;
        const context = canvas.getContext("2d");
        const { offsetX, offsetY } = e.nativeEvent;
        if (lastPoint.length > 0) {
            context.beginPath();
            context.moveTo(lastPoint[0], lastPoint[1]);
            context.lineTo(offsetX, offsetY);
            context.stroke();
        }
        setLastPoint([offsetX, offsetY]);
        setPolygonFrame((prevPoints) => [...prevPoints, [offsetX, offsetY]]);
    };

    const stopDrawing = (e) => {
        setIsDrawing(false);
        const { offsetX, offsetY } = e.nativeEvent;
        setPolygonFrame((prevPoints) => [...prevPoints, [offsetX, offsetY]]);
    };

    useEffect(() => {
        if (img) {
            const canvas = canvasRef.current;
            const context = canvas.getContext("2d");
            context.clearRect(0, 0, canvas.width, canvas.height);
            context.drawImage(img, 0, 0);
        }
    }, [img]);

    return <>
        <div ref={inputsRef} className={css.borderCanvas}>
            <canvas ref={canvasRef} id="canvas"
                onMouseDown={startDrawing} onMouseMove={draw} onMouseUp={stopDrawing} />
        </div>
    </>
};

export default Canvas;