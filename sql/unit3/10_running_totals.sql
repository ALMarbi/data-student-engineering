SELECT s.student_id, s.full_name, a.assessment_id,
       ROUND((a.score / a.max_score) * 100.0, 2) AS score_percentage,
       ROUND(SUM((a.score / a.max_score) * 100.0) OVER (
           PARTITION BY s.student_id ORDER BY a.assessment_id
       ), 2) AS running_score
FROM students s
JOIN enrollments e ON e.student_id = s.student_id
JOIN assessments a ON a.enrollment_id = e.enrollment_id
ORDER BY s.student_id, a.assessment_id;
