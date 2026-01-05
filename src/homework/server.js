// 로컬에서 API 환경 세팅 테스트
import express from 'express'

const app = express();
const PORT = 5000;

app.get('/', (req, res) =>{
    res.send('HI~~~')
});

app.get('/api/data', (req, res) => {
    res.send('data!!!')
});

app.post('/api/po', (req, res) => {
    res.send('data!!!')
});

app.listen(PORT, () => {
    console.log(`server running on http://localhost:${PORT}`)
})