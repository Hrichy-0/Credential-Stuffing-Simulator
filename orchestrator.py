import requests
import random
import time 
import json
import os
import concurrent.futures
from faker import Faker

TARGET_URL = "http://127.0.0.1:5001/api/login"
fake = Faker()

# 1. generate the ground truth database.

def setup_database(num_users=1000):
    if not os.path.exists("database.json"):
        print(f"[*] Generating database with {num_users} users...")
        db = {}
        for _ in range(num_users):
            db[fake.user_name()] = fake.password(length=12)

        with open("database.json", "w") as f:
            json.dump(db, f, indent=4)
        print("[+] Database generated successfully!")

    with open("database.json", "r") as f:
        return json.load(f)

#load the database into memory so our workers know who the real users are
USER_DB = setup_database()
USERNAMES = list(USER_DB.keys())

# 2.The thread workers will simulate human traffic and attacker bot traffic concurrently.
def human_worker():
    """Simulates normal humans logging in with occasional typos."""
    my_ip = fake.ipv4()
    my_ua = fake.user_agent()
    
    # THE FIX: The human picks their ONE specific account before the loop starts
    my_account = random.choice(USERNAMES)
    real_password = USER_DB[my_account]
    
    for _ in range(20): # Each human thread does 20 actions
        # 20% chance of a typo
        attempt_pw = real_password + "oops" if random.random() < 0.20 else real_password
            
        payload = {"username": my_account, "password": attempt_pw}
        headers = {"User-Agent": my_ua, "X-Forwarded-For": my_ip}
        
        requests.post(TARGET_URL, json=payload, headers=headers)
        time.sleep(random.uniform(0.5, 2.0)) # Humans type slowly

def brute_force_worker():
    """Simulates a noisy botnet slamming the server from one IP."""
    # THE FIX: Generate the IP outside the loop!
    fake_ip = fake.ipv4() 
    
    for _ in range(50): # Rapid fire 50 attempts
        payload = {
            "username": random.choice(USERNAMES),
            "password": fake.password() # Total random guess
        }
        headers = {"User-Agent": "curl/7.68.0", "X-Forwarded-For": fake_ip}
        
        requests.post(TARGET_URL, json=payload, headers=headers)
        time.sleep(random.uniform(0.01, 0.05)) # Blistering fast

def password_sprayer_worker():
    """Simulates a sneaky bot trying ONE common password on many accounts."""
    sneaky_ip = fake.ipv4()
    common_password = "Spring2026!"
    
    for _ in range(15): 
        payload = {
            "username": random.choice(USERNAMES),
            "password": common_password
        }
        headers = {"User-Agent": "python-requests/2.28.1", "X-Forwarded-For": sneaky_ip}
        
        requests.post(TARGET_URL, json=payload, headers=headers)
        time.sleep(random.uniform(1.0, 3.0)) # Low and slow to avoid detection

# 3. THE MULTI-THREADING ENGINE

if __name__ == '__main__':
    print("[*] Initiating Cyber Range Orchestrator...")
    print("[*] Unleashing threaded traffic against the API. Press Ctrl+C to abort.")
    
    # We create a pool of simultaneous threads to stress test the API
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        futures = []
        
        # Launch 15 Human Threads
        for _ in range(15):
            futures.append(executor.submit(human_worker))
            
        # Launch 10 Brute Force Threads
        for _ in range(10):
            futures.append(executor.submit(brute_force_worker))
            
        # Launch 5 Password Sprayer Threads
        for _ in range(5):
            futures.append(executor.submit(password_sprayer_worker))
            
        # Wait for all threads to finish their loops
        concurrent.futures.wait(futures)
        
    print("\n[*] Mega-Simulation Complete! Check your login_attempts.jsonl file.")
        

