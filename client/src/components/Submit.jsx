import { createUseStyles } from 'react-jss';
import axios from 'axios'
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Button from '@mui/material/Button';

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
    },
})

const Submit = ({ changeStat, imagePath, polygonFrame, setResponse, inputsRef, submitRef, loaderRef, responseRef }) => {

    const css = useStyles();

    const theme = createTheme({
        palette: {
            primary: {
                main: '#2E7D32',
                contrastText: '#fff',
            }
        },
    });

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

    return <>
        <div ref={submitRef}>
            <ThemeProvider theme={theme}>
                <div onClick={changeStat}>
                    <Button variant="contained" onClick={(e) => handleClick(e)} className={css.submit}>Send to censor</Button>
                </div>
            </ThemeProvider>
        </div>
        <div className={css.loader} ref={loaderRef}></div>
    </>
}

export default Submit;
