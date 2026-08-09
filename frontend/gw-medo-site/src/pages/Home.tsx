
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography'
import Grid from '@mui/material/Grid'
import Container from '@mui/material/Container'
import List from '@mui/material/List'
import ListItem from '@mui/material/ListItem'

import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';
import { useState, ChangeEvent } from 'react'
import { useQuery } from '@tanstack/react-query'

import './Home.css'
import CategorySelection from './CategorySelection';
import DateSelection from './DateSelection';

const getCategories = async () => {
    const response = await fetch('http://localhost:7611/category/?offset=0&limit=100')
    return await response.json()
}

function Home() {
    const {data: categoriesData, isPending } = useQuery({
        queryKey: [ 'categories'],
        queryFn: getCategories,
        retry: 0
    })
    const [ category, setCategory] = useState('?')

    const handleCategory = (event) => {
        setCategory(event.target.value)
    }

    var categories = []
    { isPending ? categories =[] : categories = categoriesData }
    
    return (<div className="Home">
        <Container>
            <Typography variant="h2">カテゴリ・日付で検索</Typography>
        </Container>
        
        <div>
            {isPending ? 'Pending ...' : JSON.stringify(categories)}
        </div>

        <Grid container sx={{
            justifyContent: "center",
            alignItems: "center",
            }}
            mx={{
            justifyContent: "center",
            alignItems: "center",
            }}>
            <Grid size={5} sx={{ p: 5 }}>
                <CategorySelection categories={categories} handleCategory={handleCategory} />
            </Grid>
            <Grid size={6}>
                <DateSelection category={category} />
            </Grid>
        </Grid>
    </div>)
}

export default Home
