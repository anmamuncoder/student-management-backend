import json
import requests

# -----------------------
# CONFIG
# -----------------------
BASE_URL = "http://localhost:8020/api/v1"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc5NzI4MjIwLCJpYXQiOjE3NzcxMzYyMjAsImp0aSI6IjgwNDhiMjBjMzQ2NzQ0ZDU5Zjg4NDM0NGJmNGJiNTQ0IiwiaWQiOiI5NDRiMTBlNi00MjJhLTQ5OGMtOGMwNi01ZjgyOTMyMjQ1YmYifQ.Dv8n3HBgB2e7jn9MoSVnMdzuSwVcTRzK1s34BeEq2V0"


STATE_FILE = "restore_state.json"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

session = requests.Session()
session.headers.update(HEADERS)

# -----------------------
# LOAD DATA
# -----------------------
with open("data.json", "r", encoding="utf-8", errors="replace") as f:
    data = json.load(f)

# -----------------------
# MAPS
# -----------------------
rank_map = {}
student_type_map = {}
course_map = {}
module_map = {}
subject_map = {}
batch_map = {}
user_map = {}
student_map = {}

existing_pnumbers = set()

# -----------------------
# HELPER
# -----------------------
def post(url, payload,label=""):
    res = session.post(url, json=payload)
    if res.status_code in [200, 201]:
        return res.json()
    else:
        print("URL:", url)
        print("Payload:", payload)
        print(f"❌ {label}", res.text)
        print("-" * 60)
        return None

# -----------------------
# RANK
# -----------------------
def create_ranks():
    for i, r in enumerate(data["designations"], start=1):

        payload = {
            "name": r["name"],
            "code": (r.get('note') or r["name"].lower().replace(" ", "_")) + f"_{i}",
            "order": r["id"]
        }

        res = post(f"{BASE_URL}/accounts/ranks/", payload)

        if res:
            rank_map[r["id"]] = res["id"]
            # print(f"Created: {r['name']} -> {payload['code']}")

# -----------------------
# STUDENT TYPE
# -----------------------
def create_student_types():
    for st in data["student_types"]:
        payload = {
            "name": st["type"],
            "note": st.get("note")
        }
        res = post(f"{BASE_URL}/students/student-types/", payload)
        if res:
            student_type_map[st["id"]] = res["id"]

# -----------------------
# COURSES
# -----------------------
def create_courses():
    for c in data["classes"]:
        payload = {
            "name": c["course_fullname"],
            "short_name": c["name"],
            "duration": c["duration"],
            "vacancy": int(c["vacency"]),
            "note": c["note"]
        }
        res = post(f"{BASE_URL}/courses/courses/", payload)
        if res:
            course_map[c["id"]] = res["id"]

# -----------------------
# MODULES
# -----------------------
def create_modules():
    for m in data["mainblocksyllabus_tbl"]:
        payload = {
            "name": m["module_name"],
            "code": m["module_code"]
        }
        res = post(f"{BASE_URL}/courses/modules/", payload)
        if res:
            module_map[m["id"]] = res["id"]

# -----------------------
# SUBJECTS
# -----------------------
def create_subjects():
    for s in data["main_syllabuses"]:
        payload = {
            "name": s["subject_name"],
            "code": s["subject_code"]
        }
        res = post(f"{BASE_URL}/courses/subjects/", payload)
        if res:
            subject_map[s["id"]] = res["id"]

# -----------------------
# SYLLABUS
# -----------------------
def create_syllabus():
    for m in data["mainblocksyllabus_tbl"]:
        payload = {
            "course": course_map.get(int(m["class_id"])),
            "module": module_map.get(m["id"]),
            "trade": m["trade"],
            "note": m["note"]
        }
        post(f"{BASE_URL}/courses/syllabus/", payload)

# -----------------------
# DETAIL SYLLABUS
# -----------------------
def create_detail_syllabus():
    for s in data["syllabuses"]:
        payload = {
            "course": course_map.get(s["class_id"]),
            "module": module_map.get(s["module_id"]),
            "subject": subject_map.get(int(s["mainsyllabus_id"])),
            "lecture": int(s["lecture"]),
            "practical": int(s["practical"]),
            "written": int(s["written"]),
            "others": int(s["others"]),
            "note": s["note"]
        }
        post(f"{BASE_URL}/courses/detail-syllabus/", payload)

# -----------------------
# BATCH
# -----------------------
def create_batches():
    for c in data["classes"]:
        payload = {
            "name": f"{c['name']} Batch",
            "course": course_map.get(c["id"]),
            "note": c["note"]
        }
        res = post(f"{BASE_URL}/courses/batches/", payload)
        if res:
            batch_map[c["id"]] = res["id"]

# -----------------------
# USERS (MERGED)
# -----------------------

def create_users():
    url = f"{BASE_URL}/accounts/users/"

    # MAIN STUDENTS
    for s in data["main_students"]:
        create_user(s, s["id"],label="Main Student")

    # NORMAL STUDENTS
    for s in data["students"]:
        create_user(s, s["student_id"],label="Normal Student")


def create_user(s, key,label=""):
    
    email = s.get("email") or f"user{key}@dipstick.com"

    payload = {
        "email": email,
        "password": "12345678",
        "full_name": s.get("name"),
        "phone": s.get("phone"),
        "personal_number": s.get("pnumber"),
    }

    res = post(f"{BASE_URL}/accounts/users/", payload,label=label)
    if res:
        user_map[key] = res["id"]

# -----------------------
# STUDENTS (MERGED LOGIC)
# -----------------------
def create_students():
    url = f"{BASE_URL}/students/students/"

    # MAIN STUDENT
    for s in data["main_students"]:
        pnumber = s["pnumber"]

        payload = {
            "user": user_map.get(s["id"]),
            "student_type": student_type_map.get(s["type_id"]),
            "batch": batch_map.get(int(s.get("class_id", 0))),
            "second_language": s["second_language"],

            "father_full_name": s["father_name"],
            "mother_full_name": s["mother_name"],

            "health_condition": s["health_condition"],
            "is_active": True
        }

        res = post(url, payload)
        if res:
            student_map[s["id"]] = res["id"]
            existing_pnumbers.add(pnumber)

    # NORMAL STUDENT
    for s in data["students"]:
        pnumber = s["pnumber"]

        if pnumber in existing_pnumbers:
            continue

        payload = {
            "user": user_map.get(s["student_id"]),
            "batch": batch_map.get(int(s["class_id"])),
            "is_active": False
        }

        post(url, payload)



def save_state():
    state = {
        "rank_map": rank_map,
        "student_type_map": student_type_map,
        "course_map": course_map,
        "module_map": module_map,
        "subject_map": subject_map,
        "batch_map": batch_map,
        "user_map": user_map,
        "student_map": student_map,
        "existing_pnumbers": list(existing_pnumbers)
    }

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=4, ensure_ascii=False)

    print("STATE SAVED SUCCESSFULLY")
# -----------------------
# RUN ORDER
# -----------------------
if __name__ == "__main__":
    print("Ranks")
    create_ranks()

    print("Student Types")
    create_student_types()

    print("Courses")
    create_courses()

    print("Modules")
    create_modules()

    print("Subjects")
    create_subjects()

    print("Syllabus")
    create_syllabus()

    print("Detail Syllabus")
    create_detail_syllabus()

    print("Batch")
    create_batches()

    print("Users")
    create_users()

    print("Students")
    create_students()

    print("FULL RESTORE COMPLETED")

    save_state()
    print("STATE SAVED TO", STATE_FILE)