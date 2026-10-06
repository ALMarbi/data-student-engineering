SELECT
    COUNT(*) AS total_assessments,
    SUM(CASE WHEN (score / max_score) * 100.0 >= 90 THEN 1 ELSE 0 END) AS excellent_count,
    SUM(CASE WHEN (score / max_score) * 100.0 < 60 THEN 1 ELSE 0 END) AS weak_count,
    ROUND(100.0 * SUM(CASE WHEN (score / max_score) * 100.0 >= 60 THEN 1 ELSE 0 END) / COUNT(*), 2) AS pass_rate
FROM assessments;
