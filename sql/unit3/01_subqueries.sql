-- Students whose average assessment percentage is above the university average.
SELECT s.student_id, s.full_name,
       ROUND(AVG((a.score / a.max_score) * 100.0), 2) AS average_score
FROM students s
JOIN enrollments e ON e.student_id = s.student_id
JOIN assessments a ON a.enrollment_id = e.enrollment_id
GROUP BY s.student_id, s.full_name
HAVING AVG((a.score / a.max_score) * 100.0) > (
    SELECT AVG((a2.score / a2.max_score) * 100.0)
    FROM assessments a2
);
