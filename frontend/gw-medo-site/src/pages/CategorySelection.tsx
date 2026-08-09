import * as React from 'react'
import Container from '@mui/material/Container'
import Typography from '@mui/material/Typography'
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import FormControl from '@mui/material/FormControl'
import FormLabel from '@mui/material/FormLabel'
import FormControlLabel from '@mui/material/FormControlLabel'
import RadioGroup from '@mui/material/RadioGroup'
import Radio from '@mui/material/Radio'
import List from '@mui/material/List'
import ListItem from '@mui/material/ListItem'

function CategorySelection({categories, handleCategory}) {
    const id = React.useId()

    return (
        <Container>
            <Typography variant="h4">カテゴリ</Typography>
            <FormControl>
                <FormLabel  id={`${id}-label`}>Categories</FormLabel>
                <RadioGroup
                    aria-labelledby={`${id}-label`}
                    name="controlled-radio-buttons-group"
                    onChange={handleCategory}>
                    {categories.map( (category) => (
                        <FormControlLabel value={category['name']} control={<Radio />} label={category['name']} />
                    ))}
                </RadioGroup>
            </FormControl>
        </Container>
    );
}

export default CategorySelection
