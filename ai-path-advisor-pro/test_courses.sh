#!/bin/bash

echo "=== Testing AI Path Advisor Course System ==="
echo ""

echo "1. Available Majors:"
curl -s http://localhost:8000/courses/majors | python3 -m json.tool
echo ""

echo "2. Computer Science Courses:"
curl -s http://localhost:8000/courses/major/cs | python3 -c "import sys, json; courses = json.load(sys.stdin); [print(f'  - {c[\"id\"]}: {c[\"name\"]}') for c in courses[:5]]"
echo ""

echo "3. Sample Course Detail (CS201 - Data Structures):"
curl -s http://localhost:8000/courses/major/cs/course/CS201 | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f'  Course: {data[\"name\"]}')
print(f'  Credits: {data[\"credits\"]}')
print(f'  Description: {data[\"description\"]}')
print('  Topics (first 3 weeks):')
for topic in data['syllabus']['topics'][:3]:
    print(f'    Week {topic[\"week\"]}: {topic[\"topic\"]}')
"
echo ""

echo "4. Generate CS Course Roadmap:"
curl -s http://localhost:8000/courses/major/cs/roadmap | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f'  Total Semesters: {data[\"total_semesters\"]}')
print(f'  Total Courses: {data[\"total_courses\"]}')
print('  Semester 1 Courses:', data['roadmap'][0]['courses'])
"
echo ""

echo "=== Test Complete! ==="
echo "Access the interactive API docs at: http://localhost:8000/docs"