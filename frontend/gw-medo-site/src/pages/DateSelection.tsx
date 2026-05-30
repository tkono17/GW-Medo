import { useState } from 'react'
import Container from '@mui/material/Container'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import {useNavigate} from 'react-router-dom'

function DateSelection({}) {
    const [ category, setCategory] = useState<String|null>(null)
    const [ startDate, setStartDate] = useState<String|null>(null)
    const [ endDate, setEndDate] = useState<String|null>(null)
    const navigate = useNavigate()

    return (
        <Container >
            <Typography variant="h4">日付の範囲</Typography>
            <Stack direction="column" spacing={2}>
                <Stack direction="row" spacing={1}>
                    <TextField label="Start date" variant="standard" />
                    <Typography variant="h5">ー</Typography>
                    <TextField label="End date" variant="standard" />
                </Stack>
                <Stack direction="row" spacing={1}>
                    <Button variant="outlined">今日</Button>
                    <Button variant="outlined">今週</Button>
                    <Button variant="outlined">前後1ヶ月</Button>
                    <Button variant="contained" onClick={() => navigate("/eventlist", { viewTransition: true })}>検索</Button>
                </Stack>
            </Stack>
        </Container>
    )
}

export default DateSelection
