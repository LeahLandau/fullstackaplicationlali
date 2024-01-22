import { createUseStyles } from 'react-jss';
import React, { useState } from 'react';
import Alert from '@mui/material/Alert';
import Button from '@mui/material/Button';

import ImageReduction from './ImageReduction';
import ReducedImage from './ReducedImage';


const useStyles = createUseStyles({
    response: {
        display: 'none',
        marginTop: '50px',
    },
})

const Response = ({ response, responseRef, imagePath }) => {

    const css = useStyles();

    const [showNewComponent, setShowNewComponent] = useState(false);
    const [showComponent, setShowComponent] = useState(false);

    const handleClick = () => {
        setShowNewComponent(true);
    };

    const onclose = () => {
        setShowComponent(true)
        responseRef.current.style.display = 'none'
    }

    return <>
        <div className={css.response} ref={responseRef}>
            <Button onClick={onclose}>x</Button>
            {{ response } !== 'The image has been blackened successfully' ? <Alert severity='success' action={<Button onClick={() => { handleClick(); }}>display</Button>}>{response}</Alert> : <Alert severity='error'>{response}</Alert>}
            {showNewComponent && <ReducedImage />}
        </div>
        {showComponent && <ImageReduction imagePath={imagePath} />}
    </>
}

export default Response;
