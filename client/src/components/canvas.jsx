import axios from "axios";
import { useRef, useEffect, useState, useContext } from "react"
import { ServerConfig } from "../configs/server";
import ImgContext from "../context/ImageReduction";

const Canvas = () => {
    const { setPolygonFrame,inputsRef,imagePath } = useContext(ImgContext);
    const canvasRef = useRef(null);
    const [isDrawing, setIsDrawing] = useState(false);
    const [lastPoint, setLastPoint] = useState([]);
    const [src, setSrc] = useState("")

    useEffect(() => {
        const canvas = canvasRef.current;
        const context = canvas.getContext("2d");
        const loadImage = () => {
            const imgOnCanvas = new Image();
            imgOnCanvas.onload = () => {
                context.drawImage(imgOnCanvas, 0, 0, canvas.width, canvas.height);
            };
            imgOnCanvas.src = src;
        };
        if (src) {
            loadImage();
            setLastPoint([]);
        }
    }, [src]);

    useEffect(() => {
        axios.get(`${ServerConfig.PATH}/get_url_by_path?path=${imagePath}`).then((response) => {
            setSrc(response.data);
        })
    }, [imagePath]);

    const startDrawing = (e) => {
        setIsDrawing(true);
        const canvas = canvasRef.current;
        const context = canvas.getContext("2d");
        context.beginPath();
        context.moveTo(e.nativeEvent.offsetX, e.nativeEvent.offsetY);
        setLastPoint([e.nativeEvent.offsetX, e.nativeEvent.offsetY]);
    };

    const draw = (e) => {
        if (imagePath) {
            if (!isDrawing) return;
            const canvas = canvasRef.current;
            const context = canvas.getContext("2d");
            setLastPoint([e.nativeEvent.offsetX, e.nativeEvent.offsetY]);
            context.lineTo(e.nativeEvent.offsetX, e.nativeEvent.offsetY);
            context.stroke();
            setPolygonFrame((prevPoints) => [...prevPoints, lastPoint]);
        }
    };

    const stopDrawing = () => {
        setIsDrawing(false);
    };

    return <>
        <div ref={inputsRef}>
            <canvas ref={canvasRef} id="canvas" src={src}
                onMouseDown={startDrawing} onMouseMove={draw} onMouseUp={stopDrawing} onMouseOut={stopDrawing} />
        </div>
    </>
}

export default Canvas;