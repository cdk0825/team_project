// 로컬에서 API 환경 세팅 테스트
import express from 'express'
import userRouter from './routes/user.js'

const app = express();
const PORT = 5000;

// express 서버에서 들어오는 요청의 json데이터 읽을수 있게 설정
// 미들웨어 모든 요청에 적용
app.use(express.json());
app.use('/api/users', userRouter);


app.get('/', (req, res) =>{
    res.send('HI~~~')
});

app.get('/api/data', (req, res) => {
    res.send('data!!!')
});

app.post('/api/po', (req, res) => {
    // api 테스트 하는 곳 body에 json 값입력 하지 않고 사용하려면 아래와 같이 명시
    req.body = {
      name: "Alice",
      age: 15
    };
    const {name, age} = req.body;
    res.json({
        message: 'POST 성공',
        name,
        age
    });
});

// url 파아미터 & 쿼리 사용
// http://localhost:5000/api/user/123
app.get('/api/user/:id', (req, res) => {
    res.json({userId: req.params.id});
});

// Query String
// http://localhost:5000/search?keyword=node&page=1
app.get('/search', (req, res) => {
    res.json(req.query);
});

// error 처리
// http://localhost:5000/error
app.get('/error', (req, res) => {
    res.status(400).json({error: '잘못된 요청'});
});

// 가짜 DB테스트
const users = []
app.post('/users', (req, res) => {
    // api 테스트 하는 곳 body에 json 값입력 하지 않고 사용하려면 아래와 같이 명시
    req.body = {
      name: "Alice",
      age: 15
    };
    users.push(req.body);
    res.status(201).json(users);
});
app.get('/users', (req, res) => {
    res.json(users);
});

app.listen(PORT, () => {
    console.log(`server running on http://localhost:${PORT}`)
})