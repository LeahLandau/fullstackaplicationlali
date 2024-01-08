import { useContext, useEffect, useState } from "react"
import ImgContext from "../context/ImageReduction"

const ReducedImage=()=>{
    const {imagePath}=useContext(ImgContext)

    const [url,setUrl]=useState('')

    useEffect(()=>{
        // const paths = imagePath //need fix it? cat? split??
        //maybe ? const path = paths.split('/').slice(3?(example without:"/share/vistorage?/")).join('/')
        // const response = axios.get('http://localhost:5000/api/get_url_by_path', path);
        // response={data:"https://storagefromvi.file.core.windows.net/vistorage/ofakim-test/OC2_0016483137/OC2_0016483137.R1.jpeg?se=2024-01-05T08%3A28%3A58Z&sp=r&sv=2019-02-02&sr=f&sig=ZwhTGbmoF7b08hbHBI6RO4eFk5WXTkSJPWvNxEyNEA8%3D"}
        // setUrl(response.data)
       
        // setUrl("https://storagefromvi.file.core.windows.net/vistorage/ofakim-test/OC2_0016483137/OC2_0016483137.R1.jpeg?se=2024-01-05T09%3A02%3A03Z&sp=r&sv=2019-02-02&sr=f&sig=9bdudCFHSLbp795JKUnTvPUYarufEvHfhwPdZTSWT/w%3D" )
    },[])

    return<>
    <img src={url} alt=""  width={800} />
    </>
}

export default ReducedImage