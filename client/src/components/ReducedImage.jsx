import { useEffect, useState } from "react"


const ReducedImage = ({ imagePath }) => {

    const [url, setUrl] = useState('')

    useEffect(() => {
        setUrl(imagePath);
    }, [imagePath]);

    return <>
        <img src={url} alt="" width={150} height={150} />
    </>
}

export default ReducedImage