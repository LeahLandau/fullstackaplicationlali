import { createUseStyles } from 'react-jss';
import { useContext } from 'react';

import ImgContext from '../context/ImageReduction';
import ReducedImage from './ReducedImage';

const useStyles = createUseStyles({
    response: {
        display: 'none',
        position: "fixed",
        top: "50%",
        left: "50%",
        transform: "translate(-50%, -50%)",
    }
})

const Response = () => {

    const css = useStyles();

    const { response, responseRef } = useContext(ImgContext);

    return <>
        <div className={css.response} ref={responseRef}>
            <h1>
                {response}
            </h1>
            <ReducedImage></ReducedImage>
        </div>
    </>
}

export default Response;