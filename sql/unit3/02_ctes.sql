WITH student_average AS (
    SELECT s.student_id, s.full_name,
           AVG((a.score / a.max_score) * 100.0) AS average_score
    FROM students s
    JOIN enrollments e ON e.student_id = s.student_id
    JOIN assessments a ON a.enrollment_id = e.enrollment_id
    GROUP BY s.student_id, s.full_name
)
SELECT student_id, full_name, ROUND(average_score, 2) AS average_score
FROM student_average
ORDER BY average_score DESC;
