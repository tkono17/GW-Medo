import TextField from '@mui/material/TextField'
import Typography from '@mui/material/Typography'
import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'
import Grid from '@mui/material/Grid'
import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'
import CardActionArea from '@mui/material/CardActionArea'
import './EventList.css'

function EventList() {
    return (<div>
        <Box>
            <Typography variant="h2">イベントの一覧</Typography>
        </Box>

        <Box       sx={{
        width: '100%',
        display: 'grid',
        gridTemplateColumns: 'repeat(600px)',
        gap: 2,
      }}
            mx={{
        width: '100%',
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(min(200px, 100%), 1fr))',
        gap: 2,
      }}>
            <Card sx={{p: 1}}>
                <CardContent  sx={{ height: '100%', m: 1 }}  mx={{ height: '100%' }}>
                    <CardActionArea>
                        <Grid container>
                            <Grid size={2}>
                                <Typography variant="h6">2026-05-06</Typography>
                            </Grid>
                            <Grid size={2}>
                                <Typography variant="h6">13:30 - 15:00</Typography>
                            </Grid>
                            <Grid size={5}>
                                <Typography variant="h5">B4演習</Typography>
                            </Grid>
                        </Grid>
                    </CardActionArea>
                </CardContent>
            </Card>
            <Grid container sx = {{ borderRadius: 2, p: 1}} className="EventItem">
                <Grid size={2}>
                    <Typography variant="h6">2026-05-06</Typography>
                </Grid>
                <Grid size={2}>
                    <Typography variant="h6">15:00 - 17:00</Typography>
                </Grid>
                <Grid size={5}>
                    <Typography variant="h5">研究室ミーティング</Typography>
                </Grid>
            </Grid>
        </Box>
    </div>)
}

export default EventList
