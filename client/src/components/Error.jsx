import Alert from '@mui/material/Alert';

const Error = ({ response }) => {

  return <>
    <Alert severity='error'>{response}</Alert>
  </>;

};
export default Error;