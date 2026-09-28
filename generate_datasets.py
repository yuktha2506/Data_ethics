import random
import numpy as np
import pandas as pd
from datetime import date, timedelta

random.seed(42)
np.random.seed(42)

FIRST_NAMES = ["Aarav","Vivaan","Aditya","Ishaan","Arjun","Reyansh","Kabir","Vihaan",
    "Ananya","Diya","Saanvi","Myra","Aadhya","Kiara","Anika","Riya",
    "Meera","Rohan","Kavya","Naveen","Priya","Sanjay","Divya","Karthik",
    "Lakshmi","Manoj","Nisha","Pranav","Sneha","Varun","Yamini","Zoya",
    "Farhan","Imran","Neha","Suresh","Deepa","Rakesh","Pooja","Tarun"]
LAST_NAMES = ["Sharma","Iyer","Reddy","Nair","Gupta","Rao","Menon","Verma",
    "Pillai","Krishnan","Bose","Chatterjee","Desai","Kapoor","Mehta","Joshi",
    "Kulkarni","Bhat","Naidu","Shetty","Pandey","Singh","Agarwal","Mukherjee"]

CITIES_STATES_PIN = [
    ("Bengaluru","Karnataka","5600"), ("Chennai","Tamil Nadu","6000"),
    ("Hyderabad","Telangana","5000"), ("Mumbai","Maharashtra","4000"),
    ("Pune","Maharashtra","4110"), ("Delhi","Delhi","1100"),
    ("Kolkata","West Bengal","7000"), ("Ahmedabad","Gujarat","3800"),
    ("Kochi","Kerala","6820"), ("Coimbatore","Tamil Nadu","6410"),
]

DEVICES = ["Android App","iOS App","Desktop Web","Mobile Web"]
PAYMENTS = ["UPI","Credit Card","Debit Card","Net Banking","Cash on Delivery","Wallet"]
CATEGORIES = ["Electronics","Fashion","Grocery","Home & Kitchen","Beauty",
              "Sports & Fitness","Books","Toys & Baby","Footwear","Furniture"]
LOYALTY = ["Silver","Gold","Platinum","None"]
PROFESSIONS = ["Software Engineer","Teacher","Bank Employee","Business Owner",
    "Student","Doctor","Marketing Executive","Government Employee",
    "Freelance Designer","Accountant","Sales Executive","Consultant","Retired"]

N_A = 600
N_B_ONLY = 550
OVERLAP = 380


def random_dob(min_age=18, max_age=65):
    today = date(2026, 1, 1)
    age_days = random.randint(min_age*365, max_age*365)
    return today - timedelta(days=age_days)


def make_person(pid_prefix, idx):
    fn = random.choice(FIRST_NAMES)
    ln = random.choice(LAST_NAMES)
    city, state, pin_prefix = random.choice(CITIES_STATES_PIN)
    pincode = pin_prefix + str(random.randint(10, 99))
    dob = random_dob()
    gender = random.choice(["Male", "Female", "Other"])
    return {
        "full_name": f"{fn} {ln}", "first_name": fn, "last_name": ln,
        "gender": gender, "dob": dob, "city": city, "state": state, "pincode": pincode,
    }


overlap_people = [make_person("OV", i) for i in range(OVERLAP)]
a_only_people = [make_person("AO", i) for i in range(N_A - OVERLAP)]
b_only_people = [make_person("BO", i) for i in range(N_B_ONLY)]

rows_a = []
for i, person in enumerate(overlap_people + a_only_people):
    cust_id = f"SN{100000+i}"
    email = f"{person['first_name'].lower()}.{person['last_name'].lower()}{random.randint(1,999)}@mailbox.com"
    phone = f"9{random.randint(100000000,999999999)}"
    ip = f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
    card_last4 = f"{random.randint(0,9999):04d}"
    rows_a.append({
        "Customer_ID": cust_id, "Full_Name": person["full_name"], "Email": email,
        "Phone_Number": phone, "Gender": person["gender"], "Date_of_Birth": person["dob"].isoformat(),
        "Pincode": person["pincode"], "City": person["city"], "State": person["state"],
        "Device_Type": random.choice(DEVICES), "Payment_Method": random.choice(PAYMENTS),
        "Product_Category": random.choice(CATEGORIES),
        "Order_Amount_INR": round(float(np.random.gamma(3.2, 850)), 2),
        "Loyalty_Tier": random.choice(LOYALTY), "Last_Login_IP": ip, "Card_Last4": card_last4,
        "Signup_Date": (date(2026,1,1) - timedelta(days=random.randint(30, 1800))).isoformat(),
    })
random.shuffle(rows_a)
df_a = pd.DataFrame(rows_a)

rows_b = []
for i, person in enumerate(overlap_people + b_only_people):
    rows_b.append({
        "Public_Profile_ID": f"PUB{200000+i}", "Full_Name": person["full_name"],
        "Gender": person["gender"], "Date_of_Birth": person["dob"].isoformat(),
        "Pincode": person["pincode"], "City": person["city"],
        "Profession": random.choice(PROFESSIONS), "Public_Review_Count": random.randint(0, 120),
    })
random.shuffle(rows_b)
df_b = pd.DataFrame(rows_b)

df_a.to_csv("data/Dataset_A_original_ShopNest.csv", index=False)
df_b.to_csv("data/Dataset_B_auxiliary_PublicDirectory.csv", index=False)
with open("data/_ground_truth_overlap_count.txt", "w") as f:
    f.write(str(OVERLAP))
print("Dataset A:", df_a.shape, "Dataset B:", df_b.shape)
