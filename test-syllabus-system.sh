#!/bin/bash

echo "========================================"
echo "SYLLABUS MANAGEMENT SYSTEM TEST"
echo "========================================"
echo ""

# Backend must be running at localhost:8000
API_BASE="http://localhost:8000"

echo "1. Testing syllabus endpoints..."
echo "---------------------------------"

# Check if backend is running
echo "Checking if backend is running..."
curl -s "$API_BASE/" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Backend is not running. Please start it first:"
    echo "   cd ai-path-advisor-pro/backend && uvicorn main:app --reload"
    exit 1
fi
echo "✅ Backend is running"
echo ""

# Check syllabus stats
echo "2. Getting syllabus statistics..."
echo "---------------------------------"
curl -s "$API_BASE/syllabus/stats" | python3 -m json.tool
echo ""

# Check if CS101 has a syllabus
echo "3. Checking if CS101 has a syllabus..."
echo "---------------------------------"
curl -s "$API_BASE/syllabus/check/CS101" | python3 -m json.tool
echo ""

# List all syllabi
echo "4. Listing all uploaded syllabi..."
echo "---------------------------------"
curl -s "$API_BASE/syllabus/list" | python3 -m json.tool
echo ""

echo "5. Creating sample syllabus file..."
echo "---------------------------------"
cat > sample_syllabus.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>CS101 - Introduction to Programming</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h1 { color: #333; }
        h2 { color: #666; margin-top: 30px; }
        .info { background: #f0f0f0; padding: 10px; margin: 10px 0; }
    </style>
</head>
<body>
    <h1>CS101 - Introduction to Programming</h1>
    
    <div class="info">
        <strong>Instructor:</strong> Prof. Michael Chen<br>
        <strong>Credits:</strong> 4<br>
        <strong>Meeting Time:</strong> TTh 10:30 AM - 12:00 PM<br>
        <strong>Location:</strong> Computer Science Building 110
    </div>
    
    <h2>Course Description</h2>
    <p>Introduction to programming concepts using Python. Topics include variables, 
    control structures, functions, data structures, object-oriented programming, 
    and algorithm development.</p>
    
    <h2>Learning Objectives</h2>
    <ul>
        <li>Write, test, and debug Python programs</li>
        <li>Use fundamental programming constructs</li>
        <li>Implement basic data structures</li>
        <li>Apply object-oriented programming principles</li>
        <li>Develop algorithms to solve computational problems</li>
    </ul>
    
    <h2>Grading</h2>
    <ul>
        <li>Programming Projects: 30%</li>
        <li>Homework: 20%</li>
        <li>Lab Exercises: 15%</li>
        <li>Midterm: 15%</li>
        <li>Final: 15%</li>
        <li>Participation: 5%</li>
    </ul>
    
    <h2>Schedule</h2>
    <table border="1" cellpadding="5" style="border-collapse: collapse;">
        <tr><th>Week</th><th>Topic</th><th>Assignment</th></tr>
        <tr><td>1</td><td>Introduction to Python</td><td>Lab 1</td></tr>
        <tr><td>2</td><td>Variables and Expressions</td><td>HW 1</td></tr>
        <tr><td>3</td><td>Conditional Execution</td><td>Lab 2</td></tr>
        <tr><td>4</td><td>Loops</td><td>Project 1</td></tr>
        <tr><td>5</td><td>Functions</td><td>HW 2</td></tr>
        <tr><td>6</td><td>Lists and Tuples</td><td>Midterm</td></tr>
        <tr><td>7</td><td>Dictionaries</td><td>Lab 3</td></tr>
        <tr><td>8</td><td>File I/O</td><td>Project 2</td></tr>
        <tr><td>9</td><td>Classes and Objects</td><td>HW 3</td></tr>
        <tr><td>10</td><td>Inheritance</td><td>Lab 4</td></tr>
        <tr><td>11</td><td>Recursion</td><td>HW 4</td></tr>
        <tr><td>12</td><td>Algorithm Analysis</td><td>Project 3</td></tr>
        <tr><td>13</td><td>Advanced Topics</td><td>Lab 5</td></tr>
        <tr><td>14</td><td>Review</td><td>Practice Exam</td></tr>
        <tr><td>15</td><td>Final Exam</td><td>-</td></tr>
    </table>
</body>
</html>
EOF
echo "✅ Created sample_syllabus.html"
echo ""

echo "6. Uploading sample syllabus for CS101..."
echo "-----------------------------------------"
curl -X POST "$API_BASE/syllabus/upload/CS101" \
     -F "file=@sample_syllabus.html" \
     -F "description=Introduction to Programming course syllabus" \
     2>/dev/null | python3 -m json.tool
echo ""

echo "7. Checking CS101 syllabus metadata..."
echo "---------------------------------------"
curl -s "$API_BASE/syllabus/metadata/CS101" | python3 -m json.tool
echo ""

echo "========================================"
echo "TEST COMPLETE!"
echo "========================================"
echo ""
echo "You can now:"
echo "1. Open syllabus-display.html?course=CS101 to view the uploaded syllabus"
echo "2. Upload more syllabi through the web interface"
echo "3. Access syllabi via the API endpoints"
echo ""
echo "API Endpoints:"
echo "  POST   /syllabus/upload/{course_id}    - Upload syllabus"
echo "  GET    /syllabus/view/{course_id}      - View syllabus"
echo "  GET    /syllabus/download/{course_id}  - Download syllabus"
echo "  GET    /syllabus/metadata/{course_id}  - Get metadata"
echo "  GET    /syllabus/check/{course_id}     - Check if exists"
echo "  GET    /syllabus/list                  - List all syllabi"
echo "  GET    /syllabus/stats                 - Get statistics"
echo "  DELETE /syllabus/delete/{course_id}    - Archive syllabus"