import json
import requests

# -----------------------
# CONFIG
# -----------------------
BASE_URL = "http://localhost:8000/api/v1"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzg0MTIxNjEyLCJpYXQiOjE3ODE1Mjk2MTIsImp0aSI6ImU3Y2Y2NDIyZGE1ZjQ3Njk5MTJjYTEwY2ZjNjE2ZGFjIiwiaWQiOiJiMWFiY2M3ZC0yZDU1LTQxZDEtYWEyNi1kMmI0MDZjMjY3ZDYifQ.iG3LdQr25UcvdAEkcCZIiGznAn2_by1l0jHqHYR00rk"

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
batch_membership_map = {}

# global serial number
index_no_counter = 1



teacher_map = {}   # old teacher id → new user id
MARITAL_STATUS_TEACHER_MAP = {
    "yes":      "married",
    "no":       "single",
    "married":  "married",
    "single":   "single",
    "divorced": "divorced",
    "widowed":  "widowed",
}

exam_grade_map = {}
event_map = {}

# -----------------------
# NORMALIZERS
# -----------------------
BLOOD_GROUP_MAP = {
    "a_positive":  "A+",
    "a_negative":  "A-",
    "b_positive":  "B+",
    "b_negative":  "B-",
    "ab_positive": "AB+",
    "ab_negative": "AB-",
    "o_positive":  "O+",
    "o_negative":  "O-",
    "a+": "A+", "a-": "A-",
    "b+": "B+", "b-": "B-",
    "ab+": "AB+", "ab-": "AB-",
    "o+": "O+", "o-": "O-",
}

MARITAL_STATUS_MAP = {
    "single":    "single",
    "married":   "married",
    "Married":   "married",
    "divorced":  "divorced",
    "widowed":   "widowed",
    "unmarried": "single",
    "widow":     "widowed",
    "widower":   "widowed",
}


def normalize_blood_group(val):
    if not val:
        return None
    return BLOOD_GROUP_MAP.get(val.strip().lower()) or None


def normalize_marital_status(val):
    if not val:
        return None
    return MARITAL_STATUS_MAP.get(val.strip().lower()) or None


# -----------------------
# HELPERS
# -----------------------
def normalize_pnumber(p):
    return (p or "").replace(" ", "").lower()


def clean_date(val):
    """Return None for invalid/placeholder dates."""
    if not val:
        return None
    s = str(val).strip()
    if s in ("", "0000-00-00", "0000-00-00 00:00:00", "1970-01-01"):
        return None
    return s


def post(url, payload, label=""):
    res = session.post(url, json=payload)
    if res.status_code in [200, 201]:
        return res.json()
    else:
        print(f"POST ERROR [{label}]: {url}")
        print("Payload:", json.dumps(payload, indent=2))
        print("Response:", res.text)
        print("-" * 50)
        return None


def patch(url, payload, label=""):
    res = session.patch(url, json=payload)
    if res.status_code in [200, 202]:
        return res.json()
    else:
        print(f"PATCH ERROR [{label}]: {url}")
        print("Payload:", json.dumps(payload, indent=2))
        print("Response:", res.text)
        print("-" * 50)
        return None


# -----------------------
# PREPARE MAIN STUDENT MAP
# -----------------------
main_student_by_pnumber = {}

for s in data["main_students"]:
    p = normalize_pnumber(s.get("pnumber"))
    if p:
        main_student_by_pnumber[p] = s


# -----------------------
# RANK
# -----------------------
def create_ranks():
    for i, r in enumerate(data["designations"], start=1):
        payload = {
            "name": r["name"],
            "code": (r.get("note") or r["name"].lower().replace(" ", "_")) + f"_{i}",
            "order": r["id"]
        }
        res = post(f"{BASE_URL}/accounts/ranks/", payload, "Rank")
        if res:
            rank_map[r["id"]] = res["id"]


# -----------------------
# STUDENT TYPE
# -----------------------
def create_student_types():
    for st in data["student_types"]:
        payload = {
            "name": st["type"],
            "note": st.get("note")
        }
        res = post(f"{BASE_URL}/students/student-types/", payload, "StudentType")
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
        res = post(f"{BASE_URL}/courses/courses/", payload, "Course")
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
        res = post(f"{BASE_URL}/courses/modules/", payload, "Module")
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
        res = post(f"{BASE_URL}/courses/subjects/", payload, "Subject")
        if res:
            subject_map[s["id"]] = res["id"]


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
        res = post(f"{BASE_URL}/courses/batches/", payload, "Batch")
        if res:
            batch_map[c["id"]] = res["id"]


# -----------------------
# USERS (MERGED)
# -----------------------
def create_users():

    # MAIN USERS — full field mapping
    for s in data["main_students"]:
        create_main_user(s)

    # MERGE / CREATE from students table
    for s in data["students"]:
        p = normalize_pnumber(s.get("pnumber"))

        if p in main_student_by_pnumber:
            # Already created from main_students — patch in email if missing
            main_s = main_student_by_pnumber[p]
            user_id = user_map.get(main_s["id"])

            if not user_id:
                continue

            patch_payload = {}
            if s.get("email"):
                patch_payload["email"] = s["email"]
            if s.get("phone"):
                patch_payload["phone"] = s["phone"]

            if patch_payload:
                patch(f"{BASE_URL}/accounts/users/{user_id}/", patch_payload, "Merge User Email")

        else:
            # Not in main_students — create a basic user
            create_normal_user(s)


def create_main_user(s):
    """Create a user from main_students with all available fields."""
    key = s["id"]
    email = s.get("email") or f"user{key}@dipstick.com"

    rank_id_raw = s.get("rank")
    rank_id = None
    if rank_id_raw:
        try:
            rank_id = rank_map.get(int(rank_id_raw))
        except (ValueError, TypeError):
            pass

    payload = {
        # Identity
        "email": email,
        "password": "12345678",
        "full_name": s.get("name"),
        "short_name": s.get("sname"),
        "personal_number": s.get("pnumber"),

        # Rank
        "rank": rank_id,

        # Contact
        "phone": s.get("phone"),
        "national_id": s.get("national_id") or None,

        # Personal Info
        "age": s.get("age"),
        "gender": s.get("gender") or None,
        "blood_group": normalize_blood_group(s.get("blood_group")),
        "marital_status": normalize_marital_status(s.get("mstatus")),
        "date_of_marriage": clean_date(s.get("dom")),

        # Birth Info
        "birth_date": clean_date(s.get("dob")),
        "place_of_birth": s.get("pob") or None,
        "country": s.get("country") or None,
        "religion": s.get("religion") or None,

        # Address
        "present_address": s.get("present_address") or None,
        "permanent_address": s.get("permanent_address") or None,

        # Organization
        "current_unit": s.get("cunit") or None,
        "parent_unit_auth": s.get("punit") or None,
        "joining_date": clean_date(s.get("date_of_joining")),
        "date_of_enrolment": clean_date(s.get("doc")),
    }

    res = post(f"{BASE_URL}/accounts/users/", payload, "Main User")
    if res:
        user_map[key] = res["id"]


def create_normal_user(s):
    """Create a basic user from students table (not in main_students)."""
    key = s["student_id"]
    email = s.get("email") or f"user{key}@dipstick.com"

    rank_id_raw = s.get("rank")
    rank_id = None
    if rank_id_raw:
        try:
            rank_id = rank_map.get(int(rank_id_raw))
        except (ValueError, TypeError):
            pass

    payload = {
        "email": email,
        "password": "12345678",
        "full_name": s.get("name"),
        "personal_number": s.get("pnumber"),
        "phone": s.get("phone"),
        "rank": rank_id,
        "current_unit": s.get("cunit") or None,
    }

    res = post(f"{BASE_URL}/accounts/users/", payload, "Normal User")
    if res:
        user_map[key] = res["id"]


# -----------------------
# BATCH MEMBERSHIP
# -----------------------
def create_batch_membership(student_id, batch_id=None, is_active=True):
    global index_no_counter 

    payload = {
        "student": student_id,
        "batch": batch_id,
        "is_active": is_active,
        "index_no":index_no_counter
    }
    res = post(f"{BASE_URL}/students/batch-memberships/", payload, "BatchMembership")
    if res:
        batch_membership_map[student_id] = res["id"]
        # next serial
        index_no_counter += 1


# -----------------------
# STUDENTS
# -----------------------
def create_students():
    url = f"{BASE_URL}/students/students/"

    # MAIN — full field mapping to Student model
    for index, s in enumerate(data["main_students"], start=1):
        payload = {
            "user": user_map.get(s["id"]),
            "student_type": student_type_map.get(s.get("type_id")),

            # Academic
            "second_language": s.get("second_language") or None,
            "date_of_joining": clean_date(s.get("date_of_joining")),

            # Family
            "father_full_name": s.get("father_name") or None,
            "father_phone": s.get("father_phone") or None,
            "father_address": s.get("father_address") or None,
            "father_profession": s.get("father_profession") or None,
            "father_designation": s.get("father_designation") or None,

            "mother_full_name": s.get("mother_name") or None,
            "mother_phone": s.get("mother_phone") or None,
            "mother_address": s.get("mother_address") or None,
            "mother_profession": s.get("mother_profession") or None,
            "mother_designation": s.get("mother_designation") or None,

            # Health / Other
            "health_condition": s.get("health_condition") or None,
            "other_info": s.get("other_info") or None,
            "previous_school": s.get("previous_school") or None,
            "previous_class": s.get("previous_class") or None,
            "current_unit": s.get("cunit") or None,
            "parent_unit": s.get("punit") or None,
            "discount": s.get("discount_id") or 0,

            "is_active": True,
            "index_no": index
        }

        res = post(url, payload, "Main Student")
        if res:
            student_id = res["id"]
            student_map[s["id"]] = student_id
            create_batch_membership(student_id, None, True)

    # Patch batch onto already-created main students using students table
    for s in data["students"]:
        p = normalize_pnumber(s.get("pnumber"))

        if p in main_student_by_pnumber:
            main_s = main_student_by_pnumber[p]
            student_id = student_map.get(main_s["id"])

            if not student_id:
                continue

            class_id = s.get("class_id")
            batch_id = batch_map.get(int(class_id)) if class_id and str(class_id).isdigit() else None

            if batch_id:
                membership_id = batch_membership_map.get(student_id)
                if membership_id:
                    patch(
                        f"{BASE_URL}/students/batch-memberships/{membership_id}/",
                        {"batch": batch_id},
                        "Patch Batch onto Main Student"
                    )

        else:
            # NORMAL student  not in main_students
            payload = {
                "user": user_map.get(s["student_id"]),
                "is_active": False,
            }

            res = post(url, payload, "Normal Student")
            if res:
                student_id = res["id"]

                class_id = s.get("class_id")
                batch_id = batch_map.get(int(class_id)) if class_id and str(class_id).isdigit() else None
                if batch_id:
                    create_batch_membership(student_id, batch_id, False)

def normalize_wing(value):
    if not value:
        return None

    value = value.strip().lower()

    mapping = {
        "army wing": "army",
        "army": "army",

        "navy wing": "navy",
        "navy": "navy",

        "air force wing": "air_force",
        "air force": "air_force",

        "civil wing": "civil",
        "civil": "civil",

        "school wing": "school",
        "school": "school",
    }

    return mapping.get(value)

def normalize_marital_status_teacher(val):
    if not val:
        return None
    return MARITAL_STATUS_TEACHER_MAP.get(val.strip().lower()) or None
 

# TEACHERS  →  accounts/users/  with role_slug=instructors
def create_teachers():
    for t in data.get("teachers", []):
        key = t["id"]
 
        # Rank lookup — designation_id maps to rank_map
        rank_id_raw = t.get("designation_id")
        rank_id = None
        if rank_id_raw:
            try:
                rank_id = rank_map.get(int(rank_id_raw))
            except (ValueError, TypeError):
                pass
 
        # Fallback email
        email = t.get("email") or f"teacher{key}@dipstick.com"
 
        payload = {
            # Auth
            "email":            email,
            "password":         "12345678",
            "role_slug":        "instructors",       # ← assigns instructor role
 
            # Identity
            "full_name":        t.get("name"),
            "short_name":       t.get("sname") or None,
            "personal_number":  t.get("pnumber") or None,
 
            # Rank
            "rank":             rank_id,
 
            # Contact
            "phone":            t.get("phone") or None,
            "national_id":      t.get("national_id") or None,
 
            # Personal
            "gender":           t.get("gender") or None,
            "blood_group":      normalize_blood_group(t.get("blood_group")),
            "marital_status":   normalize_marital_status_teacher(t.get("mstatus")),
            "date_of_marriage": clean_date(t.get("dom")),
            "religion":         t.get("religion") or None,
 
            # Birth
            "birth_date":       clean_date(t.get("dob")),
            "place_of_birth":   clean_date(t.get("pob")),   # pob may be "0000-00-00" → clean_date returns None
            "country":          t.get("country") or None,
 
            # Address
            "present_address":  t.get("present_address") or None,
            "permanent_address":t.get("permanent_address") or None,
 
            # Organization
            "current_unit":     t.get("cunit") or None,
            "parent_unit_auth": t.get("punit") or None,
            "wing":             normalize_wing(t.get("wing")),
            "appointment":      t.get("appointment") or None,
            "joining_date":     clean_date(t.get("joining_date")),
            "date_of_enrolment":clean_date(t.get("doe")),
            "current_status":   "active" if t.get("status") == 1 else "inactive",
        }
 
        res = post(f"{BASE_URL}/accounts/users/", payload, f"Teacher id={key}")
        if res:
            teacher_map[key] = res["id"]
            print(f"  ✓ Teacher created: {t.get('name')} → user_id={res['id']}")
 


# -----------------------
# EXAM GRADES
# -----------------------
def create_exam_grades():
    for g in data.get("grades", []):  # adjust key if different in data.json
        payload = {
            "b_side_grade": g.get("bside_grade"),
            "y_side_grade": g.get("yside_grade"),
            "grade_point":  g.get("point"),
            "mark_from":    int(g["mark_from"]),
            "mark_to":      int(g["mark_to"]),
            "note":         g.get("note") or None,
        }

        res = post(f"{BASE_URL}/exams/exam-grades/", payload, f"ExamGrade id={g['id']}")
        if res:
            exam_grade_map[g["id"]] = res["id"]
            print(f"  ✓ ExamGrade created: {g.get('bside_grade')} ({g['mark_from']}-{g['mark_to']}) → id={res['id']}")



# -----------------------
# EVENTS
# -----------------------
def create_events():
    for e in data.get("events", []):
        payload = {
            "title":          e.get("title"),
            "place":          e.get("event_place") or None,
            "from_date":      clean_date(e.get("event_from")),
            "to_date":        clean_date(e.get("event_to")),
            "note":           e.get("note") or None,
            "is_view_on_web": bool(e.get("is_view_on_web", 1)),
        }

        res = post(f"{BASE_URL}/noticeboards/events/", payload, f"Event id={e['id']}")
        if res:
            event_map[e["id"]] = res["id"]
            print(f"  ✓ Event created: {e.get('title')} → id={res['id']}")


# -----------------------
# SAVE STATE
# -----------------------
def save_state():
    state = {
        "rank_map":             rank_map,
        "student_type_map":     student_type_map,
        "course_map":           course_map,
        "batch_map":            batch_map,
        "user_map":             {str(k): v for k, v in user_map.items()},
        "student_map":          {str(k): v for k, v in student_map.items()},
        "batch_membership_map": {str(k): v for k, v in batch_membership_map.items()},
        "teacher_map":          {str(k): v for k, v in teacher_map.items()}, 
        "exam_grade_map": {str(k): v for k, v in exam_grade_map.items()},
        "event_map": {str(k): v for k, v in event_map.items()},
    }
 
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)
 
    print("STATE SAVED")



# -----------------------
# RUN
# -----------------------
if __name__ == "__main__":
    create_ranks()
    create_student_types()
    create_courses()
    create_modules()
    create_subjects()
    create_batches()

    create_users()
    create_students()
    create_teachers()        
    create_exam_grades()
    create_events()
    save_state()

    print("RESTORE COMPLETED")
