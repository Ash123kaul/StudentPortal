// server.js
const express = require('express');
const mysql = require('mysql2'); // or your database driver
const cors = require('cors');
const app = express();

app.use(cors());
app.use(express.json());

// Database connection
const db = mysql.createConnection({
  host: 'your-database-host',
  user: 'your-username',
  password: 'your-password',
  database: 'your-database-name'
});

// Login endpoint
app.post('/api/login', (req, res) => {
  const { username, password, userType } = req.body;
  
  // Query database to verify credentials
  let query = '';
  if (userType === 'student') {
    query = 'SELECT * FROM students WHERE student_id = ? AND password = ?';
  } else if (userType === 'counselor') {
    query = 'SELECT * FROM counselors WHERE username = ? AND password = ?';
  }
  
  db.execute(query, [username, password], (err, results) => {
    if (err) {
      return res.status(500).json({ error: 'Database error' });
    }
    
    if (results.length > 0) {
      res.json({ 
        success: true, 
        user: results[0],
        userType: userType
      });
    } else {
      res.status(401).json({ success: false, message: 'Invalid credentials' });
    }
  });
});

// Get student data
app.get('/api/student/:id', (req, res) => {
  const studentId = req.params.id;
  
  const query = `
    SELECT s.*, 
           a.attendance_percentage,
           AVG(g.score) as average_score,
           COUNT(DISTINCT c.course_id) as courses_completed
    FROM students s
    LEFT JOIN attendance a ON s.student_id = a.student_id
    LEFT JOIN grades g ON s.student_id = g.student_id
    LEFT JOIN courses c ON s.student_id = c.student_id AND c.status = 'completed'
    WHERE s.student_id = ?
    GROUP BY s.student_id
  `;
  
  db.execute(query, [studentId], (err, results) => {
    if (err) {
      return res.status(500).json({ error: 'Database error' });
    }
    
    if (results.length > 0) {
      res.json({ student: results[0] });
    } else {
      res.status(404).json({ error: 'Student not found' });
    }
  });
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});