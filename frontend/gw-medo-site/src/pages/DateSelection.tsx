import { useState } from 'react'
import Container from '@mui/material/Container'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import {useNavigate} from 'react-router-dom'

function dateString(date: Date): String {
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    const ds = `${year}-${month}-${day}`
    return ds
}
function DateSelection({category}) {
    const navigate = useNavigate()
    const [ startDate, setStartDate] = useState('')
    const [ endDate, setEndDate] = useState('')

    const setToday = () => {
        const now = new Date()
        const ds = dateString(now)
        setStartDate(ds)
        setEndDate(ds)
    }
    const setThisWeek = () => {
        const now = new Date()
        const year = now.getFullYear()
        const month = String(now.getMonth() + 1).padStart(2, '0')
        const day = now.getDay()
        if (day == 0) {
            day = 7
        }
        const diff1 = day - 1
        const diff2 = 7 - day
        const date1 = new Date()
        const date2 = new Date()
        date1.setDate(date1.getDate() - diff1)
        date2.setDate(date2.getDate() + diff2)
        const ds1 = dateString(date1)
        const ds2 = dateString(date2)
        setStartDate(ds1)
        setEndDate(ds2)
    }

    const handleStartDate = (event) => {
        setStartDate(event.target.value)
    }
    const handleEndDate = (event) => {
        setEndDate(event.target.value)
    }
    const handleSearch = () => {
        navigate("/eventlist", 
            {state: {categoryId: 1, startDate: startDate, endDate: endDate}})
    }

    return (
        <Container >
            <Typography variant="h4">日付の範囲</Typography>
            <Stack direction="column" spacing={2}>
                <Stack direction="row" spacing={1}>
                    <TextField label="Start date" variant="standard" value={startDate} onChange={handleStartDate}/>
                    <Typography variant="h5">ー</Typography>
                    <TextField label="End date" variant="standard" value={endDate} onChange={handleEndDate} />
                </Stack>
                <Stack direction="row" spacing={1}>
                    <Button variant="outlined" onClick={setToday}>今日</Button>
                    <Button variant="outlined" onClick={setThisWeek}>今週</Button>
                    <Button variant="outlined">前後1ヶ月</Button>
                    <Button variant="contained" onClick={handleSearch}>検索</Button>
                </Stack>
            </Stack>
        </Container>
    )
}

export default DateSelection
