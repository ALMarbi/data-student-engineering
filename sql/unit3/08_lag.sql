WITH scores AS (
    SELECT s.student_id, s.full_name, e.course_code, a.assessment_id,
           a.assessment_type,
           (a.score / a.max_score) * 100.0 AS score_percentage
    FROM students s
    JOIN enrollments e ON e.student_id = s.student_id
    JOIN assessments a ON a.enrollment_id = e.enrollment_id
)
SELECT *, LAG(score_percentage) OVER (
    PARTITION BY student_id, course_code ORDER BY assessment_id
) AS previous_score
FROM scores;
