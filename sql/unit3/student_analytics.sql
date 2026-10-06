-- Unit 3 master analytical query
WITH student_metrics AS (
    SELECT
        s.student_id,
        s.full_name,
        s.city,
        COUNT(DISTINCT e.course_code) AS courses_count,
        AVG((a.score / a.max_score) * 100.0) AS average_score
    FROM students s
    JOIN enrollments e ON e.student_id = s.student_id
    JOIN assessments a ON a.enrollment_id = e.enrollment_id
    GROUP BY s.student_id, s.full_name, s.city
), ranked_students AS (
    SELECT *,
           RANK() OVER (ORDER BY average_score DESC) AS university_rank,
           RANK() OVER (PARTITION BY city ORDER BY average_score DESC) AS city_rank,
           AVG(average_score) OVER () AS university_average
    FROM student_metrics
)
SELECT student_id, full_name AS student_name, city, courses_count,
       ROUND(average_score, 2) AS average_score,
       university_rank, city_rank,
       ROUND(average_score - university_average, 2) AS difference_from_average,
       CASE
           WHEN average_score >= 90 THEN 'Excellent'
           WHEN average_score >= 80 THEN 'Very Good'
           WHEN average_score >= 70 THEN 'Good'
           WHEN average_score >= 60 THEN 'Pass'
           ELSE 'Weak'
       END AS performance_level
FROM ranked_students
ORDER BY university_rank, student_id;
