-- Seed data for QBank system
-- Insert sample questions with IRT parameters

-- Insert item banks
INSERT INTO item_banks (name, description, subject, grade_level, test_type) VALUES
('SAT Mathematics', 'SAT Math question bank with 1500+ items', 'Mathematics', 'High School', 'SAT'),
('ACT Science', 'ACT Science reasoning questions', 'Science', 'High School', 'ACT'),
('GRE Verbal', 'GRE Verbal reasoning and vocabulary', 'English', 'Graduate', 'GRE'),
('AP Calculus BC', 'Advanced Placement Calculus BC questions', 'Mathematics', 'High School', 'AP'),
('GMAT Quantitative', 'GMAT Quantitative reasoning questions', 'Mathematics', 'Graduate', 'GMAT');

-- Insert Mathematics questions with varied IRT parameters
INSERT INTO questions (content, subject, topic, difficulty_level, discrimination, difficulty, guessing, question_type, options, correct_answer, explanation, tags, cognitive_level, item_bank_id) VALUES
-- Easy Algebra questions
('Solve for x: 2x + 5 = 13', 'Mathematics', 'Algebra', 'easy', 1.2, -1.5, 0.25, 'multiple_choice', '["4", "5", "6", "7"]', '4', 'Subtract 5 from both sides: 2x = 8, then divide by 2: x = 4', '["linear_equation", "basic_algebra"]', 'application', 1),
('What is the value of 3x when x = 7?', 'Mathematics', 'Algebra', 'very_easy', 0.8, -2.0, 0.25, 'multiple_choice', '["14", "21", "28", "35"]', '21', 'Multiply: 3 × 7 = 21', '["multiplication", "substitution"]', 'comprehension', 1),
('Simplify: 5x + 3x', 'Mathematics', 'Algebra', 'very_easy', 0.9, -2.2, 0.25, 'multiple_choice', '["3x", "5x", "8x", "15x"]', '8x', 'Combine like terms: 5x + 3x = 8x', '["like_terms", "simplification"]', 'application', 1),

-- Medium Algebra questions
('Solve the system: x + y = 10, x - y = 4', 'Mathematics', 'Algebra', 'medium', 1.5, 0.0, 0.20, 'multiple_choice', '["x=7, y=3", "x=6, y=4", "x=5, y=5", "x=8, y=2"]', 'x=7, y=3', 'Add equations: 2x = 14, so x = 7. Substitute: y = 3', '["systems_of_equations", "elimination"]', 'analysis', 1),
('Factor: x² - 5x + 6', 'Mathematics', 'Algebra', 'medium', 1.3, 0.3, 0.22, 'multiple_choice', '["(x-1)(x-6)", "(x-2)(x-3)", "(x-2)(x-4)", "(x-1)(x-5)"]', '(x-2)(x-3)', 'Find factors of 6 that add to -5: -2 and -3', '["factoring", "quadratics"]', 'application', 1),

-- Hard Algebra questions
('Find the sum of roots of x³ - 2x² - 5x + 6 = 0', 'Mathematics', 'Algebra', 'hard', 1.8, 1.5, 0.18, 'multiple_choice', '["0", "1", "2", "3"]', '2', 'By Vieta''s formulas, sum of roots = -(-2)/1 = 2', '["polynomials", "vietas_formulas"]', 'analysis', 1),
('If log₂(x) + log₂(x-2) = 3, find x', 'Mathematics', 'Algebra', 'hard', 2.0, 1.8, 0.15, 'multiple_choice', '["2", "3", "4", "5"]', '4', 'log₂(x(x-2)) = 3, so x(x-2) = 8, x² - 2x - 8 = 0, x = 4', '["logarithms", "quadratic_equation"]', 'synthesis', 1),

-- Geometry questions
('What is the area of a circle with radius 5?', 'Mathematics', 'Geometry', 'easy', 1.0, -1.0, 0.25, 'multiple_choice', '["25π", "10π", "5π", "50π"]', '25π', 'Area = πr² = π(5)² = 25π', '["circle", "area"]', 'application', 1),
('Find the perimeter of a rectangle with length 8 and width 5', 'Mathematics', 'Geometry', 'very_easy', 0.7, -2.3, 0.25, 'multiple_choice', '["13", "26", "40", "52"]', '26', 'Perimeter = 2(length + width) = 2(8 + 5) = 26', '["rectangle", "perimeter"]', 'application', 1),
('In a right triangle with legs 3 and 4, find the hypotenuse', 'Mathematics', 'Geometry', 'easy', 1.1, -0.8, 0.25, 'multiple_choice', '["5", "6", "7", "8"]', '5', 'By Pythagorean theorem: c² = 3² + 4² = 9 + 16 = 25, c = 5', '["pythagorean_theorem", "right_triangle"]', 'application', 1),

-- Calculus questions
('Find the derivative of f(x) = x²', 'Mathematics', 'Calculus', 'easy', 1.2, -0.5, 0.20, 'multiple_choice', '["x", "2x", "x²", "2"]', '2x', 'Using power rule: d/dx(x²) = 2x', '["derivative", "power_rule"]', 'application', 1),
('Evaluate ∫2x dx', 'Mathematics', 'Calculus', 'medium', 1.4, 0.2, 0.18, 'multiple_choice', '["x² + C", "2x² + C", "x + C", "2x + C"]', 'x² + C', 'Using power rule for integration: ∫2x dx = x² + C', '["integral", "power_rule"]', 'application', 1),
('Find lim(x→0) sin(x)/x', 'Mathematics', 'Calculus', 'hard', 1.9, 1.2, 0.15, 'multiple_choice', '["0", "1", "∞", "undefined"]', '1', 'This is a standard limit: lim(x→0) sin(x)/x = 1', '["limit", "trigonometric"]', 'analysis', 1),

-- Statistics questions
('Find the mean of: 2, 4, 6, 8, 10', 'Mathematics', 'Statistics', 'very_easy', 0.8, -2.0, 0.25, 'multiple_choice', '["5", "6", "7", "8"]', '6', 'Mean = (2+4+6+8+10)/5 = 30/5 = 6', '["mean", "average"]', 'application', 1),
('What is the median of: 3, 7, 2, 9, 5?', 'Mathematics', 'Statistics', 'easy', 1.0, -1.2, 0.25, 'multiple_choice', '["3", "5", "7", "9"]', '5', 'Sort: 2, 3, 5, 7, 9. Middle value is 5', '["median", "central_tendency"]', 'application', 1),
('If P(A) = 0.3 and P(B) = 0.4, and A and B are independent, find P(A∩B)', 'Mathematics', 'Statistics', 'medium', 1.6, 0.5, 0.18, 'multiple_choice', '["0.12", "0.7", "0.3", "0.4"]', '0.12', 'For independent events: P(A∩B) = P(A) × P(B) = 0.3 × 0.4 = 0.12', '["probability", "independence"]', 'application', 1);

-- Insert Science questions
INSERT INTO questions (content, subject, topic, difficulty_level, discrimination, difficulty, guessing, question_type, options, correct_answer, explanation, tags, cognitive_level, item_bank_id) VALUES
-- Physics questions
('What is the SI unit of force?', 'Science', 'Physics', 'very_easy', 0.7, -2.5, 0.25, 'multiple_choice', '["Joule", "Newton", "Watt", "Pascal"]', 'Newton', 'The SI unit of force is the Newton (N)', '["units", "mechanics"]', 'knowledge', 2),
('If a car travels 120 km in 2 hours, what is its average speed?', 'Science', 'Physics', 'easy', 1.0, -1.3, 0.25, 'multiple_choice', '["30 km/h", "60 km/h", "90 km/h", "120 km/h"]', '60 km/h', 'Average speed = distance/time = 120 km / 2 h = 60 km/h', '["kinematics", "speed"]', 'application', 2),
('What is the acceleration due to gravity on Earth?', 'Science', 'Physics', 'easy', 0.9, -1.5, 0.25, 'multiple_choice', '["9.8 m/s²", "10 m/s", "9.8 km/s²", "98 m/s²"]', '9.8 m/s²', 'Standard acceleration due to gravity is approximately 9.8 m/s²', '["gravity", "constants"]', 'knowledge', 2),

-- Chemistry questions
('What is the chemical symbol for gold?', 'Science', 'Chemistry', 'very_easy', 0.6, -2.8, 0.25, 'multiple_choice', '["Go", "Gd", "Au", "Ag"]', 'Au', 'Gold''s chemical symbol is Au (from Latin: aurum)', '["elements", "periodic_table"]', 'knowledge', 2),
('How many protons does carbon have?', 'Science', 'Chemistry', 'easy', 0.9, -1.4, 0.25, 'multiple_choice', '["4", "6", "8", "12"]', '6', 'Carbon''s atomic number is 6, meaning it has 6 protons', '["atomic_structure", "elements"]', 'knowledge', 2),
('What type of bond forms between Na and Cl in NaCl?', 'Science', 'Chemistry', 'medium', 1.4, 0.3, 0.20, 'multiple_choice', '["Covalent", "Ionic", "Metallic", "Hydrogen"]', 'Ionic', 'Sodium (metal) and chlorine (nonmetal) form an ionic bond', '["chemical_bonding", "compounds"]', 'comprehension', 2),

-- Biology questions
('What is the powerhouse of the cell?', 'Science', 'Biology', 'very_easy', 0.5, -3.0, 0.25, 'multiple_choice', '["Nucleus", "Mitochondria", "Ribosome", "Chloroplast"]', 'Mitochondria', 'Mitochondria produce ATP, the cell''s energy currency', '["cell_biology", "organelles"]', 'knowledge', 2),
('What process do plants use to make food?', 'Science', 'Biology', 'easy', 0.8, -1.6, 0.25, 'multiple_choice', '["Respiration", "Photosynthesis", "Digestion", "Fermentation"]', 'Photosynthesis', 'Plants use photosynthesis to convert light energy into chemical energy', '["plant_biology", "metabolism"]', 'knowledge', 2),
('Which base is NOT found in DNA?', 'Science', 'Biology', 'medium', 1.5, 0.4, 0.18, 'multiple_choice', '["Adenine", "Thymine", "Uracil", "Guanine"]', 'Uracil', 'Uracil is found in RNA, not DNA. DNA contains thymine instead', '["molecular_biology", "nucleic_acids"]', 'comprehension', 2);

-- Insert English questions
INSERT INTO questions (content, subject, topic, difficulty_level, discrimination, difficulty, guessing, question_type, options, correct_answer, explanation, tags, cognitive_level, item_bank_id) VALUES
-- Grammar questions
('Choose the correct form: "Neither of the students ___ ready."', 'English', 'Grammar', 'medium', 1.3, 0.2, 0.20, 'multiple_choice', '["is", "are", "were", "be"]', 'is', 'Neither is singular and takes a singular verb', '["subject_verb_agreement", "grammar"]', 'application', 3),
('Identify the verb tense: "She has been studying all day."', 'English', 'Grammar', 'medium', 1.4, 0.4, 0.18, 'multiple_choice', '["Present perfect", "Past perfect", "Present perfect continuous", "Past continuous"]', 'Present perfect continuous', 'Has been + -ing indicates present perfect continuous', '["verb_tenses", "grammar"]', 'analysis', 3),

-- Vocabulary questions
('What does "ubiquitous" mean?', 'English', 'Vocabulary', 'hard', 1.7, 1.3, 0.15, 'multiple_choice', '["Rare", "Present everywhere", "Mysterious", "Ancient"]', 'Present everywhere', 'Ubiquitous means present, appearing, or found everywhere', '["vocabulary", "advanced"]', 'knowledge', 3),
('Choose the synonym for "ephemeral"', 'English', 'Vocabulary', 'hard', 1.8, 1.5, 0.15, 'multiple_choice', '["Eternal", "Temporary", "Beautiful", "Complex"]', 'Temporary', 'Ephemeral means lasting for a very short time', '["synonyms", "vocabulary"]', 'comprehension', 3);

-- Insert History questions
INSERT INTO questions (content, subject, topic, difficulty_level, discrimination, difficulty, guessing, question_type, options, correct_answer, explanation, tags, cognitive_level, item_bank_id) VALUES
('In which year did World War II end?', 'History', 'World History', 'easy', 0.9, -1.2, 0.25, 'multiple_choice', '["1943", "1944", "1945", "1946"]', '1945', 'World War II ended in 1945 with the surrender of Japan', '["world_war_2", "dates"]', 'knowledge', NULL),
('Who was the first President of the United States?', 'History', 'US History', 'very_easy', 0.5, -3.0, 0.25, 'multiple_choice', '["Thomas Jefferson", "George Washington", "John Adams", "Benjamin Franklin"]', 'George Washington', 'George Washington served as the first U.S. President from 1789-1797', '["presidents", "founding_fathers"]', 'knowledge', NULL);

-- Update item bank statistics
UPDATE item_banks ib
SET total_items = (SELECT COUNT(*) FROM questions q WHERE q.item_bank_id = ib.id),
    active_items = (SELECT COUNT(*) FROM questions q WHERE q.item_bank_id = ib.id AND q.is_active = true),
    average_difficulty = (SELECT AVG(difficulty) FROM questions q WHERE q.item_bank_id = ib.id),
    average_discrimination = (SELECT AVG(discrimination) FROM questions q WHERE q.item_bank_id = ib.id);

-- Insert sample test sessions (for demonstration)
INSERT INTO test_sessions (user_id, session_token, test_type, subject, target_questions, ability_estimate, ability_se, status, questions_answered, correct_answers) VALUES
('user_001', 'token_001', 'SAT', 'Mathematics', 20, 0.5, 0.4, 'completed', 20, 14),
('user_002', 'token_002', 'ACT', 'Science', 25, -0.2, 0.5, 'completed', 25, 15),
('user_003', 'token_003', 'GRE', 'English', 30, 1.2, 0.3, 'active', 15, 12);

-- Insert sample responses (for demonstration)
INSERT INTO responses (session_id, question_id, user_id, given_answer, is_correct, response_time, ability_before, ability_after, information_value) VALUES
(1, 1, 'user_001', '4', true, 45.2, 0.0, 0.3, 1.2),
(1, 2, 'user_001', '21', true, 32.1, 0.3, 0.5, 0.9),
(1, 4, 'user_001', 'x=7, y=3', true, 68.4, 0.5, 0.6, 1.5),
(2, 16, 'user_002', 'Newton', true, 25.3, 0.0, 0.2, 0.8),
(2, 17, 'user_002', '60 km/h', true, 42.7, 0.2, 0.3, 1.0);

-- Initialize exposure control for all questions
INSERT INTO exposure_control (question_id, target_exposure, current_exposure, selection_parameter)
SELECT id, 0.25, 0.0, 1.0
FROM questions
ON CONFLICT (question_id) DO NOTHING;

-- Create initial calibration run record
INSERT INTO calibration_runs (run_id, status, calibration_method, questions_calibrated, total_responses_used) VALUES
('initial_calibration_001', 'completed', 'MMLE', 30, 150);

-- Add some variety to question parameters for more realistic distribution
UPDATE questions SET 
    discrimination = 0.5 + RANDOM() * 2.0,
    difficulty = -3.0 + RANDOM() * 6.0,
    guessing = 0.15 + RANDOM() * 0.20
WHERE id > 10;

-- Update exposure statistics for some questions
UPDATE questions SET 
    total_responses = FLOOR(50 + RANDOM() * 450),
    correct_responses = FLOOR(total_responses * (0.3 + RANDOM() * 0.5))
WHERE id <= 10;

-- Calculate and update exposure rates
UPDATE questions SET 
    exposure_rate = LEAST(0.25, total_responses::FLOAT / GREATEST((SELECT SUM(questions_answered) FROM test_sessions), 1))
WHERE total_responses > 0;

-- Final statistics update
UPDATE questions SET
    average_response_time = 30 + RANDOM() * 90
WHERE total_responses > 0;

-- Commit message
-- COMMIT;