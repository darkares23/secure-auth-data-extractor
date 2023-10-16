import React, { useState, ChangeEvent } from 'react';
import { Button, TextField, Container, Typography } from '@mui/material';
import { extractData } from '../api/apiServices';


const TextInputComponent = ( ) => {
  const [text, setText] = useState<string>('');
  const [result, setResult] = useState<string | null>(null);

  const handleTextChange = (event: ChangeEvent<HTMLInputElement>) => {
    setText(event.target.value);
  };

  const handleSubmit = async () => {
    console.log(text);
    try {
      const data = await extractData(text);
      console.log(data);
      setResult(JSON.stringify(data, null, 2));
    } catch (error) {
       console.error(error);
       setResult("Error al extraer datos.");
    }
  };

  return (
    <Container component="main" maxWidth="lg">
      <TextField
        style={{ backgroundColor: 'white' }}
        variant="outlined"
        margin="normal"
        required
        fullWidth
        id="text"
        label="text"
        multiline
        rows={15}
        value={text}
        onChange={handleTextChange}
      />
      <Button
        type="submit"
        fullWidth
        variant="contained"
        color="primary"
        onClick={handleSubmit}
      >
        Submit
      </Button>
      {result && (
        <Typography style={{ marginTop: '20px' }}>
          Resultado:
          <pre>{result}</pre>
        </Typography>
      )}
    </Container>
  );
}

export default TextInputComponent;
