
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
import { useQuery } from '@tanstack/react-query'
import './Home.css'

const getCategories = async () => {
    const response = await fetch('http://localhost:7611/category/?offset=0&limit=100')
    return await response.json()
}

function Home() {
    const {data, isPending } = useQuery({
        queryKey: [ 'categories'],
        queryFn: getCategories,
        retry: 0
    })
            
    return (<div className="Home">
        <Container>
            <Typography variant="h2">カテゴリ・日付で検索</Typography>
        </Container>
        
        <h2>hello</h2>
        <div>
            {isPending ? 'Pending ...' : JSON.stringify(data)}
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
                <Typography variant="h4">Category</Typography>
                <List className="CategoryList">
                    <ListItem><Typography variant="h5">物理学科</Typography></ListItem>
                    <ListItem><Typography variant="h5">河野研究室</Typography></ListItem>
                </List>
            </Grid>
            <Grid size={5}>
                <Typography variant="h4">Date</Typography>
                <Grid container>
                    <Grid size={6}>
                        <Typography variant="h5">日付（検索開始）</Typography>
                    </Grid>
                    <Grid size={6}>
                        <TextField defaultValue="2026-05-06"></TextField>
                    </Grid>
                    <Grid size={6}>
                        <Typography variant="h5">日付（検索終了）</Typography>
                    </Grid>
                    <Grid size={6}>
                        <TextField defaultValue="2026-05-06"></TextField>
                    </Grid>
                </Grid>
            </Grid>
            <Grid size={2}>
                <Button variant="outlined">検索</Button>
            </Grid>
        </Grid>
    </div>)
}

export default Home
