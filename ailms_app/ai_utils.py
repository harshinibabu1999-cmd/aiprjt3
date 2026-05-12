import os
import re
import json
import random
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = None
if os.getenv("OPENAI_API_KEY"):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ---------------------------------------------------------------------------
# Content-based question generation (no OpenAI required)
# ---------------------------------------------------------------------------

def _extract_key_facts(text):
    """Pull out sentences that contain strong factual signals."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    facts = []
    for s in sentences:
        s = s.strip()
        # Keep sentences that are factual (not too short, not headers)
        if len(s) > 60 and not s.isupper() and ':' not in s[:25]:
            facts.append(s)
    return facts


def _make_distractor(correct_answer, all_facts, seed_words):
    """Create a plausible wrong answer from other content in the text."""
    # Pull nouns / phrases that appear in the text but differ from the answer
    candidates = []
    words = re.findall(r'\b[A-Z][a-zA-Z]{3,}\b', ' '.join(all_facts))
    words = list(set(words) - set(re.findall(r'\b[A-Z][a-zA-Z]{3,}\b', correct_answer)))
    candidates = words[:40]
    random.shuffle(candidates)
    for c in candidates:
        if c.lower() not in correct_answer.lower():
            return c
    # absolute fallback
    return random.choice(["None of the above", "All of the above", "Not mentioned in text", "Cannot be determined"])


def _build_fill_question(sentence, difficulty):
    """Turn a factual sentence into a fill-in-the-blank MCQ."""
    # Find a good candidate phrase to blank out
    # For Easy: blank the last key noun phrase
    # For Medium: blank a mid-sentence key term
    # For Hard: blank a technical term / number / name
    
    words = sentence.split()
    if len(words) < 8:
        return None

    if difficulty == 'easy':
        # blank the last meaningful word (noun, year, name)
        for i in range(len(words) - 1, len(words) // 2, -1):
            w = words[i].strip('.,;:()"\'-')
            if len(w) > 3 and w[0].isupper():
                answer = w
                question = ' '.join(words[:i]) + ' _____ ' + ' '.join(words[i+1:])
                return question.strip(), answer

    elif difficulty == 'medium':
        # blank an important mid-sentence term
        mid = len(words) // 2
        for i in range(mid, mid + 10 if mid + 10 < len(words) else len(words)):
            w = words[i].strip('.,;:()"\'-')
            if len(w) > 4:
                answer = w
                question = ' '.join(words[:i]) + ' _____ ' + ' '.join(words[i+1:])
                return question.strip(), answer

    else:  # hard
        # blank a technical abbreviation or year
        for i, w in enumerate(words):
            clean = w.strip('.,;:()"\'-')
            if (clean.isupper() and len(clean) > 1) or re.match(r'^\d{4}$', clean) or (len(clean) > 6 and clean[0].isupper()):
                answer = clean
                question = ' '.join(words[:i]) + ' _____ ' + ' '.join(words[i+1:])
                return question.strip(), answer

    return None


def _generate_content_questions(text, difficulty, count=10):
    """Generate MCQs directly from the textbook content."""
    facts = _extract_key_facts(text)
    if not facts:
        return []

    random.shuffle(facts)
    questions = []
    attempts = 0
    max_attempts = min(len(facts), 50)

    while len(questions) < count and attempts < max_attempts:
        sentence = facts[attempts % len(facts)]
        attempts += 1

        result = _build_fill_question(sentence, difficulty)
        if not result:
            continue

        question_text, correct_answer = result

        # Guard: question must be meaningful
        if len(question_text) < 30 or len(correct_answer) < 2:
            continue

        # Build distractors from other content
        distractors = set()
        other_facts = [f for f in facts if f != sentence]
        random.shuffle(other_facts)

        for f in other_facts:
            words = re.findall(r'\b[A-Za-z][a-zA-Z]{3,}\b', f)
            for w in words:
                if w.lower() != correct_answer.lower() and w not in distractors:
                    distractors.add(w)
                if len(distractors) >= 3:
                    break
            if len(distractors) >= 3:
                break

        # Fill remaining distractors if needed
        fallbacks = [
            "Not defined in this text", "All of the above",
            "None of these", "Cannot be determined from context"
        ]
        while len(distractors) < 3:
            distractors.add(fallbacks[len(distractors)])

        options = [correct_answer] + list(distractors)[:3]
        random.shuffle(options)

        questions.append({
            "question": f"Fill in the blank: {question_text}",
            "options": options,
            "answer": correct_answer
        })

    # If we couldn't generate enough fill-in-blank questions, supplement with
    # "Which of the following is described in the text?" questions
    if len(questions) < count:
        for sentence in facts[:count - len(questions)]:
            snippet = sentence[:180] + ("..." if len(sentence) > 180 else "")
            words = re.findall(r'\b[A-Z][a-zA-Z]{3,}\b', sentence)
            if not words:
                continue
            correct = random.choice(words)
            distractors = [
                "Not mentioned in the text", "A general concept only",
                "Defined elsewhere in the course"
            ]
            options = [correct] + distractors
            random.shuffle(options)
            questions.append({
                "question": f"According to the course material: \"{snippet}\" — which key term is central to this concept?",
                "options": options,
                "answer": correct
            })

    return questions[:count]


# ---------------------------------------------------------------------------
# OpenAI path (used when API key is set)
# ---------------------------------------------------------------------------

def get_ai_response(prompt, json_mode=False):
    if not client:
        return None  # caller must handle None
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"} if json_mode else None
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"AI Error: {e}")
        return None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_quiz(content, difficulty="medium"):
    """
    Generate 10 MCQs from the provided course content.
    Uses OpenAI if available, otherwise falls back to content-based extraction.
    """
    if not content or not content.strip():
        return []

    difficulty = difficulty.lower()

    # --- OpenAI path ---
    if client:
        difficulty_instructions = {
            "easy": "Focus on basic definitions, key terms, and foundational concepts explicitly stated in the text.",
            "medium": "Focus on understanding and application of concepts described in the text.",
            "hard": "Focus on deep analysis, advanced concepts, technical details, and inter-relating multiple ideas from the text.",
        }
        instruction = difficulty_instructions.get(difficulty, difficulty_instructions["medium"])
        prompt = (
            f"You are an expert educator. Generate exactly 10 multiple-choice questions (MCQs) "
            f"strictly based on the following course material. {instruction} "
            f"Each question must be directly answerable from the provided text only — "
            f"do NOT use outside knowledge. "
            f"Return JSON with a single key 'questions', which is a list of objects, each with: "
            f"'question' (string), 'options' (list of exactly 4 strings), 'answer' (string — must exactly match one option).\n\n"
            f"COURSE MATERIAL:\n{content[:6000]}"
        )
        res = get_ai_response(prompt, json_mode=True)
        if res:
            try:
                data = json.loads(res)
                qs = data.get('questions', [])
                if qs:
                    return qs
            except Exception:
                pass

    # --- Content-based fallback ---
    print(f"[ai_utils] Using content-based question generator for difficulty='{difficulty}'")
    return _generate_content_questions(content, difficulty, count=10)


def parse_resume(text):
    if not text:
        return [], "Unknown"
    
    if client:
        prompt = f"Extract skills (list) and domain from this resume: {text[:4000]}. Format as JSON with keys 'skills', 'domain'."
        res = get_ai_response(prompt, json_mode=True)
        if res:
            try:
                data = json.loads(res)
                skills = data.get('skills', [])
                domain = data.get('domain', 'Unknown')
                if skills:
                    return skills, domain
            except Exception:
                pass
                
    # Content-based fallback
    text_lower = text.lower()
    skills = []
    domain = "Software Engineering"
    
    if any(w in text_lower for w in ["ui", "ux", "figma", "sketch", "design", "wireframe", "prototype"]):
        skills.extend(["UI/UX Design", "Figma", "User Research", "Wireframing"])
        domain = "UI/UX Design"
    if any(w in text_lower for w in ["python", "django", "flask", "fastapi"]):
        skills.extend(["Python", "Backend Development"])
        domain = "Backend Engineering" if domain == "Software Engineering" else domain
    if any(w in text_lower for w in ["javascript", "react", "angular", "vue", "html", "css", "frontend"]):
        skills.extend(["JavaScript", "Frontend Web", "HTML/CSS"])
        domain = "Frontend Engineering" if domain == "Software Engineering" else domain
    if any(w in text_lower for w in ["machine learning", "ai", "data science", "tensorflow", "pytorch"]):
        skills.extend(["Machine Learning", "Data Analysis"])
        domain = "Data Science & AI" if domain == "Software Engineering" else domain
    if any(w in text_lower for w in ["sql", "database", "analytics", "tableau", "power bi"]):
        skills.extend(["SQL", "Data Analytics"])
        domain = "Data Analytics" if domain == "Software Engineering" else domain
        
    if not skills:
        skills = ["Problem Solving", "Software Development", "Communication"]
        
    return list(set(skills)), domain


def suggest_jobs(skills):
    if client:
        prompt = (
            f"Suggest exactly 4 realistic job roles based on these skills: {skills}. "
            f"For each role provide a clear career progression path. "
            f"Return JSON with 'jobs' as a list of objects with keys 'role' and 'path'."
        )
        res = get_ai_response(prompt, json_mode=True)
        if res:
            try:
                data = json.loads(res)
                jobs = data.get('jobs', [])
                if jobs:
                    return jobs
            except Exception:
                pass

    # Smart fallback: infer roles from skill keywords
    skills_str = " ".join(skills).lower() if isinstance(skills, list) else str(skills).lower()

    if any(w in skills_str for w in ["python", "django", "flask", "fastapi"]):
        return [
            {"role": "Python Developer", "path": "Junior Dev → Senior Dev → Tech Lead"},
            {"role": "Backend Engineer", "path": "Engineer → Senior → Principal Engineer"},
            {"role": "ML Engineer", "path": "Junior ML → ML Engineer → Staff ML Engineer"},
            {"role": "Data Engineer", "path": "Analyst → Data Engineer → Architect"},
        ]
    elif any(w in skills_str for w in ["ui", "ux", "design", "figma", "wireframing"]):
        return [
            {"role": "UI/UX Designer", "path": "Junior Designer → Senior Designer → Design Lead"},
            {"role": "Product Designer", "path": "Designer → Senior Product Designer → Head of Design"},
            {"role": "UX Researcher", "path": "Junior Researcher → Senior Researcher → UX Director"},
            {"role": "Frontend Developer", "path": "Junior Dev → Frontend Engineer → Tech Lead"},
        ]
    elif any(w in skills_str for w in ["machine learning", "ai", "tensorflow", "pytorch", "deep learning"]):
        return [
            {"role": "ML Engineer", "path": "Junior ML Engineer → ML Engineer → Principal"},
            {"role": "AI Research Scientist", "path": "Research Engineer → Scientist → Director of AI"},
            {"role": "Data Scientist", "path": "Analyst → Data Scientist → Lead Scientist"},
            {"role": "NLP Engineer", "path": "Engineer → Senior NLP → Head of NLP"},
        ]
    elif any(w in skills_str for w in ["react", "javascript", "typescript", "vue", "angular"]):
        return [
            {"role": "Frontend Engineer", "path": "Junior → Senior → Lead Frontend"},
            {"role": "Full Stack Developer", "path": "Junior Dev → Full Stack → CTO"},
            {"role": "UI/UX Engineer", "path": "Designer → Engineer → Design Systems Lead"},
            {"role": "React Native Developer", "path": "Mobile Dev → Senior → Tech Lead"},
        ]
    elif any(w in skills_str for w in ["java", "spring", "kotlin"]):
        return [
            {"role": "Java Developer", "path": "Junior → Senior → Architect"},
            {"role": "Backend Engineer", "path": "Engineer → Senior → Principal"},
            {"role": "Android Developer", "path": "Junior → Senior → Lead Mobile"},
            {"role": "DevOps Engineer", "path": "Engineer → Senior → Platform Lead"},
        ]
    elif any(w in skills_str for w in ["sql", "data", "analytics", "tableau", "power bi"]):
        return [
            {"role": "Data Analyst", "path": "Junior Analyst → Senior Analyst → Manager"},
            {"role": "Business Intelligence Engineer", "path": "BI Developer → Senior → Director"},
            {"role": "Data Scientist", "path": "Analyst → Scientist → Lead Scientist"},
            {"role": "Database Administrator", "path": "DBA → Senior DBA → Data Architect"},
        ]
    else:
        return [
            {"role": "Software Engineer", "path": "Junior → Mid-Level → Senior → Staff"},
            {"role": "Product Manager", "path": "APM → PM → Senior PM → Director"},
            {"role": "Full Stack Developer", "path": "Junior Dev → Senior Dev → CTO"},
            {"role": "DevOps Engineer", "path": "Junior → Senior → Platform Lead"},
        ]


def recommend_courses_ai(skills):
    if client:
        prompt = f"Recommend courses for skills: {skills}. Format as JSON with 'recommendations' list."
        res = get_ai_response(prompt, json_mode=True)
        if res:
            try:
                data = json.loads(res)
                return data.get('recommendations', [])
            except Exception:
                pass
                
    skills_str = " ".join(skills).lower() if isinstance(skills, list) else str(skills).lower()
    
    if any(w in skills_str for w in ["ui", "ux", "design", "figma"]):
        return ["UI/UX Fundamentals", "Digital Design Principles", "Advanced CSS"]
    elif any(w in skills_str for w in ["python", "django", "flask", "backend"]):
        return ["Advanced Python", "Backend Engineering with Django", "API Design"]
    elif any(w in skills_str for w in ["javascript", "react", "html", "frontend", "web"]):
        return ["Full Stack Web Development", "React Mastery", "JavaScript Advanced"]
    elif any(w in skills_str for w in ["data", "sql", "analytics"]):
        return ["Data Science Bootcamp", "SQL & Database Design", "Data Analytics"]
    elif any(w in skills_str for w in ["ai", "machine learning", "ml", "tensorflow"]):
        return ["AI & Machine Learning Concepts", "Deep Learning", "Neural Networks"]
    
    return ["Python Foundations", "Intro to Software Engineering", "Full Stack Basics"]
