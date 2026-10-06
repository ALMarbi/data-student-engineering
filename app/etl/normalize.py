


def flatten_student_documents(documents: list[dict]) -> list[dict]:
    rows = []
    for student in documents:
        for course in student.get("courses", []):
            for assessment in course.get("assessments", []):
                rows.append(
                    {
                        "student_id": student.get("student_id"),
                        "full_name": student.get("full_name"),
                        "age": student.get("age"),
                        "major": student.get("major"),
                        "gpa": student.get("gpa"),
                        "course_code": course.get("course_code"),
                        "course_name": course.get("course_name"),
                        "credit_hours": course.get("credit_hours"),
                        "semester": course.get("semester"),
                        "assessment_type": assessment.get("assessment_type"),
                        "max_score": assessment.get("max_score"),
                        "score": assessment.get("score"),
                    }
                )
    return rows
