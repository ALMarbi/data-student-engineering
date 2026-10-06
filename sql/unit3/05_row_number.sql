WITH scores AS (
    SELECT s.student_id, s.full_name, c.course_name,
           (a.score / a.max_score) * 100.0 AS score_percentage
    FROM students s
    JOIN enrollments e ON e.student_id = s.student_id
    JOIN courses c ON c.course_code = e.course_code
    JOIN assessments a ON a.enrollment_id = e.enrollment_id
)
SELECT *, ROW_NUMBER() OVER (PARTITION BY student_id ORDER BY score_percentage DESC) AS score_number
FROM scores;
