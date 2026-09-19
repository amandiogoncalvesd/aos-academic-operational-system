# aos-domain-sis

Plugin de domínio SIS (Student Information System) — cursos e matrículas.

- API: `/api/v1/sis/courses`, `/api/v1/sis/enrollments`
- Publica: `sis.course.created`, `sis.student.enrolled`, `sis.enrollment.cancelled`
- Filter `sis.enrollment.validate`: outros plugins (ERP, pré-requisitos) podem vetar uma matrícula devolvendo `{"ok": False, "reason": "..."}`.
