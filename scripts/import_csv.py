import csv

from pypinyin import pinyin, lazy_pinyin, Style

former_codes = dict()

with open('former_code.csv', mode='r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        former_codes[row['old_code']] = row['new_code']

departments = set()
teachers = set()
categories = set()
courses = set()
encoding = 'utf-8'
data_dir = '../data'
semester = '2021-2022-3'
course_department = dict()


def regulate_department(raw_name: str) -> str:  # 将系统一到学院层面
    if any(raw_name == x for x in ['软件学院', '微电子学院', '计算机科学与工程系']):
        return '电子信息与电气工程学院'
    if raw_name == '高分子科学与工程系':
        return '化学化工学院'
    return raw_name


with open(f'{data_dir}/{semester}.csv', mode='r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)

    for row in reader:
        department = row['开课院系']
        if department == '研究生院':  # 跳过所有的研究生课程（主要原因是没有main_teacher字段）
            continue

        teacher_groups = row['合上教师']
        if teacher_groups == 'QT2002231068/THIERRY; Fine; VAN CHUNG/无[外国语学院]':
            teacher_groups = 'QT2002231068/THIERRY, Fine, VAN CHUNG/无[外国语学院]'

        teacher_groups = teacher_groups.split(';')
        tid_groups = []
        for teacher in teacher_groups:
            try:
                tid, name, title = teacher.split('/')
            except ValueError:
                print("\"" + teacher + "\"")
                continue
            department = regulate_department(title[title.find('[') + 1:-1])
            title = title[0:title.find('[')]
            my_pinyin = ''.join(lazy_pinyin(name))
            abbr_pinyin = ''.join([i[0] for i in pinyin(name, style=Style.FIRST_LETTER)])
            teachers.add((tid, name, title, department, my_pinyin, abbr_pinyin, semester))
            tid_groups.append(tid)
            departments.add(department)
        department = regulate_department(row['开课院系'])

        departments.add(department)
        name = row['课程名称']
        code = row['课程号']

        category = row['通识课归属模块'].split(',')[0]
        if category == "" and department == '研究生院':
            category = '研究生'
            name = name.removesuffix('（研）')
        if category == "" and row['年级'] == "0":
            if row['课程号'].startswith('SP'):
                category = '新生研讨'
            elif any(x in row['选课备注'] for x in ['重修班', '不及格', '面向民族生', '面向留学生']):
                category = ''
            else:
                category = '通选'
        if category == "" and any(code.startswith(x) for x in ['PE001C', 'PE002C', 'PE003C', 'PE004C']):
            category = '体育'
        if category.find('（致远）') != -1:
            category = category.removesuffix('（致远）')
        categories.add(category)
        if category == "" and code in former_codes:
            code = former_codes[code]
        main_teacher = row['任课教师'].split('|')[0] if row['任课教师'] else tid_groups[0]
        if department != '致远学院':
            course_department[(code, main_teacher)] = department
        # code	name	credit	department	category    main_teacher	teacher_group
        courses.add(
            (code, name, row['学分'], department, category,
             main_teacher, ';'.join(tid_groups), semester))

unique_courses = set()
for course in courses:
    other_dept = course_department.get((course[0], course[5]), '')
    if course[3] == '致远学院' and other_dept != '' and other_dept != '致远学院':
        print(course)
        continue
    unique_courses.add(course)

print(len(teachers), len(departments), len(categories), len(courses))

with open(f'{data_dir}/Teachers.csv', mode='w', encoding=encoding, newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['tid', 'name', 'title', 'department', 'pinyin', 'abbr_pinyin', 'last_semester'])
    writer.writerows(teachers)

with open(f'{data_dir}/Categories.csv', mode='w', encoding=encoding, newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['name'])
    writer.writerows([[category] for category in categories])

with open(f'{data_dir}/Departments.csv', mode='w', encoding=encoding, newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['name'])
    writer.writerows([[department] for department in departments])

with open(f'{data_dir}/Courses.csv', mode='w', encoding=encoding, newline='') as f:
    writer = csv.writer(f)
    writer.writerow(
        ['code', 'name', 'credit', 'department', 'category', 'main_teacher', 'teacher_group', 'last_semester'])
    writer.writerows(unique_courses)
