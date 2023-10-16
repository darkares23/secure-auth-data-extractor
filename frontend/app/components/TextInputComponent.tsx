import React, { useState, ChangeEvent } from 'react';
import { Button, TextField, Container, Typography } from '@mui/material';
import { extractData } from '../api/apiServices';

interface TextInputComponentProps {
    email: string;
}

const TextInputComponent: React.FC<TextInputComponentProps> = ({ email }) => {
  const [text, setText] = useState<string>('');
  const [result, setResult] = useState<string | null>(null);

  const handleTextChange = (event: ChangeEvent<HTMLInputElement>) => {
    setText(event.target.value);
  };

  const handleClear = () => {
    setText('');
  };

  const handleSubmit = async () => {
    try {
      const data = await extractData(text, email);
      setResult(JSON.stringify(data, null, 2));
    } catch (error) {
       console.error(error);
       setResult("Data extracted failed, review the format of the text");
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
      <Button
        fullWidth
        variant="contained"
        color="secondary"
        onClick={handleClear}
      >
        Clear
      </Button>
      {result && (
        <Typography style={{ marginTop: '20px' }}>
          Result:
          <pre>{result}</pre>
        </Typography>
      )}
    </Container>
  );
}

export default TextInputComponent;