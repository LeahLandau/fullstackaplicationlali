import { createUseStyles } from 'react-jss';
import React, { useState } from 'react';
import Alert from '@mui/material/Alert';
import Button from '@mui/material/Button';
import axios from 'axios';

import ReducedImage from './ReducedImage';
import { ServerConfig } from '../configs/server';


const useStyles = createUseStyles({
  response: {
    display: 'none',
    marginTop: '50px',
  },
});

const Response = ({ response, responseRef, imagePath }) => {

  const css = useStyles();

  const [showNewComponent, setShowNewComponent] = useState(false);
  const [url, setUrl] = useState(null);


  const handleClick = () => {
    const convert = async () => {
      const paths = {
        file_path_jp2: imagePath,
        file_path_jpeg: '/images/jpeg/display.jpeg'
      };
      const response = await axios.post(`${ServerConfig.PATH}/convert_jp2_to_jpeg`, paths);
      setUrl(response.data);
    };
    convert();
    setShowNewComponent(true);

  };

  const onclose = () => {
    responseRef.current.style.display = 'none';
    window.location.reload();
  };

  return <>
    <div className={css.response} ref={responseRef}>
      <Button onClick={onclose}>x</Button>
      {response !== 'The image has been blackened successfully' ? <Alert severity='success' action={<Button onClick={() => { handleClick(); }}>display</Button>}>{response}</Alert> : <Alert severity='error'>{response}</Alert>}
      {showNewComponent && <ReducedImage url={url} />}
    </div>
  </>;
};

export default Response;
