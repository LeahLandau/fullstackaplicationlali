import { useState, useRef } from 'react';
import { createUseStyles } from 'react-jss';

import ImgContext from '../context/ImageReduction'
import Canvas from './canvas';
import Submit from './Submit'
import Response from './Response'
import SelectionImage from './selectionImage';

const useStyles = createUseStyles({
    wrraper: {
        textAlign: 'center'
    }
})

const ImageReduction = () => {

    const css = useStyles();

    const [imagePath, setImagePath] = useState(null)
    const [polygonFrame, setPolygonFrame] = useState([])
    const [response, setResponse] = useState('')

    const inputsRef = useRef(null);
    const submitRef = useRef(null);
    const responseRef = useRef(null);
    const loaderRef = useRef(null);

    return<>
        <div className={css.wrraper}>
            <ImgContext.Provider value={{imagePath, setImagePath,polygonFrame, setPolygonFrame, response, setResponse, inputsRef, submitRef, responseRef, loaderRef}}>
                {
                    !imagePath ? (
                        <div>
                            <SelectionImage></SelectionImage>
                        </div>
                    ) : (
                        <div>
                            <Canvas></Canvas>
                            <Submit></Submit>
                            <Response></Response>
                        </div>
                    )
                }
            </ImgContext.Provider>
        </div>
    </>
}

export default ImageReduction;