import csv
from pathlib import Path

ANALYTICS_DIR = Path(__file__).resolve().parents[2] / "data" / "analytics"
ANALYTICS_DIR.mkdir(parents=True, exist_ok=True)

STUDENT_ANALYTICS_QUERY = """
WITH student_metrics AS (
    SELECT
        s.student_id,
        s.full_name,
        s.city,
        COUNT(DISTINCT e.course_code) AS courses_count,
        AVG((a.score / a.max_score) * 100.0) AS average_score
    FROM students AS s
    JOIN enrollments AS e ON e.student_id = s.student_id
    JOIN assessments AS a ON a.enrollment_id = e.enrollment_id
    GROUP BY s.student_id, s.full_name, s.city
), ranked_students AS (
    SELECT
        *,
        RANK() OVER (ORDER BY average_score DESC) AS university_rank,
        RANK() OVER (PARTITION BY city ORDER BY average_score DESC) AS city_rank,
        AVG(average_score) OVER () AS university_average
    FROM student_metrics
)
SELECT
    student_id,
    full_name AS student_name,
    city,
    courses_count,
    ROUND(average_score, 2) AS average_score,
    university_rank,
    city_rank,
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
"""

REPORT_QUERIES = {
    "01_top_students": """
        SELECT s.student_id, s.full_name AS student_name,
               ROUND(AVG((a.score / a.max_score) * 100.0), 2) AS average_score
        FROM students s
        JOIN enrollments e ON e.student_id = s.student_id
        JOIN assessments a ON a.enrollment_id = e.enrollment_id
        GROUP BY s.student_id, s.full_name
        ORDER BY average_score DESC, s.student_id
        LIMIT 5;
    """,
    "02_student_ranking": """
        WITH averages AS (
            SELECT s.student_id, s.full_name AS student_name,
                   AVG((a.score / a.max_score) * 100.0) AS average_score
            FROM students s
            JOIN enrollments e ON e.student_id = s.student_id
            JOIN assessments a ON a.enrollment_id = e.enrollment_id
            GROUP BY s.student_id, s.full_name
        )
        SELECT student_id, student_name, ROUND(average_score, 2) AS average_score,
               RANK() OVER (ORDER BY average_score DESC) AS student_rank
        FROM averages
        ORDER BY student_rank, student_id;
    """,
    "03_city_ranking": """
        WITH averages AS (
            SELECT s.student_id, s.full_name AS student_name, s.city,
                   AVG((a.score / a.max_score) * 100.0) AS average_score
            FROM students s
            JOIN enrollments e ON e.student_id = s.student_id
            JOIN assessments a ON a.enrollment_id = e.enrollment_id
            GROUP BY s.student_id, s.full_name, s.city
        )
        SELECT student_id, student_name, city, ROUND(average_score, 2) AS average_score,
               RANK() OVER (PARTITION BY city ORDER BY average_score DESC) AS city_rank
        FROM averages
        ORDER BY city, city_rank, student_id;
    """,
    "04_course_ranking": """
        WITH course_averages AS (
            SELECT c.course_code, c.course_name,
                   AVG((a.score / a.max_score) * 100.0) AS average_score
            FROM courses c
            JOIN enrollments e ON e.course_code = c.course_code
            JOIN assessments a ON a.enrollment_id = e.enrollment_id
            GROUP BY c.course_code, c.course_name
        )
        SELECT course_code, course_name, ROUND(average_score, 2) AS average_score,
               RANK() OVER (ORDER BY average_score DESC) AS course_rank
        FROM course_averages
        ORDER BY course_rank, course_code;
    """,
    "05_performance_classification": """
        WITH averages AS (
            SELECT s.student_id, s.full_name AS student_name,
                   AVG((a.score / a.max_score) * 100.0) AS average_score
            FROM students s
            JOIN enrollments e ON e.student_id = s.student_id
            JOIN assessments a ON a.enrollment_id = e.enrollment_id
            GROUP BY s.student_id, s.full_name
        )
        SELECT student_id, student_name, ROUND(average_score, 2) AS average_score,
               CASE
                   WHEN average_score >= 90 THEN 'Excellent'
                   WHEN average_score >= 80 THEN 'Very Good'
                   WHEN average_score >= 70 THEN 'Good'
                   WHEN average_score >= 60 THEN 'Pass'
                   ELSE 'Weak'
               END AS performance_level
        FROM averages
        ORDER BY average_score DESC;
    """,
    "06_previous_vs_current_score": """
        WITH scores AS (
            SELECT s.student_id, s.full_name AS student_name,
                   e.course_code, e.enrollment_id, a.assessment_type,
                   (a.score / a.max_score) * 100.0 AS score_percentage,
                   a.assessment_id
            FROM students s
            JOIN enrollments e ON e.student_id = s.student_id
            JOIN assessments a ON a.enrollment_id = e.enrollment_id
        ), ordered AS (
            SELECT *, LAG(score_percentage) OVER (
                PARTITION BY student_id, course_code ORDER BY assessment_id
            ) AS previous_score
            FROM scores
        )
        SELECT student_id, student_name, course_code, assessment_type,
               ROUND(score_percentage, 2) AS current_score,
               ROUND(previous_score, 2) AS previous_score,
               ROUND(score_percentage - previous_score, 2) AS score_change
        FROM ordered
        ORDER BY student_id, course_code, assessment_id;
    """,
    "07_running_score": """
        SELECT s.student_id, s.full_name AS student_name,
               a.assessment_id,
               ROUND((a.score / a.max_score) * 100.0, 2) AS score_percentage,
               ROUND(SUM((a.score / a.max_score) * 100.0) OVER (
                   PARTITION BY s.student_id ORDER BY a.assessment_id
                   ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
               ), 2) AS running_score,
               ROUND(AVG((a.score / a.max_score) * 100.0) OVER (
                   PARTITION BY s.student_id ORDER BY a.assessment_id
                   ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
               ), 2) AS running_average
        FROM students s
        JOIN enrollments e ON e.student_id = s.student_id
        JOIN assessments a ON a.enrollment_id = e.enrollment_id
        ORDER BY s.student_id, a.assessment_id;
    """,
    "08_average_vs_university": """
        WITH averages AS (
            SELECT s.student_id, s.full_name AS student_name,
                   AVG((a.score / a.max_score) * 100.0) AS average_score
            FROM students s
            JOIN enrollments e ON e.student_id = s.student_id
            JOIN assessments a ON a.enrollment_id = e.enrollment_id
            GROUP BY s.student_id, s.full_name
        )
        SELECT student_id, student_name, ROUND(average_score, 2) AS average_score,
               ROUND(AVG(average_score) OVER (), 2) AS university_average,
               ROUND(average_score - AVG(average_score) OVER (), 2) AS difference_from_average
        FROM averages
        ORDER BY average_score DESC;
    """,
}


def run_query(connection, query):
    return connection.execute(query).fetchall()


def run_all_reports(connection):
    reports = {name: run_query(connection, query) for name, query in REPORT_QUERIES.items()}
    reports["11_student_analytics"] = run_query(connection, STUDENT_ANALYTICS_QUERY)
    return reports


def export_student_analytics(connection):
    rows = run_query(connection, STUDENT_ANALYTICS_QUERY)
    if not rows:
        raise ValueError("No analytics rows to export.")

    output = ANALYTICS_DIR / "student_analytics.csv"
    with output.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows([dict(row) for row in rows])
    return output
