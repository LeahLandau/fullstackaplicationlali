import { useRef, useEffect, useState, useContext } from "react"
import ImgContext from "../context/ImageReduction";

const Canvas = () => {
    const { setPolygonFrame,inputsRef,imagePath } = useContext(ImgContext);
    const canvasRef = useRef(null);
    const [img, setImg] = useState(null);
    const [isDrawing, setIsDrawing] = useState(false);
    const [lastPoint, setLastPoint] = useState([]);

    useEffect(() => {
        const canvas = canvasRef.current;
        const context = canvas.getContext("2d");
        const uploadedImage = new Image();
        // just to run now:
        const urlImage = "https://storagefromvi.file.core.windows.net/vistorage/ofakim-test/OC2_0016483137/OC2_0016483137.R1.jpeg?se=2024-01-05T08%3A28%3A58Z&sp=r&sv=2019-02-02&sr=f&sig=ZwhTGbmoF7b08hbHBI6RO4eFk5WXTkSJPWvNxEyNEA8%3D"
        uploadedImage.src = urlImage;
        
        setImg(uploadedImage);
        context.clearRect(0, 0, canvas.width, canvas.height);
        context.drawImage(uploadedImage, 0, 0, uploadedImage.width, uploadedImage.height);
        setLastPoint([]);
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
            <h4>display image with path "{imagePath?imagePath.split(".")[0]:''}.R1.jpeg" :</h4>
            <h4>the correct path is "{imagePath}" :</h4>
            <canvas ref={canvasRef} id="canvas"
                // width={img ? (img.width) : 200} height={img ? (img.height) : 200}
                onMouseDown={startDrawing} onMouseMove={draw} onMouseUp={stopDrawing} onMouseOut={stopDrawing} />
        </div>
    </>
}

export default Canvas;