import axios from 'axios'
import { createUseStyles } from 'react-jss';
import { useContext } from 'react';
import ImgContext from '../context/ImageReduction';
import { ServerConfig } from '../configs/server';

const useStyles = createUseStyles({
    loader: {
        display: 'none',
        border: '10px solid gray',
        borderTop: '10px solid black',
        borderRadius: '50%',
        width: '50px',
        height: '50px',
        animation: '$spin 2s linear infinite',
        position: "fixed",
        top: "45%",
        left: "46%",
        transform: "translate(-50%, -50%)",
    },
    '@keyframes spin': {
        '0%': { transform: 'rotate(0deg)' },
        '100%': { transform: 'rotate(360deg)' },
    }
})

const Submit = () => {

    const css = useStyles();

    const { imagePath, setImagePath, polygonFrame, setResponse, inputsRef, submitRef, loaderRef, responseRef } = useContext(ImgContext);
    const handleClick = async (e) => {
        e.preventDefault()
        const imageDetails = { imagePath, polygonFrame }
        inputsRef.current.style.display = 'none'
        submitRef.current.style.display = 'none'
        loaderRef.current.style.display = 'block'
        const response = await axios.post(`${ServerConfig.PATH}/blackening_pixels`, imageDetails)
        setTimeout(() => {
            loaderRef.current.style.display = 'none'
            responseRef.current.style.display = 'block'
        }, 1000);
        setResponse(response.data)
    }
    const backClick = (e) => {
        setImagePath(null)
    }

    return <>
        <div ref={submitRef}>
            <button onClick={(e) => handleClick(e)}> Send to censor </button>
            <button onClick={(e) => backClick(e)}> back </button>
        </div>
        <div className={css.loader} ref={loaderRef}></div>
    </>
}

export default Submit;