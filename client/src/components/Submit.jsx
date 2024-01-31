import { createUseStyles } from 'react-jss';
import { useState } from 'react';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Button from '@mui/material/Button';
import axios from 'axios';

import { ServerConfig } from '../configs/server';
import Error from './Error';


const useStyles = createUseStyles({
  loader: {
    display: 'none',
    border: '10px solid gray',
    borderTop: '10px solid black',
    borderRadius: '50%',
    width: '50px',
    height: '50px',
    animation: '$spin 2s linear infinite',
    position: 'fixed',
    top: '45%',
    left: '46%',
    transform: 'translate(-50%, -50%)',
  },
  '@keyframes spin': {
    '0%': { transform: 'rotate(0deg)' },
    '100%': { transform: 'rotate(360deg)' },
  },
});

const Submit = ({ changeState, imagePath, polygonFrame, setResponse, inputsRef, submitRef, loaderRef, responseRef }) => {

  const css = useStyles();

  const [isError, setIsError] = useState(false);
  const [error, setError] = useState('');

  const theme = createTheme({
    palette: {
      primary: {
        main: '#2E7D32',
        contrastText: '#fff',
      }
    },
  });

  const handleClick = async (e) => {
    e.preventDefault();
    const imageDetails = { imagePath, polygonFrame: JSON.stringify(polygonFrame) };
    inputsRef.current.style.display = 'none';
    submitRef.current.style.display = 'none';
    loaderRef.current.style.display = 'block';
    try {
      const response = await axios.post(`${ServerConfig.PATH}/blackening_pixels`, imageDetails);
      setTimeout(() => {
        loaderRef.current.style.display = 'none';
        responseRef.current.style.display = 'block';
      }, 1000);
      setResponse(response.data);
    } catch (error) {
      const parser = new DOMParser();
      const doc = parser.parseFromString(error.response.data, 'text/html');
      setError(doc.querySelector('p').textContent);
      setIsError(true);
    }
  };

  return <>
    {!isError ? (
      <div>
        <div ref={submitRef}>
          <ThemeProvider theme={theme}>
            <div onClick={changeState}>
              <Button variant='contained' onClick={(e) => handleClick(e)} className={css.submit}>Submit</Button>
            </div>
          </ThemeProvider>
        </div>
        <div className={css.loader} ref={loaderRef}></div>
      </div>) : <Error response={`${error}`}></Error>
    }

  </>;
};

export default Submit;
