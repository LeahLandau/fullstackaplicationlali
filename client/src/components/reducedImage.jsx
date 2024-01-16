import { useContext, useEffect, useState } from "react"
import ImgContext from "../context/ImageReduction"

const ReducedImage=()=>{
    const {imagePath}=useContext(ImgContext)

    const [url,setUrl]=useState('')

    useEffect(()=>{
        setUrl(imagePath);
    }, [imagePath]);

    return<>
    <img src={url} alt="" width={150} height={150} />
    </>
}

export default ReducedImage