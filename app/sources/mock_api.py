"""Small local HTTP API used as an ETL source."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from urllib.request import Request, urlopen


def build_demo_payload() -> list[dict]:
    return [
        {
            "student_id": "STU001",
            "full_name": "Ahmed Ali",
            "age": 21,
            "major": "Computer Science",
            "city": "Sanaa",
            "gpa": 3.45,
            "courses": [
                {
                    "course_code": "CS101",
                    "course_name": "Python Programming",
                    "credit_hours": 3,
                    "semester": "2026-Fall",
                    "assessments": [
                        {"assessment_type": "Midterm", "max_score": 25, "score": 22},
                        {"assessment_type": "Final", "max_score": 50, "score": 42},
                        {"assessment_type": "Assignment", "max_score": 25, "score": 23},
                    ],
                },
                {
                    "course_code": "DB201",
                    "course_name": "Database Systems",
                    "credit_hours": 3,
                    "semester": "2026-Fall",
                    "assessments": [
                        {"assessment_type": "Midterm", "max_score": 25, "score": 22},
                        {"assessment_type": "Final", "max_score": 50, "score": 42},
                        {"assessment_type": "Assignment", "max_score": 25, "score": 23},
                    ],
                },
            ],
        },
        {
            "student_id": "STU002",
            "full_name": "Sara Mohammed",
            "age": 22,
            "major": "Artificial Intelligence",
            "city": "Dhamar",
            "gpa": 3.82,
            "courses": [
                {
                    "course_code": "CS101",
                    "course_name": "Python Programming",
                    "credit_hours": 3,
                    "semester": "2026-Fall",
                    "assessments": [
                        {"assessment_type": "Midterm", "max_score": 25, "score": 24},
                        {"assessment_type": "Final", "max_score": 50, "score": 47},
                        {"assessment_type": "Assignment", "max_score": 25, "score": 24},
                    ],
                },
                {
                    "course_code": "DE301",
                    "course_name": "Data Engineering",
                    "credit_hours": 4,
                    "semester": "2026-Fall",
                    "assessments": [
                        {"assessment_type": "Midterm", "max_score": 24, "score": 24},
                        {"assessment_type": "Final", "max_score": 50, "score": 47},
                        {"assessment_type": "Assignment", "max_score": 25, "score": 24},
                    ],
                },
            ],
        },
        {
            "student_id": "STU003",
            "full_name": "Omar Hassan",
            "age": 20,
            "major": "Information Systems",
            "city": "Taiz",
            "gpa": 3.05,
            "courses": [
                {
                    "course_code": "DB201",
                    "course_name": "Database Systems",
                    "credit_hours": 3,
                    "semester": "2026-Fall",
                    "assessments": [
                        {"assessment_type": "Midterm", "max_score": 25, "score": 18},
                        {"assessment_type": "Final", "max_score": 50, "score": 35},
                        {"assessment_type": "Assignment", "max_score": 25, "score": 20},
                    ],
                }
            ],
        },
        {
            "student_id": "STU004",
            "full_name": "Noura Salem",
            "age": 23,
            "major": "Computer Science",
            "city": "Sanaa",
            "gpa": 3.67,
            "courses": [
                {
                    "course_code": "CS101",
                    "course_name": "Python Programming",
                    "credit_hours": 3,
                    "semester": "2026-Fall",
                    "assessments": [
                        {"assessment_type": "Midterm", "max_score": 25, "score": 23},
                        {"assessment_type": "Final", "max_score": 50, "score": 45},
                        {"assessment_type": "Assignment", "max_score": 25, "score": 24},
                    ],
                },
                {
                    "course_code": "DE301",
                    "course_name": "Data Engineering",
                    "credit_hours": 4,
                    "semester": "2026-Fall",
                    "assessments": [
                        {"assessment_type": "Midterm", "max_score": 25, "score": 23},
                        {"assessment_type": "Final", "max_score": 50, "score": 45},
                        {"assessment_type": "Assignment", "max_score": 25, "score": 24},
                    ],
                },
            ],
        },
    ]


class _Handler(BaseHTTPRequestHandler):
    payload = build_demo_payload()

    def do_GET(self):  # noqa: N802
        if self.path != "/api/students":
            self.send_response(404)
            self.end_headers()
            return

        body = json.dumps({"students": self.payload}, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        return


def start_mock_api(host: str = "127.0.0.1", port: int = 8765) -> ThreadingHTTPServer:
    server = ThreadingHTTPServer((host, port), _Handler)
    Thread(target=server.serve_forever, daemon=True).start()
    return server


def extract_api(url: str = "http://127.0.0.1:8765/api/students", timeout: int = 5) -> list[dict]:
    request = Request(url, headers={"Accept": "application/json"})
    with urlopen(request, timeout=timeout) as response:
        payload = json.load(response)
    return payload.get("students", payload)
