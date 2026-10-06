from app.database.schema import initialize_database
from app.repositories.student_repository import StudentRepository
from app.repositories.course_repository import CourseRepository
from app.repositories.enrollment_repository import EnrollmentRepository
from app.repositories.assessment_repository import AssessmentRepository
from app.etl.pipeline import run_all_source_pipelines
from app.sources.mock_api import start_mock_api
from app.sources.mongodb import seed_mongo_demo
from app.analytics.advanced_sql import run_all_reports, export_student_analytics

def seed_demo_data(student_repo, course_repo, enrollment_repo, assessment_repo):
    students = [
        ("STU001", "Ahmed Ali", 21, "Computer Science", 3.45),
        ("STU002", "Sara Mohammed", 22, "Artificial Intelligence", 3.82),
        ("STU003", "Omar Hassan", 20, "Information Systems", 2.91),
        ("STU004", "Noura Salem", 23, "Computer Science", 3.67),
    ]
    courses = [
        ("CS101", "Python Programming", 3),
        ("DB201", "Database Systems", 3),
        ("DE301", "Data Engineering", 4),
    ]

    for student in students:
        try:
            student_repo.create(*student)
        except Exception:
            pass

   
    cities = {
        "STU001": "Sanaa",
        "STU002": "Dhamar",
        "STU003": "Taiz",
        "STU004": "Sanaa",
    }
    for student_id, city in cities.items():
        student_repo.update(student_id, city=city)

    for course in courses:
        try:
            course_repo.create(*course)
        except Exception:
            pass

    enrollments = [
        ("STU001", "CS101"), ("STU001", "DB201"),
        ("STU002", "CS101"), ("STU002", "DE301"),
        ("STU003", "DB201"),
        ("STU004", "CS101"), ("STU004", "DE301"),
    ]

    for student_id, course_code in enrollments:
        try:
            enrollment_id = enrollment_repo.create(
                student_id, course_code, "2026-Fall"
            )
            assessment_repo.create(enrollment_id, "Midterm", 25, 22)
            assessment_repo.create(enrollment_id, "Final", 50, 42)
            assessment_repo.create(enrollment_id, "Assignment", 25, 23)
        except Exception:
            pass

def main():
    conn = initialize_database()

    student_repo = StudentRepository(conn)
    course_repo = CourseRepository(conn)
    enrollment_repo = EnrollmentRepository(conn)
    assessment_repo = AssessmentRepository(conn)

    seed_demo_data(
        student_repo, course_repo, enrollment_repo, assessment_repo
    )

    demo_scores = {
        "STU001": {"Midterm": 22, "Final": 42, "Assignment": 23},
        "STU002": {"Midterm": 24, "Final": 47, "Assignment": 24},
        "STU003": {"Midterm": 18, "Final": 35, "Assignment": 20},
        "STU004": {"Midterm": 23, "Final": 45, "Assignment": 24},
    }
    for student_id, scores in demo_scores.items():
        for assessment_type, score in scores.items():
            conn.execute(
                """
                UPDATE assessments
                SET score = ?
                WHERE assessment_type = ?
                  AND enrollment_id IN (
                      SELECT enrollment_id
                      FROM enrollments
                      WHERE student_id = ?
                  )
                """,
                (score, assessment_type, student_id),
            )
    conn.commit()

  
    student_repo.update("STU003", gpa=3.05)


    course_repo.create("TMP999", "Temporary Course", 1)
    course_repo.delete("TMP999")


    api_server = start_mock_api()

 
    mongo_seeded = seed_mongo_demo()


    pipeline_files = run_all_source_pipelines(conn)

  
    reports = run_all_reports(conn)
    analytics_file = export_student_analytics(conn)

    api_server.shutdown()
    conn.close()

    print("Application completed successfully.")
    print(f"MongoDB documents seeded: {mongo_seeded}")
    print("Source-specific ETL outputs:")
    for source, output_file in pipeline_files.items():
        print(f"  {source.upper()}: {output_file}")
    print(f"Advanced SQL analytics: {analytics_file}")
    print(f"Advanced SQL reports executed: {len(reports)}")


if __name__ == "__main__":
    main()
