import streamlit as st
import random
import time

# --- Page Configuration ---
st.set_page_config(page_title="PulseGuard AI - Ward Dashboard", layout="wide")

# --- 1. Generate 1000 Patient Records ---
if "patient_registry" not in st.session_state:
    current_random_state = random.getstate()
    random.seed(42)  # Lock seed for consistent multi-tab generation
    
    first_names = ["Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Ayaan", "Krishna", "Ishaan", "Shaurya", "Atharv", "Dhruv", "Kabir", "Rudra", "Diya", "Saanvi", "Ananya", "Aadhya", "Pari", "Anika", "Navya", "Angel", "Myra", "Sara", "Ira", "Riya", "Aarohi", "Anvi", "Prisha"]
    last_names = ["Sharma", "Verma", "Patel", "Reddy", "Rao", "Nair", "Iyer", "Kulkarni", "Deshmukh", "Mehta", "Gupta", "Singh", "Kumar", "Chopra", "Bose", "Chatterjee", "Banerjee", "Pillai", "Menon", "Joshi", "Bhat", "Hegde", "Shetty", "Gowda", "Naidu", "Chowdhury", "Das", "Dutta", "Mukherjee", "Sen", "Malhotra", "Kapoor", "Khanna", "Saxena"]
    blood_groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    allergies_list = ["None Known (NKDA)", "Penicillin", "Sulfa Drugs", "Aspirin / NSAIDs", "Latex", "Peanuts", "Dust Mites", "Ciprofloxacin"]
    histories_list = ["No Major Medical History", "Type 2 Diabetes Mellitus", "Essential Hypertension", "Coronary Artery Disease (Post-Stent)", "Asthma (Moderate Persistent)", "Chronic Kidney Disease Stage 2", "Hypothyroidism", "Previous Stroke (2022)"]
    medications_list = ["None", "Metformin 500mg BD", "Amlodipine 5mg OD", "Atorvastatin 20mg HS", "Telmisartan 40mg OD", "Salbutamol Inhaler PRN", "Levothyroxine 50mcg OD", "Ecosprin 75mg OD"]
    
    registry = []
    patient_count = 0
    
    for first in first_names:
        for last in last_names:
            if patient_count >= 1000:
                break
            
            profile_chance = random.random()
            if profile_chance < 0.85:
                profile = "Stable"
            elif profile_chance < 0.90:
                profile = "Hypoxia Risk"
            elif profile_chance < 0.95:
                profile = "Hypertension Risk"
            else:
                profile = "Volatile"
                
            mobile_prefix = random.choice(["98", "97", "99", "88", "70", "91", "63"])
            mobile_suffix = str(random.randint(10000000, 99999999))
            phone_number = f"+91 {mobile_prefix}{mobile_suffix[:3]} {mobile_suffix[3:]}"
            email_addr = f"{first.lower()}.{last.lower()}{random.randint(10, 99)}@gmail.com"
            
            registry.append({
                "id": f"PG-{1001 + patient_count}",
                "name": f"{first} {last}",
                "age": random.randint(19, 88),
                "gender": random.choice(["Male", "Female"]),
                "blood_group": random.choice(blood_groups),
                "condition": profile,
                "allergies": random.choice(allergies_list),
                "history": random.choice(histories_list),
                "medications": random.choice(medications_list),
                "contact": phone_number,
                "email": email_addr,
                "emergency_contact": f"+91 {random.choice(['98', '99', '88'])}{random.randint(1000000, 9999999)}"
            })
            patient_count += 1
            
        if patient_count >= 1000:
            break
            
    st.session_state.patient_registry = registry
    random.setstate(current_random_state)

# --- 2. Triage Logic Engine ---
def calculate_severity(spo2, heart_rate, bp_sys, bp_dia):
    if spo2 < 90:
        spo2_data = ("#dc3545", "CRITICAL")
    elif 90 <= spo2 <= 94:
        spo2_data = ("#ffc107", "WARNING")
    else:
        spo2_data = ("#28a745", "NORMAL")

    if heart_rate < 50 or heart_rate >= 120:
        hr_data = ("#dc3545", "CRITICAL")
    elif (50 <= heart_rate <= 59) or (101 <= heart_rate <= 119):
        hr_data = ("#ffc107", "WARNING")
    else:
        hr_data = ("#28a745", "NORMAL")

    if bp_sys >= 180 or bp_dia >= 110:
        bp_data = ("#dc3545", "CRITICAL")
    elif (120 <= bp_sys <= 179) or (80 <= bp_dia <= 109):
        bp_data = ("#ffc107", "WARNING")
    else:
        bp_data = ("#28a745", "NORMAL")

    return spo2_data, hr_data, bp_data

# --- 3. Simulated Telemetry Engine ---
def generate_patient_vitals(profile):
    if profile == "Stable":
        return {"spo2": random.randint(96, 100), "hr": random.randint(60, 85), "bp_sys": random.randint(110, 118), "bp_dia": random.randint(70, 78)}
    elif profile == "Hypoxia Risk":
        return {"spo2": random.randint(85, 93), "hr": random.randint(95, 115), "bp_sys": random.randint(120, 135), "bp_dia": random.randint(80, 90)}
