# -*- coding: utf-8 -*-
""" DOCSTRING
"""
import datetime
import json
import random
import numpy as np
from bs4 import BeautifulSoup

SAMPLE_RESPONSES = json.load(open("references/sample_responses.json", "r", encoding="utf-8"))
RANDOM_SEED = 4232
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
n_students = 100

# Each  allows us to generate sample data that looks more normal
id_scales = {"term_id": {"scale": 10, "offset": 10},
             "course_id": {"scale": 1000, "offset": 700},
             "user_id": {"scale": 10000, "offset": 500},
             "assignment_group_id": {"scale": 1000, "offset": 500},
             "section_id": {"scale": 100, "offset": 100},
             "folder_id": {"scale": 1000, "offset": 1000},
             "file_id": {"scale": 1000, "offset": 750},
             "enrollment_id": {"scale": 1000, "offset": 500},
             "assignment_id": {"scale": 1000, "offset": 500},
             "submission_id": {"scale": 10000, "offset": 1000},
             }

id_cursor = {key: random.randint(id_scales[key]["scale"], id_scales[key]["scale"]*10 -1) for key in id_scales}

def next_id(key):
    id_cursor[key] += random.randint(1, id_scales[key]["offset"])
    return id_cursor[key]


with open("library/firstnames_f.json", "r", encoding="utf-8") as f:
    firstnames_f = json.load(f)[0:2000]
with open("library/firstnames_m.json", "r", encoding="utf-8") as f:
    firstnames_m = json.load(f)[0:2000]
with open("library/surnames.json", "r", encoding="utf-8") as f:
    lastnames = json.load(f)[0:1500]

with open("references/rest_api_all_resources.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")
    rest_api_all_resources_for_copilot = soup.get_text() # load all resources for copilot

def generate_person():
    sis_id = random.randint(10000000000, 99999999999)
    gender = random.choice(["F", "M"])
    if gender == "F":
        first_name = random.choice(firstnames_f)
        if random.random() < 0.6:
            middle_name = random.choice(firstnames_f)
            if random.random() < 0.5:
                middle_name = middle_name[0]
        elif random.random() < 0.9:
            middle_name = random.choice(lastnames)
            if random.random() < 0.5:
                middle_name = middle_name[0]
        else:
            middle_name = ""
        last_name = random.choice(lastnames)
        if random.random() < 0.45:
            if random.random() < 0.8:
                last_name += "-" + random.choice(lastnames)
            else:
                last_name += " " + random.choice(lastnames)
    else:
        first_name = random.choice(firstnames_m)
        if random.random() < 0.7:
            middle_name = random.choice(firstnames_m)
            if random.random() < 0.5:
                middle_name = middle_name[0]
        elif random.random() < 0.9:
            middle_name = random.choice(lastnames)
            if random.random() < 0.5:
                middle_name = middle_name[0]
        else:
            middle_name = ""
        last_name = random.choice(lastnames)
        if random.random() < 0.12:
            if random.random() < 0.8:
                last_name += "-" + random.choice(lastnames)
            else:
                last_name += " " + random.choice(lastnames)
    if random.random() < 0.02:
        first_name = first_name.upper()
        middle_name = middle_name.upper()
        last_name = last_name.upper()
    elif random.random() < 0.027:
        first_name = first_name.lower()
        middle_name = middle_name.lower()
        last_name = last_name.lower()
    if random.random() < 0.01:
        gender = "N"

    # Returns user like object from Canvas API (https://canvas.instructure.com/doc/api/users.html)
    user = {"id": next_id("user_id"),
            "name": first_name + " " + last_name,
            "sortable_name": last_name + ", " + first_name,
            "last_name": last_name,
            "first_name": first_name,
            "short_name": first_name,
            "sis_user_id": sis_id,
            "sis_import_id": None,
            "integration_id": None,
            "login_id": str(first_name[0].lower() + last_name.lower()).replace(" ", "") + str(random.randint(1, 999)),
            "avatar_url": "https://placekitten.com/100/100",
            "enrollments": [],
            "email": first_name.lower()[0].replace(" ","") + last_name.lower().replace(" ", "") + "@cba.slu.edu",
            "locale": "en",
            # minus a random number of hours between 0 and 7 days (604800 seconds) in iso format
            "last_login": (datetime.datetime.now() - datetime.timedelta(seconds=random.randint(0, 604800))).isoformat(),
            "time_zone": "America/Los_Angeles"}
    return user

students = []
faculty = []
for i in range(n_students):
    students.append(generate_person())
    if random.random() < 0.1:
        faculty.append(generate_person())

print(students)
print(faculty)

for student in students:
    print (student)




