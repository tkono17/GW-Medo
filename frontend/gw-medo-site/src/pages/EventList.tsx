import TextField from '@mui/material/TextField'
import Typography from '@mui/material/Typography'
import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'
import Grid from '@mui/material/Grid'
import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'
import CardActionArea from '@mui/material/CardActionArea'
import { useId, useState } from 'react'
import { useLocation } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import './EventList.css'

const getEvents = async (category_id: int, start_date: str, end_date: str) => {
    const response = await fetch('http://localhost:7611/eventSession/?offset=0&limit=100')
    return await response.json()
}

function Event({name, date, startTime, endTime}) {
    return (<Card sx={{p: 1}}>
        <CardContent  sx={{ height: '100%', m: 1 }}  mx={{ height: '100%' }}>
            <CardActionArea>
                <Grid container>
                    <Grid size={2}>
                        <Typography variant="h6">{date}</Typography>
                    </Grid>
                    <Grid size={2}>                            <Typography variant="h6">{startTime} - {endTime}</Typography>
                    </Grid>
                    <Grid size={5}>
                        <Typography variant="h5">{name}</Typography>
                    </Grid>
                </Grid>
            </CardActionArea>
        </CardContent>
    </Card>)
}

function EventList() {
    const location = useLocation()
    const params = location.state

    const categoryId = location.state.categoryId
    const startDate = location.state.startDate
    const endDate = location.state.endDate

    const [events, setEvents] = useState([])
    const { data: eventsData, isPending } = useQuery({
        queryKey: ['eventlist', categoryId, startDate, endDate],
        queryFn: () => getEvents(categoryId, startDate, endDate),
        retry: 0
    })
    //isPending ? setEvents([]) : setEvents(eventsData)
    //console.log(events)

    return (<div>
        <Box>
            <Typography variant="h2">イベントの一覧</Typography>
        </Box>
        <Stack direction="row">
            <Typography variant="h5">Category: {params.category}</Typography>, 
            <Typography variant="h5">,   Date: {params.startDate} - {params.endDate}</Typography>
        </Stack>
    </div>)
}

export default EventList
