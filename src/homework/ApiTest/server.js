// 로컬에서 API 환경 세팅 테스트
import express from 'express'
import userRouter from './routes/user.js'
import { db } from './db.js';

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
// const users = []
// app.post('/users', (req, res) => {
//     // api 테스트 하는 곳 body에 json 값입력 하지 않고 사용하려면 아래와 같이 명시
//     req.body = {
//       name: "Alice",
//       age: 15
//     };
//     users.push(req.body);
//     res.status(201).json(users);
// });
// app.get('/users', (req, res) => {
//     res.json(users);
// });

app.get('/ping', async (req, res) => {
  try {
    const [rows] = await db.query('SELECT 1 AS result');
    res.json(rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'DB error' });
  }
});

/**
 * 회원 전체 조회 (SELECT)
 */
app.get('/users', async (req, res) => {
  const [rows] = await db.query('SELECT * FROM users');
  res.json(rows);
});

/**
 * 특정 유저 조회 (SELECT by id)
 * GET /users/:id
 */
app.get('/users/:id', async (req, res) => {
  const { id } = req.params;

  const [rows] = await db.query('SELECT * FROM users WHERE id = ?', [id]);

  // 유저가 없는 경우
  if (rows.length === 0) {
    return res.status(404).json({ message: '유저 없음' });
  }

  // 있는 경우
  res.json(rows[0]);
});

/**
 * 회원가입 (INSERT)
 * body: { "username": "abc", "password": "1234" }
 */
app.post('/users', async (req, res) => {
  const { username, password } = req.body;

  await db.query('INSERT INTO users (username, password) VALUES (?, ?)', [
    username, // pkok976
    password, // aktlakfh1!
  ]);

  res.json({ message: '회원가입 완료' });
  // res.status(201).json({ message: '회원가입 완료' });
});

app.listen(PORT, () => {
    console.log(`server running on http://localhost:${PORT}`)
})