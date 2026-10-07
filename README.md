# English Learning Platform V4 — Alijon Davlatov

Original CEFR-aligned English course for Tajik-speaking learners. 7 levels (A0-C2), 12 units/level, 4 lessons/unit = 336 lessons.

Features: TJ/RU/EN UI, placement test, level recommendation, lesson practice, vocabulary with IPA/Tajik/Russian, browser TTS + speech recognition, five-part homework, six-section final exams, progress, certificates with QR verification, admin dashboard, optional OpenRouter AI Teacher, PWA.

Content is original and not copied from Oxford or other copyrighted textbooks. The platform certificate certifies completion of this platform's course only; it is not IELTS/Cambridge/state accreditation.

## Render
Build: `pip install -r requirements.txt`
Start: `gunicorn app.main:app --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 120`

Set DATABASE_URL, SECRET_KEY, ADMIN_USERNAME, ADMIN_PASSWORD. OPENROUTER_API_KEY is optional.

## Testing
Run `python3 tools/smoke_test.py` after dependencies are installed. Run `python3 tools/validate_content.py` to validate generated content.
