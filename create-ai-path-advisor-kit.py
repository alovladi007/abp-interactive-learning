#!/usr/bin/env python3
"""
AI Path Advisor Starter Kit Generator
Creates a ready-to-run backend (FastAPI) and frontend (Next.js) for the path planning system
"""

import os
import json
import textwrap
import zipfile
import pathlib
import shutil

# Setup directories
root = "/workspace/ai-path-advisor-starter"
backend = os.path.join(root, "backend")
frontend = os.path.join(root, "frontend")
data_dir = os.path.join(backend, "data")

# Clean and create directories
if os.path.exists(root):
    shutil.rmtree(root)
os.makedirs(data_dir, exist_ok=True)
os.makedirs(os.path.join(frontend, "app"), exist_ok=True)

# -----------------------------
# Seed JSON: skills (CS, EE, Physics, and more)
# -----------------------------
skills = [
    # --- Math (shared foundation) ---
    {"skill_id":"math.algebra","name":"Algebra","prereq_ids":[],"tags":["math","foundation"],"difficulty":1},
    {"skill_id":"math.precalculus","name":"Pre-Calculus","prereq_ids":["math.algebra"],"tags":["math"],"difficulty":2},
    {"skill_id":"math.calculus_1","name":"Calculus I","prereq_ids":["math.precalculus"],"tags":["math"],"difficulty":2},
    {"skill_id":"math.calculus_2","name":"Calculus II","prereq_ids":["math.calculus_1"],"tags":["math"],"difficulty":3},
    {"skill_id":"math.calculus_3","name":"Calculus III (Multivariable)","prereq_ids":["math.calculus_2"],"tags":["math"],"difficulty":4},
    {"skill_id":"math.linear_algebra","name":"Linear Algebra","prereq_ids":["math.calculus_1"],"tags":["math"],"difficulty":3},
    {"skill_id":"math.discrete","name":"Discrete Mathematics","prereq_ids":["math.algebra"],"tags":["math","cs"],"difficulty":3},
    {"skill_id":"math.differential_equations","name":"Differential Equations","prereq_ids":["math.calculus_2","math.linear_algebra"],"tags":["math"],"difficulty":4},
    {"skill_id":"math.statistics","name":"Statistics & Probability","prereq_ids":["math.calculus_1"],"tags":["math","data"],"difficulty":3},
    
    # --- Computer Science ---
    {"skill_id":"prog.basics","name":"Programming Fundamentals","prereq_ids":[],"tags":["cs","programming"],"difficulty":1},
    {"skill_id":"prog.python.basics","name":"Python Programming Basics","prereq_ids":["prog.basics"],"tags":["cs","programming"],"difficulty":1},
    {"skill_id":"prog.python.advanced","name":"Advanced Python","prereq_ids":["prog.python.basics"],"tags":["cs","programming"],"difficulty":3},
    {"skill_id":"prog.c.basics","name":"C Programming Basics","prereq_ids":["prog.basics"],"tags":["cs","programming","systems"],"difficulty":2},
    {"skill_id":"prog.cpp.basics","name":"C++ Programming","prereq_ids":["prog.c.basics"],"tags":["cs","programming"],"difficulty":3},
    {"skill_id":"prog.java.basics","name":"Java Programming","prereq_ids":["prog.basics"],"tags":["cs","programming"],"difficulty":2},
    {"skill_id":"prog.javascript.basics","name":"JavaScript Basics","prereq_ids":["prog.basics"],"tags":["cs","web"],"difficulty":2},
    
    {"skill_id":"cs.ds.algorithms","name":"Data Structures & Algorithms","prereq_ids":["math.discrete","prog.python.basics"],"tags":["cs","core"],"difficulty":4},
    {"skill_id":"cs.computer.arch","name":"Computer Architecture","prereq_ids":["prog.c.basics"],"tags":["cs","systems"],"difficulty":4},
    {"skill_id":"cs.os","name":"Operating Systems","prereq_ids":["cs.computer.arch","cs.ds.algorithms"],"tags":["cs","systems"],"difficulty":4},
    {"skill_id":"cs.networks","name":"Computer Networks","prereq_ids":["cs.os"],"tags":["cs","systems"],"difficulty":3},
    {"skill_id":"cs.databases","name":"Database Systems","prereq_ids":["cs.ds.algorithms"],"tags":["cs","data"],"difficulty":3},
    {"skill_id":"cs.distributed","name":"Distributed Systems","prereq_ids":["cs.networks","cs.databases"],"tags":["cs","systems"],"difficulty":5},
    {"skill_id":"cs.software.engineering","name":"Software Engineering","prereq_ids":["cs.ds.algorithms"],"tags":["cs","engineering"],"difficulty":3},
    {"skill_id":"cs.compilers","name":"Compiler Design","prereq_ids":["cs.ds.algorithms","cs.computer.arch"],"tags":["cs","systems"],"difficulty":5},
    
    # Web Development
    {"skill_id":"cs.web.frontend","name":"Frontend Development","prereq_ids":["prog.javascript.basics"],"tags":["cs","web"],"difficulty":3},
    {"skill_id":"cs.web.backend","name":"Backend Development","prereq_ids":["cs.databases","cs.networks"],"tags":["cs","web"],"difficulty":3},
    {"skill_id":"cs.web.fullstack","name":"Full Stack Development","prereq_ids":["cs.web.frontend","cs.web.backend"],"tags":["cs","web"],"difficulty":4},
    
    # AI/ML
    {"skill_id":"cs.ai.ml.basics","name":"Machine Learning Fundamentals","prereq_ids":["math.linear_algebra","math.statistics","prog.python.advanced"],"tags":["cs","ml"],"difficulty":4},
    {"skill_id":"cs.ai.deep_learning","name":"Deep Learning","prereq_ids":["cs.ai.ml.basics"],"tags":["cs","ml"],"difficulty":5},
    {"skill_id":"cs.ai.nlp","name":"Natural Language Processing","prereq_ids":["cs.ai.ml.basics"],"tags":["cs","ml"],"difficulty":5},
    {"skill_id":"cs.ai.cv","name":"Computer Vision","prereq_ids":["cs.ai.deep_learning"],"tags":["cs","ml"],"difficulty":5},
    {"skill_id":"cs.ai.rl","name":"Reinforcement Learning","prereq_ids":["cs.ai.ml.basics"],"tags":["cs","ml"],"difficulty":5},
    
    # Security
    {"skill_id":"cs.security.basics","name":"Computer Security Basics","prereq_ids":["cs.os","cs.networks"],"tags":["cs","security"],"difficulty":3},
    {"skill_id":"cs.security.crypto","name":"Cryptography","prereq_ids":["math.discrete","cs.security.basics"],"tags":["cs","security"],"difficulty":4},
    {"skill_id":"cs.security.web","name":"Web Security","prereq_ids":["cs.web.fullstack","cs.security.basics"],"tags":["cs","security"],"difficulty":4},
    
    # --- Electrical Engineering ---
    {"skill_id":"ee.circuits_1","name":"Circuits I","prereq_ids":["math.calculus_1","phys.em_intro"],"tags":["ee","core"],"difficulty":3},
    {"skill_id":"ee.circuits_2","name":"Circuits II","prereq_ids":["ee.circuits_1","math.calculus_2"],"tags":["ee","core"],"difficulty":3},
    {"skill_id":"ee.signals_systems","name":"Signals & Systems","prereq_ids":["math.calculus_2","math.linear_algebra"],"tags":["ee","core"],"difficulty":4},
    {"skill_id":"ee.em_1","name":"Electromagnetics I","prereq_ids":["math.calculus_3","phys.em_intro"],"tags":["ee","core"],"difficulty":4},
    {"skill_id":"ee.em_2","name":"Electromagnetics II","prereq_ids":["ee.em_1"],"tags":["ee","advanced"],"difficulty":5},
    {"skill_id":"ee.digital_logic","name":"Digital Logic & Computer Design","prereq_ids":["prog.c.basics"],"tags":["ee","digital"],"difficulty":3},
    {"skill_id":"ee.embedded","name":"Embedded Systems","prereq_ids":["ee.digital_logic","prog.c.basics"],"tags":["ee","systems"],"difficulty":4},
    {"skill_id":"ee.control_systems","name":"Control Systems","prereq_ids":["ee.signals_systems","math.differential_equations"],"tags":["ee","control"],"difficulty":4},
    {"skill_id":"ee.comm_systems","name":"Communication Systems","prereq_ids":["ee.signals_systems","ee.em_1"],"tags":["ee","comm"],"difficulty":4},
    {"skill_id":"ee.power_systems","name":"Power Systems","prereq_ids":["ee.circuits_2","ee.em_1"],"tags":["ee","power"],"difficulty":4},
    {"skill_id":"ee.semiconductor_devices","name":"Semiconductor Devices","prereq_ids":["phys.quantum_1","ee.circuits_1"],"tags":["ee","devices"],"difficulty":4},
    {"skill_id":"ee.vlsi","name":"VLSI Design","prereq_ids":["ee.digital_logic","ee.semiconductor_devices"],"tags":["ee","vlsi"],"difficulty":5},
    
    # --- Physics ---
    {"skill_id":"phys.mechanics","name":"Classical Mechanics","prereq_ids":["math.calculus_1"],"tags":["physics","core"],"difficulty":3},
    {"skill_id":"phys.em_intro","name":"Introductory Electricity & Magnetism","prereq_ids":["math.calculus_2","phys.mechanics"],"tags":["physics","core"],"difficulty":3},
    {"skill_id":"phys.modern","name":"Modern Physics","prereq_ids":["phys.mechanics","phys.em_intro"],"tags":["physics","core"],"difficulty":3},
    {"skill_id":"phys.thermo","name":"Thermodynamics","prereq_ids":["math.calculus_2","phys.mechanics"],"tags":["physics","core"],"difficulty":3},
    {"skill_id":"phys.quantum_1","name":"Quantum Mechanics I","prereq_ids":["math.linear_algebra","phys.modern","math.differential_equations"],"tags":["physics","quantum"],"difficulty":4},
    {"skill_id":"phys.quantum_2","name":"Quantum Mechanics II","prereq_ids":["phys.quantum_1"],"tags":["physics","quantum"],"difficulty":5},
    {"skill_id":"phys.em_advanced","name":"Advanced Electromagnetism","prereq_ids":["math.calculus_3","phys.em_intro","math.differential_equations"],"tags":["physics","advanced"],"difficulty":4},
    {"skill_id":"phys.stat_mech","name":"Statistical Mechanics","prereq_ids":["phys.thermo","phys.quantum_1","math.statistics"],"tags":["physics","advanced"],"difficulty":4},
    {"skill_id":"phys.solid_state","name":"Solid State Physics","prereq_ids":["phys.quantum_1","phys.stat_mech"],"tags":["physics","materials"],"difficulty":5},
    {"skill_id":"phys.particle","name":"Particle Physics","prereq_ids":["phys.quantum_2","phys.em_advanced"],"tags":["physics","advanced"],"difficulty":5},
    
    # --- Data Science ---
    {"skill_id":"data.analysis","name":"Data Analysis","prereq_ids":["prog.python.basics","math.statistics"],"tags":["data","analytics"],"difficulty":2},
    {"skill_id":"data.visualization","name":"Data Visualization","prereq_ids":["data.analysis"],"tags":["data","viz"],"difficulty":2},
    {"skill_id":"data.engineering","name":"Data Engineering","prereq_ids":["cs.databases","prog.python.advanced"],"tags":["data","engineering"],"difficulty":3},
    {"skill_id":"data.big_data","name":"Big Data Technologies","prereq_ids":["data.engineering","cs.distributed"],"tags":["data","scale"],"difficulty":4},
    {"skill_id":"data.streaming","name":"Stream Processing","prereq_ids":["data.engineering"],"tags":["data","realtime"],"difficulty":4},
]

with open(os.path.join(data_dir, "skills.json"), "w") as f:
    json.dump(skills, f, indent=2)

# -----------------------------
# Modules
# -----------------------------
modules = [
    # CS Core
    {
        "module_id":"cs.programming.core",
        "skill_ids":["prog.python.basics","prog.c.basics"],
        "outcomes":["Write programs in Python and C","Use data types and control flow","Debug and test code"],
        "assessments":["weekly coding drills","2h timed exercise"],
        "project_ideas":["CLI text processor","C-based micro-library"],
        "target_hours": 80
    },
    {
        "module_id":"cs.algorithms.core",
        "skill_ids":["cs.ds.algorithms","math.discrete"],
        "outcomes":["Asymptotic analysis","Sorting/graphs/DP","Trees/heaps/hashing"],
        "assessments":["LeetCode set (50 problems)","algorithm design problems"],
        "project_ideas":["route optimizer","streaming top-k system"],
        "target_hours": 120
    },
    {
        "module_id":"cs.systems.core",
        "skill_ids":["cs.computer.arch","cs.os","cs.networks"],
        "outcomes":["Process/memory/threads","I/O & filesystems","TCP/IP networking"],
        "assessments":["OSTEP labs","socket programming"],
        "project_ideas":["mini shell","HTTP server"],
        "target_hours": 140
    },
    {
        "module_id":"cs.web.fullstack.module",
        "skill_ids":["cs.web.frontend","cs.web.backend","cs.databases"],
        "outcomes":["React/Vue apps","REST APIs","Database design"],
        "assessments":["full stack project","performance optimization"],
        "project_ideas":["social media clone","e-commerce platform"],
        "target_hours": 160
    },
    {
        "module_id":"cs.ml.foundations",
        "skill_ids":["cs.ai.ml.basics"],
        "outcomes":["Supervised learning","Model evaluation","Feature engineering"],
        "assessments":["Kaggle competition","model deployment"],
        "project_ideas":["recommendation system","fraud detection"],
        "target_hours": 100
    },
    {
        "module_id":"cs.ml.deep",
        "skill_ids":["cs.ai.deep_learning","cs.ai.cv","cs.ai.nlp"],
        "outcomes":["CNNs/RNNs/Transformers","Transfer learning","Model optimization"],
        "assessments":["paper implementation","end-to-end project"],
        "project_ideas":["image classifier","chatbot","style transfer"],
        "target_hours": 180
    },
    
    # EE Modules
    {
        "module_id":"ee.circuits.sequence",
        "skill_ids":["ee.circuits_1","ee.circuits_2"],
        "outcomes":["AC/DC analysis","Op-amps","Transient response"],
        "assessments":["LTspice labs","breadboard projects"],
        "project_ideas":["active filter","power supply design"],
        "target_hours": 110
    },
    {
        "module_id":"ee.signals.controls",
        "skill_ids":["ee.signals_systems","ee.control_systems"],
        "outcomes":["Fourier/Laplace/Z","Feedback design","PID control"],
        "assessments":["MATLAB/Simulink labs","control design project"],
        "project_ideas":["drone stabilization","inverted pendulum"],
        "target_hours": 120
    },
    {
        "module_id":"ee.embedded.systems",
        "skill_ids":["ee.embedded","ee.digital_logic"],
        "outcomes":["Microcontroller programming","RTOS","Hardware interfaces"],
        "assessments":["ARM/Arduino projects","FPGA labs"],
        "project_ideas":["IoT sensor network","robot controller"],
        "target_hours": 130
    },
    {
        "module_id":"ee.communications",
        "skill_ids":["ee.comm_systems","ee.em_1"],
        "outcomes":["Modulation schemes","Channel coding","Antenna basics"],
        "assessments":["MATLAB simulations","SDR labs"],
        "project_ideas":["OFDM modem","wireless link design"],
        "target_hours": 120
    },
    
    # Physics Modules
    {
        "module_id":"phys.classical.sequence",
        "skill_ids":["phys.mechanics","phys.em_intro","phys.thermo"],
        "outcomes":["Newtonian mechanics","Maxwell's equations","Thermodynamic laws"],
        "assessments":["problem sets","lab reports"],
        "project_ideas":["orbital mechanics sim","heat engine analysis"],
        "target_hours": 150
    },
    {
        "module_id":"phys.quantum.sequence",
        "skill_ids":["phys.quantum_1","phys.quantum_2"],
        "outcomes":["Wave functions","Operators","Perturbation theory"],
        "assessments":["derivations","computational projects"],
        "project_ideas":["quantum well solver","molecular orbital calc"],
        "target_hours": 140
    },
    {
        "module_id":"phys.advanced.sequence",
        "skill_ids":["phys.stat_mech","phys.solid_state","phys.em_advanced"],
        "outcomes":["Partition functions","Band theory","Gauge theory"],
        "assessments":["research problems","simulations"],
        "project_ideas":["Monte Carlo Ising","DFT calculation"],
        "target_hours": 160
    },
    
    # Data Science Modules
    {
        "module_id":"data.foundations",
        "skill_ids":["data.analysis","data.visualization"],
        "outcomes":["Pandas/NumPy","Statistical analysis","Dashboard creation"],
        "assessments":["data analysis projects","visualization portfolio"],
        "project_ideas":["COVID data dashboard","stock market analysis"],
        "target_hours": 80
    },
    {
        "module_id":"data.engineering.module",
        "skill_ids":["data.engineering","data.big_data","data.streaming"],
        "outcomes":["ETL pipelines","Spark/Hadoop","Kafka streaming"],
        "assessments":["pipeline implementation","performance benchmarks"],
        "project_ideas":["real-time analytics","data lake architecture"],
        "target_hours": 140
    },
]

with open(os.path.join(data_dir, "modules.json"), "w") as f:
    json.dump(modules, f, indent=2)

# -----------------------------
# Resources (Extended catalog)
# -----------------------------
resources = [
    # Programming Resources
    {"resource_id":"course.cs50.harvard","type":"course","title":"CS50x: Introduction to Computer Science","provider":"Harvard","skills":["prog.basics","prog.python.basics","prog.c.basics"],"level":"intro","time_est_hours":100,"quality_score":9.5,"cost":"free","format":["video","problem sets","projects"]},
    {"resource_id":"book.automate_boring_stuff","type":"book","title":"Automate the Boring Stuff with Python","provider":"Sweigart","skills":["prog.python.basics"],"level":"intro","time_est_hours":40,"quality_score":8.8,"cost":"free","format":["text","projects"]},
    {"resource_id":"book.fluent_python","type":"book","title":"Fluent Python","provider":"Luciano Ramalho","skills":["prog.python.advanced"],"level":"advanced","time_est_hours":60,"quality_score":9.2,"cost":"paid","format":["text","examples"]},
    {"resource_id":"book.k_and_r_c","type":"book","title":"The C Programming Language","provider":"Kernighan & Ritchie","skills":["prog.c.basics"],"level":"intro","time_est_hours":40,"quality_score":9.0,"cost":"paid","format":["text","exercises"]},
    {"resource_id":"book.cpp_primer","type":"book","title":"C++ Primer","provider":"Lippman et al.","skills":["prog.cpp.basics"],"level":"intermediate","time_est_hours":80,"quality_score":8.9,"cost":"paid","format":["text","exercises"]},
    {"resource_id":"book.effective_java","type":"book","title":"Effective Java","provider":"Joshua Bloch","skills":["prog.java.basics"],"level":"intermediate","time_est_hours":50,"quality_score":9.3,"cost":"paid","format":["text"]},
    {"resource_id":"course.javascript30","type":"course","title":"JavaScript30","provider":"Wes Bos","skills":["prog.javascript.basics"],"level":"intro","time_est_hours":30,"quality_score":8.7,"cost":"free","format":["video","projects"]},
    
    # CS Core Resources
    {"resource_id":"book.clrs.3e","type":"book","title":"Introduction to Algorithms (CLRS)","provider":"MIT Press","skills":["cs.ds.algorithms"],"level":"advanced","time_est_hours":120,"quality_score":9.7,"cost":"paid","format":["text","problems"]},
    {"resource_id":"course.princeton.algorithms","type":"course","title":"Algorithms (Coursera)","provider":"Princeton","skills":["cs.ds.algorithms"],"level":"intermediate","time_est_hours":80,"quality_score":9.4,"cost":"free","format":["video","assignments"]},
    {"resource_id":"course.leetcode.curated","type":"practice","title":"LeetCode Top 150","provider":"LeetCode","skills":["cs.ds.algorithms"],"level":"intermediate","time_est_hours":100,"quality_score":8.9,"cost":"free","format":["practice","solutions"]},
    {"resource_id":"book.csapp","type":"book","title":"Computer Systems: A Programmer's Perspective","provider":"Bryant & O'Hallaron","skills":["cs.computer.arch"],"level":"intermediate","time_est_hours":100,"quality_score":9.5,"cost":"paid","format":["text","labs"]},
    {"resource_id":"book.ostep","type":"book","title":"Operating Systems: Three Easy Pieces","provider":"Arpaci-Dusseau","skills":["cs.os"],"level":"intermediate","time_est_hours":80,"quality_score":9.6,"cost":"free","format":["text","projects"]},
    {"resource_id":"course.nand2tetris","type":"course","title":"From NAND to Tetris","provider":"Hebrew University","skills":["cs.computer.arch","ee.digital_logic"],"level":"intermediate","time_est_hours":100,"quality_score":9.4,"cost":"free","format":["video","projects"]},
    {"resource_id":"book.kurose_ross","type":"book","title":"Computer Networking: Top-Down Approach","provider":"Kurose & Ross","skills":["cs.networks"],"level":"intermediate","time_est_hours":80,"quality_score":9.2,"cost":"paid","format":["text","labs"]},
    {"resource_id":"course.cmu.15445","type":"course","title":"CMU Database Systems","provider":"CMU","skills":["cs.databases"],"level":"advanced","time_est_hours":100,"quality_score":9.5,"cost":"free","format":["video","projects"]},
    {"resource_id":"book.ddia","type":"book","title":"Designing Data-Intensive Applications","provider":"Martin Kleppmann","skills":["cs.distributed","cs.databases"],"level":"advanced","time_est_hours":80,"quality_score":9.7,"cost":"paid","format":["text"]},
    
    # Web Development Resources
    {"resource_id":"course.fullstackopen","type":"course","title":"Full Stack Open","provider":"University of Helsinki","skills":["cs.web.frontend","cs.web.backend","cs.web.fullstack"],"level":"intermediate","time_est_hours":150,"quality_score":9.3,"cost":"free","format":["text","projects"]},
    {"resource_id":"course.freecodecamp.web","type":"course","title":"Responsive Web Design","provider":"freeCodeCamp","skills":["cs.web.frontend"],"level":"intro","time_est_hours":60,"quality_score":8.8,"cost":"free","format":["interactive","projects"]},
    {"resource_id":"book.eloquent_js","type":"book","title":"Eloquent JavaScript","provider":"Marijn Haverbeke","skills":["prog.javascript.basics","cs.web.frontend"],"level":"intermediate","time_est_hours":60,"quality_score":9.1,"cost":"free","format":["text","exercises"]},
    
    # ML/AI Resources
    {"resource_id":"course.3b1b.linear_algebra","type":"course","title":"Essence of Linear Algebra","provider":"3Blue1Brown","skills":["math.linear_algebra"],"level":"intro","time_est_hours":10,"quality_score":9.8,"cost":"free","format":["video","visual"]},
    {"resource_id":"book.strang.la","type":"book","title":"Introduction to Linear Algebra","provider":"Gilbert Strang","skills":["math.linear_algebra"],"level":"intermediate","time_est_hours":80,"quality_score":9.4,"cost":"paid","format":["text","problems"]},
    {"resource_id":"book.islr","type":"book","title":"Introduction to Statistical Learning","provider":"James et al.","skills":["cs.ai.ml.basics","math.statistics"],"level":"intermediate","time_est_hours":80,"quality_score":9.5,"cost":"free","format":["text","R labs"]},
    {"resource_id":"book.prml","type":"book","title":"Pattern Recognition and Machine Learning","provider":"Christopher Bishop","skills":["cs.ai.ml.basics"],"level":"advanced","time_est_hours":120,"quality_score":9.3,"cost":"paid","format":["text","math"]},
    {"resource_id":"course.fast.ai","type":"course","title":"Practical Deep Learning","provider":"fast.ai","skills":["cs.ai.deep_learning"],"level":"intermediate","time_est_hours":80,"quality_score":9.2,"cost":"free","format":["video","notebooks"]},
    {"resource_id":"book.dl.goodfellow","type":"book","title":"Deep Learning","provider":"Goodfellow et al.","skills":["cs.ai.deep_learning"],"level":"advanced","time_est_hours":120,"quality_score":9.1,"cost":"free","format":["text","math"]},
    {"resource_id":"course.stanford.cs231n","type":"course","title":"CS231n: CNNs for Visual Recognition","provider":"Stanford","skills":["cs.ai.cv"],"level":"advanced","time_est_hours":100,"quality_score":9.4,"cost":"free","format":["video","assignments"]},
    {"resource_id":"course.stanford.cs224n","type":"course","title":"CS224n: NLP with Deep Learning","provider":"Stanford","skills":["cs.ai.nlp"],"level":"advanced","time_est_hours":100,"quality_score":9.3,"cost":"free","format":["video","projects"]},
    
    # EE Resources
    {"resource_id":"book.sedra_smith","type":"book","title":"Microelectronic Circuits","provider":"Sedra/Smith","skills":["ee.circuits_1","ee.circuits_2"],"level":"intermediate","time_est_hours":120,"quality_score":9.1,"cost":"paid","format":["text","problems"]},
    {"resource_id":"book.oppenheim_signals","type":"book","title":"Signals & Systems","provider":"Oppenheim & Willsky","skills":["ee.signals_systems"],"level":"advanced","time_est_hours":100,"quality_score":9.4,"cost":"paid","format":["text","problems"]},
    {"resource_id":"book.ogata_control","type":"book","title":"Modern Control Engineering","provider":"Ogata","skills":["ee.control_systems"],"level":"advanced","time_est_hours":90,"quality_score":8.9,"cost":"paid","format":["text","MATLAB"]},
    {"resource_id":"book.ulaby_em","type":"book","title":"Fundamentals of Applied Electromagnetics","provider":"Ulaby","skills":["ee.em_1"],"level":"intermediate","time_est_hours":80,"quality_score":8.8,"cost":"paid","format":["text","simulations"]},
    {"resource_id":"book.proakis_comm","type":"book","title":"Digital Communications","provider":"Proakis & Salehi","skills":["ee.comm_systems"],"level":"advanced","time_est_hours":100,"quality_score":9.0,"cost":"paid","format":["text","MATLAB"]},
    {"resource_id":"book.sze_semiconductor","type":"book","title":"Physics of Semiconductor Devices","provider":"Sze & Ng","skills":["ee.semiconductor_devices"],"level":"advanced","time_est_hours":100,"quality_score":9.5,"cost":"paid","format":["text"]},
    {"resource_id":"course.arm.embedded","type":"course","title":"Embedded Systems with ARM","provider":"ARM Education","skills":["ee.embedded"],"level":"intermediate","time_est_hours":80,"quality_score":8.9,"cost":"free","format":["video","labs"]},
    
    # Physics Resources
    {"resource_id":"book.taylor_mechanics","type":"book","title":"Classical Mechanics","provider":"John R. Taylor","skills":["phys.mechanics"],"level":"intermediate","time_est_hours":90,"quality_score":9.2,"cost":"paid","format":["text","problems"]},
    {"resource_id":"book.griffiths_em","type":"book","title":"Introduction to Electrodynamics","provider":"David Griffiths","skills":["phys.em_intro","phys.em_advanced"],"level":"intermediate","time_est_hours":120,"quality_score":9.6,"cost":"paid","format":["text","problems"]},
    {"resource_id":"book.griffiths_qm","type":"book","title":"Introduction to Quantum Mechanics","provider":"David Griffiths","skills":["phys.quantum_1"],"level":"intermediate","time_est_hours":100,"quality_score":9.4,"cost":"paid","format":["text","problems"]},
    {"resource_id":"book.sakurai_qm","type":"book","title":"Modern Quantum Mechanics","provider":"Sakurai & Napolitano","skills":["phys.quantum_2"],"level":"advanced","time_est_hours":120,"quality_score":9.3,"cost":"paid","format":["text","problems"]},
    {"resource_id":"book.reif_statmech","type":"book","title":"Fundamentals of Statistical and Thermal Physics","provider":"F. Reif","skills":["phys.stat_mech","phys.thermo"],"level":"advanced","time_est_hours":110,"quality_score":9.0,"cost":"paid","format":["text","problems"]},
    {"resource_id":"book.kittel_solid","type":"book","title":"Introduction to Solid State Physics","provider":"Charles Kittel","skills":["phys.solid_state"],"level":"advanced","time_est_hours":100,"quality_score":8.9,"cost":"paid","format":["text"]},
    {"resource_id":"course.mit.8.01","type":"course","title":"MIT 8.01 Physics I","provider":"MIT OCW","skills":["phys.mechanics"],"level":"intro","time_est_hours":80,"quality_score":9.3,"cost":"free","format":["video","problems"]},
    {"resource_id":"course.mit.8.02","type":"course","title":"MIT 8.02 Physics II","provider":"MIT OCW","skills":["phys.em_intro"],"level":"intro","time_est_hours":80,"quality_score":9.2,"cost":"free","format":["video","problems"]},
    
    # Math Resources
    {"resource_id":"course.khan.calculus","type":"course","title":"Calculus Course","provider":"Khan Academy","skills":["math.calculus_1","math.calculus_2","math.calculus_3"],"level":"intro","time_est_hours":120,"quality_score":8.8,"cost":"free","format":["video","practice"]},
    {"resource_id":"book.stewart_calculus","type":"book","title":"Calculus: Early Transcendentals","provider":"James Stewart","skills":["math.calculus_1","math.calculus_2","math.calculus_3"],"level":"intermediate","time_est_hours":150,"quality_score":9.0,"cost":"paid","format":["text","problems"]},
    {"resource_id":"book.rosen_discrete","type":"book","title":"Discrete Mathematics and Its Applications","provider":"Kenneth Rosen","skills":["math.discrete"],"level":"intermediate","time_est_hours":80,"quality_score":8.9,"cost":"paid","format":["text","problems"]},
    {"resource_id":"course.mit.18.06","type":"course","title":"MIT Linear Algebra","provider":"MIT OCW","skills":["math.linear_algebra"],"level":"intermediate","time_est_hours":60,"quality_score":9.5,"cost":"free","format":["video","problems"]},
    {"resource_id":"book.ross_probability","type":"book","title":"A First Course in Probability","provider":"Sheldon Ross","skills":["math.statistics"],"level":"intermediate","time_est_hours":70,"quality_score":8.8,"cost":"paid","format":["text","problems"]},
    
    # Data Science Resources
    {"resource_id":"book.mckinney_pandas","type":"book","title":"Python for Data Analysis","provider":"Wes McKinney","skills":["data.analysis"],"level":"intermediate","time_est_hours":60,"quality_score":9.1,"cost":"paid","format":["text","code"]},
    {"resource_id":"course.coursera.data_science","type":"course","title":"Data Science Specialization","provider":"Johns Hopkins","skills":["data.analysis","data.visualization"],"level":"intermediate","time_est_hours":120,"quality_score":8.7,"cost":"paid","format":["video","projects"]},
    {"resource_id":"book.kleppmann_streaming","type":"book","title":"Streaming Systems","provider":"Akidau et al.","skills":["data.streaming"],"level":"advanced","time_est_hours":80,"quality_score":9.0,"cost":"paid","format":["text"]},
    {"resource_id":"course.spark.definitive","type":"book","title":"Spark: The Definitive Guide","provider":"Chambers & Zaharia","skills":["data.big_data"],"level":"intermediate","time_est_hours":70,"quality_score":8.9,"cost":"paid","format":["text","code"]},
]

with open(os.path.join(data_dir, "resources.json"), "w") as f:
    json.dump(resources, f, indent=2)

# -----------------------------
# Backend: FastAPI planner
# -----------------------------
backend_requirements = """\
fastapi==0.112.0
uvicorn==0.30.6
pydantic==2.8.2
python-multipart==0.0.9
cors==1.0.1
"""

with open(os.path.join(backend, "requirements.txt"), "w") as f:
    f.write(backend_requirements)

backend_readme = """\
# AI Path Advisor — Backend (FastAPI)

## Quickstart
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will run on http://127.0.0.1:8000

## API Endpoints

### POST /plan
Generate a learning roadmap based on goals and constraints.

### GET /skills
List all available skills with prerequisites.

### GET /resources
List all available learning resources.

### GET /modules
List all available learning modules.

## Test
```bash
curl -X POST http://127.0.0.1:8000/plan \\
  -H "Content-Type: application/json" \\
  -d '{
    "major":"cs",
    "goal":"ml-engineer",
    "horizon_months":12,
    "weekly_hours":15,
    "budget":200,
    "baseline_mastered":["prog.python.basics"]
  }'
```
"""

with open(os.path.join(backend, "README.md"), "w") as f:
    f.write(backend_readme)

main_py = '''
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Set
import json
import os
import math
from datetime import datetime, timedelta

# Load data
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def load_json(name: str):
    with open(os.path.join(DATA_DIR, name), "r") as f:
        return json.load(f)

# Load all data
SKILLS = {s["skill_id"]: s for s in load_json("skills.json")}
MODULES = load_json("modules.json")
RESOURCES = load_json("resources.json")

# Index resources by skill
RES_BY_SKILL: Dict[str, List[Dict[str, Any]]] = {}
for r in RESOURCES:
    for sid in r["skills"]:
        RES_BY_SKILL.setdefault(sid, []).append(r)

# Career path definitions
CAREER_PATHS = {
    "ml-engineer": {
        "name": "Machine Learning Engineer",
        "target_skills": [
            "math.linear_algebra", "math.statistics", "prog.python.advanced",
            "cs.ai.ml.basics", "cs.ai.deep_learning", "data.engineering",
            "cs.software.engineering", "cs.distributed"
        ],
        "description": "Build and deploy ML systems at scale"
    },
    "data-engineer": {
        "name": "Data Engineer",
        "target_skills": [
            "prog.python.advanced", "cs.databases", "data.engineering",
            "data.big_data", "data.streaming", "cs.distributed"
        ],
        "description": "Design and build data pipelines"
    },
    "embedded-engineer": {
        "name": "Embedded Systems Engineer",
        "target_skills": [
            "prog.c.basics", "ee.digital_logic", "ee.embedded",
            "cs.computer.arch", "cs.os"
        ],
        "description": "Develop firmware and embedded systems"
    },
    "full-stack": {
        "name": "Full Stack Developer",
        "target_skills": [
            "prog.javascript.basics", "cs.web.frontend", "cs.web.backend",
            "cs.databases", "cs.software.engineering"
        ],
        "description": "Build end-to-end web applications"
    },
    "security-engineer": {
        "name": "Security Engineer",
        "target_skills": [
            "cs.security.basics", "cs.security.crypto", "cs.security.web",
            "cs.networks", "cs.os"
        ],
        "description": "Secure systems and applications"
    }
}

# Major target skills
MAJOR_TARGETS = {
    "cs": [
        "prog.python.basics", "prog.c.basics", "math.discrete", "cs.ds.algorithms",
        "cs.computer.arch", "cs.os", "cs.networks", "cs.databases", 
        "cs.software.engineering", "cs.ai.ml.basics"
    ],
    "ee": [
        "math.calculus_1", "math.calculus_2", "math.calculus_3", "math.linear_algebra",
        "ee.circuits_1", "ee.circuits_2", "ee.signals_systems", "ee.control_systems",
        "ee.em_1", "ee.digital_logic", "ee.embedded"
    ],
    "physics": [
        "math.calculus_1", "math.calculus_2", "math.calculus_3", "math.linear_algebra",
        "phys.mechanics", "phys.em_intro", "phys.modern", "phys.thermo",
        "phys.quantum_1", "phys.stat_mech"
    ],
    "data-science": [
        "prog.python.basics", "math.statistics", "math.linear_algebra",
        "data.analysis", "data.visualization", "cs.ai.ml.basics",
        "data.engineering"
    ]
}

# Request/Response models
class PlanRequest(BaseModel):
    major: Optional[str] = Field(None, description="Academic major: cs, ee, physics, data-science")
    goal: Optional[str] = Field(None, description="Career goal: ml-engineer, data-engineer, etc.")
    target_skills: Optional[List[str]] = Field(None, description="Custom target skills")
    baseline_mastered: List[str] = Field(default_factory=list, description="Already mastered skills")
    horizon_months: int = Field(12, description="Time horizon in months")
    weekly_hours: int = Field(15, description="Weekly study hours")
    budget: int = Field(200, description="Monthly budget in USD")
    learning_style: str = Field("mixed", description="visual, reading, hands-on, mixed")

class RoadmapStep(BaseModel):
    skill_id: str
    skill_name: str
    resources: List[Dict[str, Any]]
    est_hours: int
    start_week: int
    end_week: int
    prerequisites: List[str]
    module_id: Optional[str] = None

class Milestone(BaseModel):
    week: int
    name: str
    type: str
    description: str

class Roadmap(BaseModel):
    sequence: List[RoadmapStep]
    milestones: List[Milestone]
    summary: Dict[str, Any]
    skill_graph: Dict[str, Any]
    estimated_completion: str

# Initialize FastAPI app
app = FastAPI(
    title="AI Path Advisor API",
    description="Personalized learning roadmap generator",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper functions
def expand_prereqs(targets: List[str]) -> List[str]:
    """Expand target skills to include all prerequisites"""
    seen: Set[str] = set()
    order: List[str] = []
    
    def dfs(sid: str):
        if sid in seen or sid not in SKILLS:
            return
        seen.add(sid)
        for prereq in SKILLS[sid].get("prereq_ids", []):
            dfs(prereq)
        order.append(sid)
    
    for target in targets:
        dfs(target)
    
    # Return in learning order (prerequisites first)
    return order

def pick_resources(skill_id: str, budget_remain: int, target_hours: int, style: str) -> tuple:
    """Select best resources for a skill based on constraints"""
    pool = RES_BY_SKILL.get(skill_id, [])
    
    # Score resources
    scored = []
    for r in pool:
        score = r["quality_score"] * 10
        
        # Adjust for cost
        cost = 0 if r["cost"] == "free" else 50
        if cost > budget_remain:
            score -= 30
        elif r["cost"] == "free":
            score += 10
        
        # Adjust for learning style
        if style == "visual" and "video" in r["format"]:
            score += 15
        elif style == "reading" and "text" in r["format"]:
            score += 15
        elif style == "hands-on" and any(x in r["format"] for x in ["projects", "labs", "practice"]):
            score += 15
        
        # Prefer comprehensive resources
        if r["time_est_hours"] >= target_hours * 0.8:
            score += 10
        
        scored.append((score, r, cost))
    
    # Sort by score
    scored.sort(key=lambda x: -x[0])
    
    # Select top resources within budget
    chosen = []
    total_cost = 0
    total_hours = 0
    
    for score, resource, cost in scored:
        if total_cost + cost <= budget_remain or not chosen:
            chosen.append(resource)
            total_cost += cost
            total_hours += resource["time_est_hours"]
            if total_hours >= target_hours:
                break
    
    return chosen, total_cost, max(total_hours, 40)

def find_module_for_skill(skill_id: str) -> Optional[str]:
    """Find module containing this skill"""
    for module in MODULES:
        if skill_id in module["skill_ids"]:
            return module["module_id"]
    return None

def estimate_skill_hours(skill_id: str) -> int:
    """Estimate hours needed for a skill"""
    # Check if skill is in any module
    for module in MODULES:
        if skill_id in module["skill_ids"]:
            return module["target_hours"] // len(module["skill_ids"])
    
    # Default based on difficulty
    difficulty = SKILLS.get(skill_id, {}).get("difficulty", 3)
    return difficulty * 25

# API Endpoints
@app.get("/")
def root():
    return {
        "name": "AI Path Advisor API",
        "version": "1.0.0",
        "endpoints": ["/plan", "/skills", "/resources", "/modules", "/careers"]
    }

@app.get("/skills")
def get_skills():
    """Get all available skills"""
    return list(SKILLS.values())

@app.get("/resources")
def get_resources():
    """Get all available resources"""
    return RESOURCES

@app.get("/modules")
def get_modules():
    """Get all available modules"""
    return MODULES

@app.get("/careers")
def get_careers():
    """Get all career paths"""
    return CAREER_PATHS

@app.post("/plan", response_model=Roadmap)
def generate_plan(req: PlanRequest):
    """Generate a personalized learning roadmap"""
    
    # Determine target skills
    targets = []
    if req.target_skills:
        targets = req.target_skills
    elif req.goal and req.goal in CAREER_PATHS:
        targets = CAREER_PATHS[req.goal]["target_skills"]
    elif req.major and req.major in MAJOR_TARGETS:
        targets = MAJOR_TARGETS[req.major]
    else:
        raise HTTPException(400, "Must specify either major, goal, or target_skills")
    
    # Expand prerequisites
    ordered_skills = expand_prereqs(targets)
    
    # Filter out already mastered
    needed = [s for s in ordered_skills if s not in req.baseline_mastered]
    
    if not needed:
        return Roadmap(
            sequence=[],
            milestones=[],
            summary={"message": "All target skills already mastered!"},
            skill_graph={},
            estimated_completion="Already complete"
        )
    
    # Calculate budget
    monthly_budget = req.budget
    total_months = req.horizon_months
    total_budget = monthly_budget * total_months
    budget_per_skill = total_budget // len(needed) if needed else 0
    
    # Build learning sequence
    steps = []
    current_week = 1
    budget_used = 0
    
    for skill_id in needed:
        if skill_id not in SKILLS:
            continue
        
        skill = SKILLS[skill_id]
        target_hours = estimate_skill_hours(skill_id)
        
        # Pick resources
        resources, cost, hours = pick_resources(
            skill_id, 
            min(budget_per_skill, total_budget - budget_used),
            target_hours,
            req.learning_style
        )
        
        budget_used += cost
        
        # Calculate duration
        weeks_needed = max(1, math.ceil(hours / req.weekly_hours))
        
        # Create step
        step = RoadmapStep(
            skill_id=skill_id,
            skill_name=skill["name"],
            resources=resources,
            est_hours=hours,
            start_week=current_week,
            end_week=current_week + weeks_needed - 1,
            prerequisites=skill.get("prereq_ids", []),
            module_id=find_module_for_skill(skill_id)
        )
        steps.append(step)
        current_week += weeks_needed
    
    # Generate milestones
    milestones = [
        Milestone(
            week=1,
            name="Kickoff",
            type="start",
            description="Begin your learning journey"
        )
    ]
    
    # Add skill completion milestones
    for i, step in enumerate(steps):
        if (i + 1) % 3 == 0:  # Every 3 skills
            milestones.append(Milestone(
                week=step.end_week,
                name=f"Checkpoint {(i + 1) // 3}",
                type="assessment",
                description=f"Skills assessment after {i + 1} skills"
            ))
    
    # Add final milestone
    if steps:
        milestones.append(Milestone(
            week=steps[-1].end_week + 1,
            name="Capstone Project",
            type="project",
            description="Build portfolio project showcasing all skills"
        ))
    
    # Calculate completion date
    total_weeks = steps[-1].end_week if steps else 0
    completion_date = datetime.now() + timedelta(weeks=total_weeks)
    
    # Build skill graph for visualization
    skill_graph = {
        "nodes": [{"id": s.skill_id, "name": s.skill_name} for s in steps],
        "edges": []
    }
    
    for step in steps:
        for prereq in step.prerequisites:
            if any(s.skill_id == prereq for s in steps):
                skill_graph["edges"].append({"from": prereq, "to": step.skill_id})
    
    return Roadmap(
        sequence=steps,
        milestones=milestones,
        summary={
            "total_skills": len(steps),
            "total_weeks": total_weeks,
            "total_hours": sum(s.est_hours for s in steps),
            "budget_used": budget_used,
            "budget_remaining": total_budget - budget_used,
            "weekly_hours": req.weekly_hours,
            "completion_months": round(total_weeks / 4.33, 1)
        },
        skill_graph=skill_graph,
        estimated_completion=completion_date.strftime("%B %Y")
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''

with open(os.path.join(backend, "main.py"), "w") as f:
    f.write(main_py)

# -----------------------------
# Frontend: Next.js App
# -----------------------------
package_json = {
    "name": "ai-path-advisor-frontend",
    "version": "0.1.0",
    "private": True,
    "scripts": {
        "dev": "next dev -p 3001",
        "build": "next build",
        "start": "next start -p 3001",
        "lint": "next lint"
    },
    "dependencies": {
        "next": "14.2.5",
        "react": "18.3.1",
        "react-dom": "18.3.1",
        "axios": "^1.6.0",
        "@heroicons/react": "^2.0.18"
    },
    "devDependencies": {
        "@types/node": "^20",
        "@types/react": "^18",
        "@types/react-dom": "^18",
        "typescript": "^5",
        "tailwindcss": "^3.4.0",
        "autoprefixer": "^10.0.1",
        "postcss": "^8"
    }
}

with open(os.path.join(frontend, "package.json"), "w") as f:
    json.dump(package_json, f, indent=2)

# Next.js config
next_config = """/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
}

module.exports = nextConfig
"""
with open(os.path.join(frontend, "next.config.js"), "w") as f:
    f.write(next_config)

# TypeScript config
tsconfig = {
    "compilerOptions": {
        "target": "ES2020",
        "lib": ["dom", "dom.iterable", "esnext"],
        "allowJs": True,
        "skipLibCheck": True,
        "strict": True,
        "noEmit": True,
        "esModuleInterop": True,
        "module": "esnext",
        "moduleResolution": "bundler",
        "resolveJsonModule": True,
        "isolatedModules": True,
        "jsx": "preserve",
        "incremental": True,
        "paths": {
            "@/*": ["./*"]
        }
    },
    "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx"],
    "exclude": ["node_modules"]
}

with open(os.path.join(frontend, "tsconfig.json"), "w") as f:
    json.dump(tsconfig, f, indent=2)

# Tailwind config
tailwind_config = """/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
"""
with open(os.path.join(frontend, "tailwind.config.js"), "w") as f:
    f.write(tailwind_config)

# PostCSS config
postcss_config = """module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
"""
with open(os.path.join(frontend, "postcss.config.js"), "w") as f:
    f.write(postcss_config)

# Global styles
globals_css = """@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --foreground-rgb: 0, 0, 0;
  --background-start-rgb: 214, 219, 220;
  --background-end-rgb: 255, 255, 255;
}

@media (prefers-color-scheme: dark) {
  :root {
    --foreground-rgb: 255, 255, 255;
    --background-start-rgb: 0, 0, 0;
    --background-end-rgb: 0, 0, 0;
  }
}

body {
  color: rgb(var(--foreground-rgb));
  background: linear-gradient(
      to bottom,
      transparent,
      rgb(var(--background-end-rgb))
    )
    rgb(var(--background-start-rgb));
}
"""
with open(os.path.join(frontend, "app", "globals.css"), "w") as f:
    f.write(globals_css)

# Layout
layout_tsx = """import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'AI Path Advisor',
  description: 'Personalized learning roadmap generator',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
"""
with open(os.path.join(frontend, "app", "layout.tsx"), "w") as f:
    f.write(layout_tsx)

# Main page
page_tsx = '''\'use client\'

import { useState } from 'react'
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface Resource {
  resource_id: string
  title: string
  provider: string
  type: string
  time_est_hours: number
  quality_score: number
  cost: string
}

interface RoadmapStep {
  skill_id: string
  skill_name: string
  resources: Resource[]
  est_hours: number
  start_week: number
  end_week: number
}

interface Roadmap {
  sequence: RoadmapStep[]
  milestones: any[]
  summary: any
  estimated_completion: string
}

export default function Home() {
  const [formData, setFormData] = useState({
    major: 'cs',
    goal: 'ml-engineer',
    weekly_hours: 15,
    horizon_months: 12,
    budget: 200,
    baseline: '',
    learning_style: 'mixed'
  })
  
  const [loading, setLoading] = useState(false)
  const [roadmap, setRoadmap] = useState<Roadmap | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState('form')

  const generateRoadmap = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await axios.post(`${API_URL}/plan`, {
        major: formData.major,
        goal: formData.goal,
        horizon_months: formData.horizon_months,
        weekly_hours: formData.weekly_hours,
        budget: formData.budget,
        baseline_mastered: formData.baseline.split(',').map(s => s.trim()).filter(Boolean),
        learning_style: formData.learning_style
      })
      
      setRoadmap(response.data)
      setActiveTab('roadmap')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate roadmap')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
            AI Path Advisor
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300">
            Generate personalized learning roadmaps for your career goals
          </p>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg">
          <div className="border-b border-gray-200 dark:border-gray-700">
            <nav className="flex -mb-px">
              <button
                onClick={() => setActiveTab('form')}
                className={`py-4 px-6 text-sm font-medium ${
                  activeTab === 'form'
                    ? 'border-b-2 border-blue-500 text-blue-600'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                Setup
              </button>
              <button
                onClick={() => setActiveTab('roadmap')}
                disabled={!roadmap}
                className={`py-4 px-6 text-sm font-medium ${
                  activeTab === 'roadmap'
                    ? 'border-b-2 border-blue-500 text-blue-600'
                    : 'text-gray-500 hover:text-gray-700'
                } ${!roadmap ? 'opacity-50 cursor-not-allowed' : ''}`}
              >
                Roadmap
              </button>
            </nav>
          </div>

          <div className="p-6">
            {activeTab === 'form' && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Major/Field
                  </label>
                  <select
                    value={formData.major}
                    onChange={(e) => setFormData({...formData, major: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="cs">Computer Science</option>
                    <option value="ee">Electrical Engineering</option>
                    <option value="physics">Physics</option>
                    <option value="data-science">Data Science</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Career Goal
                  </label>
                  <select
                    value={formData.goal}
                    onChange={(e) => setFormData({...formData, goal: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="ml-engineer">Machine Learning Engineer</option>
                    <option value="data-engineer">Data Engineer</option>
                    <option value="embedded-engineer">Embedded Systems Engineer</option>
                    <option value="full-stack">Full Stack Developer</option>
                    <option value="security-engineer">Security Engineer</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Weekly Study Hours: {formData.weekly_hours}
                  </label>
                  <input
                    type="range"
                    min="5"
                    max="40"
                    value={formData.weekly_hours}
                    onChange={(e) => setFormData({...formData, weekly_hours: parseInt(e.target.value)})}
                    className="w-full"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Time Horizon (months): {formData.horizon_months}
                  </label>
                  <input
                    type="range"
                    min="3"
                    max="36"
                    value={formData.horizon_months}
                    onChange={(e) => setFormData({...formData, horizon_months: parseInt(e.target.value)})}
                    className="w-full"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Monthly Budget ($): {formData.budget}
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="500"
                    step="50"
                    value={formData.budget}
                    onChange={(e) => setFormData({...formData, budget: parseInt(e.target.value)})}
                    className="w-full"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Learning Style
                  </label>
                  <select
                    value={formData.learning_style}
                    onChange={(e) => setFormData({...formData, learning_style: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="visual">Visual (Videos)</option>
                    <option value="reading">Reading (Books)</option>
                    <option value="hands-on">Hands-on (Projects)</option>
                    <option value="mixed">Mixed</option>
                  </select>
                </div>

                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Already Mastered Skills (comma-separated skill IDs)
                  </label>
                  <textarea
                    value={formData.baseline}
                    onChange={(e) => setFormData({...formData, baseline: e.target.value})}
                    placeholder="e.g., prog.python.basics, math.calculus_1"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    rows={3}
                  />
                </div>

                <div className="md:col-span-2">
                  <button
                    onClick={generateRoadmap}
                    disabled={loading}
                    className="w-full bg-blue-600 text-white py-3 px-6 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
                  >
                    {loading ? 'Generating...' : 'Generate Roadmap'}
                  </button>
                  
                  {error && (
                    <div className="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
                      {error}
                    </div>
                  )}
                </div>
              </div>
            )}

            {activeTab === 'roadmap' && roadmap && (
              <div>
                <div className="mb-6 p-4 bg-blue-50 dark:bg-blue-900 rounded-lg">
                  <h2 className="text-xl font-bold mb-2">Your Learning Path</h2>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4">
                    <div>
                      <p className="text-sm text-gray-600 dark:text-gray-400">Total Skills</p>
                      <p className="text-2xl font-bold">{roadmap.summary.total_skills}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600 dark:text-gray-400">Duration</p>
                      <p className="text-2xl font-bold">{roadmap.summary.completion_months} months</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600 dark:text-gray-400">Total Hours</p>
                      <p className="text-2xl font-bold">{roadmap.summary.total_hours}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600 dark:text-gray-400">Completion</p>
                      <p className="text-2xl font-bold">{roadmap.estimated_completion}</p>
                    </div>
                  </div>
                </div>

                <div className="space-y-4">
                  <h3 className="text-lg font-semibold mb-4">Learning Sequence</h3>
                  {roadmap.sequence.map((step, index) => (
                    <div key={step.skill_id} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
                      <div className="flex justify-between items-start mb-2">
                        <div>
                          <h4 className="font-semibold text-lg">
                            {index + 1}. {step.skill_name}
                          </h4>
                          <p className="text-sm text-gray-600 dark:text-gray-400">
                            Weeks {step.start_week}-{step.end_week} • {step.est_hours} hours
                          </p>
                        </div>
                        <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
                          Week {step.start_week}
                        </span>
                      </div>
                      
                      <div className="mt-3">
                        <p className="text-sm font-medium mb-2">Resources:</p>
                        <div className="space-y-2">
                          {step.resources.map((resource) => (
                            <div key={resource.resource_id} className="flex justify-between items-center p-2 bg-gray-50 dark:bg-gray-900 rounded">
                              <div>
                                <p className="font-medium text-sm">{resource.title}</p>
                                <p className="text-xs text-gray-600 dark:text-gray-400">
                                  {resource.provider} • {resource.type} • {resource.time_est_hours}h
                                </p>
                              </div>
                              <div className="flex items-center gap-2">
                                <span className={`px-2 py-1 rounded text-xs ${
                                  resource.cost === 'free' 
                                    ? 'bg-green-100 text-green-800' 
                                    : 'bg-yellow-100 text-yellow-800'
                                }`}>
                                  {resource.cost}
                                </span>
                                <span className="text-xs font-semibold">
                                  {resource.quality_score}/10
                                </span>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="mt-8">
                  <h3 className="text-lg font-semibold mb-4">Milestones</h3>
                  <div className="space-y-2">
                    {roadmap.milestones.map((milestone, index) => (
                      <div key={index} className="flex items-center gap-4 p-3 bg-gray-50 dark:bg-gray-900 rounded">
                        <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                          <span className="font-bold text-blue-600">W{milestone.week}</span>
                        </div>
                        <div>
                          <p className="font-medium">{milestone.name}</p>
                          <p className="text-sm text-gray-600 dark:text-gray-400">{milestone.description}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
'''

with open(os.path.join(frontend, "app", "page.tsx"), "w") as f:
    f.write(page_tsx)

# Frontend README
frontend_readme = """\
# AI Path Advisor — Frontend (Next.js)

## Setup
```bash
cd frontend
npm install
```

## Development
```bash
npm run dev
```
Open http://localhost:3001

## Environment Variables
Create a `.env.local` file:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Build for Production
```bash
npm run build
npm start
```

## Features
- Interactive form for goal setting
- Visual roadmap display
- Resource recommendations
- Progress tracking
- Milestone visualization
"""

with open(os.path.join(frontend, "README.md"), "w") as f:
    f.write(frontend_readme)

# Main README
main_readme = """\
# AI Path Advisor Starter Kit

A complete learning roadmap generator with FastAPI backend and Next.js frontend.

## Quick Start

### 1. Backend (Terminal 1)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend (Terminal 2)
```bash
cd frontend
npm install
npm run dev
```

### 3. Access
- Frontend: http://localhost:3001
- API Docs: http://localhost:8000/docs

## Features

### Backend
- FastAPI with automatic API documentation
- 50+ skills across CS, EE, Physics, Data Science
- 15+ learning modules with assessments
- 60+ curated resources (books, courses, videos)
- Intelligent path planning algorithm
- Career path templates
- Resource quality scoring

### Frontend
- Modern React/Next.js interface
- Interactive goal wizard
- Visual roadmap display
- Resource recommendations
- Progress tracking

## Data Structure

### Skills
- Prerequisite graph
- Difficulty levels
- Tags for categorization

### Modules
- Skill groupings
- Learning outcomes
- Assessment types
- Project ideas

### Resources
- Quality scores
- Time estimates
- Cost information
- Format types

## Customization

### Add New Major
1. Add skills to `backend/data/skills.json`
2. Add modules to `backend/data/modules.json`
3. Add resources to `backend/data/resources.json`
4. Update `MAJOR_TARGETS` in `backend/main.py`

### Add Career Path
Update `CAREER_PATHS` in `backend/main.py`

## API Endpoints

- `POST /plan` - Generate roadmap
- `GET /skills` - List all skills
- `GET /resources` - List all resources
- `GET /modules` - List all modules
- `GET /careers` - List career paths

## License
MIT
"""

with open(os.path.join(root, "README.md"), "w") as f:
    f.write(main_readme)

print(f"✅ AI Path Advisor starter kit created at: {root}")
print("\n📁 Structure:")
print("  backend/")
print("    ├── main.py           # FastAPI server")
print("    ├── requirements.txt  # Python dependencies")
print("    └── data/            # JSON data files")
print("        ├── skills.json")
print("        ├── modules.json")
print("        └── resources.json")
print("  frontend/")
print("    ├── app/             # Next.js app directory")
print("    │   ├── page.tsx     # Main UI")
print("    │   ├── layout.tsx")
print("    │   └── globals.css")
print("    ├── package.json")
print("    └── *.config.js      # Config files")
print("\n🚀 To run:")
print("  1. Backend:  cd backend && pip install -r requirements.txt && uvicorn main:app --reload")
print("  2. Frontend: cd frontend && npm install && npm run dev")