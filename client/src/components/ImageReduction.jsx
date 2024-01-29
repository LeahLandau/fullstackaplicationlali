import { useState, useRef, useCallback } from 'react';
import * as React from 'react';
import { createUseStyles } from 'react-jss';
import axios from 'axios';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import { createTheme, ThemeProvider } from '@mui/material/styles';

import Canvas from './Canvas';
import Submit from './Submit';
import Response from './Response';
import SelectionImage from './SelectionImage';
import { ServerConfig } from '../configs/server';


const useStyles = createUseStyles({
  wrraper: {
    textAlign: 'center',
    margin: '100px'
  },
  selectImage: {
    pointerEvents: 'painted'
  }
});

const ImageReduction = () => {

  const css = useStyles();

  const [imagePath, setImagePath] = useState(null);
  const [polygonFrame, setPolygonFrame] = useState([]);
  const [response, setResponse] = useState('');
  const [open, setOpen] = useState(false);
  const [showButton, setShowButton] = useState(true);
  const [showNewComponent, setShowNewComponent] = useState(false);
  const [isImages, setIsImages] = useState(false);
  const [jpegImagePath, setjpegImagePath] = useState(null);


  const inputsRef = useRef(null);
  const submitRef = useRef(null);
  const responseRef = useRef(null);
  const loaderRef = useRef(null);

  const changeStat = useCallback(() => {
    setShowButton(false);
  }, []);

  const theme = createTheme({
    palette: {
      primary: {
        main: '#2E7D32',
        contrastText: '#fff',
      }
    },
  });

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleClick = async () => {
    const paths = {
      file_path_jp2: imagePath,
      file_path_jpeg: '/images/jpeg/convert.jpeg'
    };
    const response = await axios.post(`${ServerConfig.PATH}/convert_jp2_to_jpeg`, paths);
    setjpegImagePath(response.data);
    setShowNewComponent(true);
  };

  return <>
    <div className={css.wrraper}>
      <React.Fragment>
        <ThemeProvider theme={theme}>
          {showButton === true ?
            <Button variant='contained' onClick={handleClickOpen} className={css.selectImage}>Select Images</Button>
            : ''}
        </ThemeProvider>
        <Dialog
          open={open}
          onClose={handleClose}
          aria-describedby='alert-dialog-description'>
          <DialogContent>
            <SelectionImage setImagePath={setImagePath} setIsImages={setIsImages}></SelectionImage>
          </DialogContent>
          <DialogActions>
            <div onClick={handleClose}>
              {
                isImages === true ?
                  <Button onClick={handleClick} variant='primary'>Select</Button> :
                  ''
              }
            </div>
          </DialogActions>
        </Dialog>
      </React.Fragment>
      <div>
        {showNewComponent && <Canvas jpegImagePath={jpegImagePath} setPolygonFrame={setPolygonFrame} inputsRef={inputsRef}></Canvas>}
        {showNewComponent && polygonFrame.length > 0 && <Submit changeStat={changeStat} imagePath={imagePath} polygonFrame={polygonFrame} setResponse={setResponse} inputsRef={inputsRef} submitRef={submitRef} loaderRef={loaderRef} responseRef={responseRef} />}
        {showNewComponent && <Response response={response} responseRef={responseRef} imagePath={imagePath} />}
      </div>
    </div>
  </>;
};

export default ImageReduction;
