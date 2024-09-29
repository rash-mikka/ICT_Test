import os
import random
from datetime import datetime, timedelta

BUSINESS_HOURS_START = 9
BUSINESS_HOURS_END = 18

# Function to generate random internal or external IP addresses
def generate_random_ip(external_chance=0.1):
    if random.random() < external_chance:  # Probability of external IP
        # Generate an external IP address
        return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
    else:
        # Generate an internal IP address (e.g., 192.168.x.x or 10.x.x.x)
        internal_prefixes = ['192.168', '10']
        selected_prefix = random.choice(internal_prefixes)
        if selected_prefix == '192.168':
            return f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}"
        else:
            return f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

# Function to generate synthetic logs
def generate_synthetic_logs(start_timestamp, host_name, source_ip, user_acc, event_outcome, num_logs):
    logs = []
    for i in range(num_logs):
        formatted_timestamp = start_timestamp.strftime('%b %d %H:%M:%S')

        process_id = random.randint(10000, 50000)
        port = random.randint(1024, 65535)

        if event_outcome == 'success':
            log = f"{formatted_timestamp} {host_name} sshd[{process_id}]: Accepted password for {user_acc} from {source_ip} port {port} ssh2"
        else:
            log = f"{formatted_timestamp} {host_name} sshd[{process_id}]: Failed password for {user_acc} from {source_ip} port {port} ssh2"

        logs.append((start_timestamp, log))

    return logs

# Function to generate daily activity logs for 10 users
def generate_daily_activity_logs():
    logs = []
    users = [f"user{i}" for i in range(1, 11)]  # 10 users
    host_name = "server01"

    for user in users:
        # Generate 10 login events throughout the business hours
        for _ in range(10):
            login_time = generate_random_business_hours_time()
            # Randomly decide if the IP is internal or external (10% chance for external by default)
            source_ip = generate_random_ip(external_chance=0.1)
            logs.extend(generate_synthetic_logs(login_time, host_name, source_ip, user, 'success', 1))

        # Random chance for brute force attack (multiple failed attempts, 80% chance for external IP)
        if random.random() < 0.2:  # 20% chance for brute force attack
            brute_force_time = generate_random_business_hours_time()
            source_ip = generate_random_ip(external_chance=0.8)  # 80% chance it's external
            logs.extend(generate_synthetic_logs(brute_force_time, host_name, source_ip, user, 'fail', random.randint(5, 10)))

        # Random chance for off-hours login attempt
        if random.random() < 0.3:  # 30% chance for login outside business hours
            off_hours_time = generate_random_off_hours_time()
            source_ip = generate_random_ip(external_chance=0.1)  # Regular 10% chance for external IP
            logs.extend(generate_synthetic_logs(off_hours_time, host_name, source_ip, user, 'success', 1))

    # Add a password spray attack (same password on multiple users, 80% chance for external IP)
    logs.extend(generate_password_spray_attack(users, host_name))

    # Sort logs by timestamp
    logs.sort(key=lambda x: x[0])

    # Extract just the log messages, discarding the timestamp
    return [log for _, log in logs]

# Function to generate a password spray attack (80% external IP chance)
def generate_password_spray_attack(users, host_name):
    logs = []
    # Simulate a password spray attack at a random time
    spray_attack_time = generate_random_off_hours_time()

    # Choose a random external IP for the attack (80% chance)
    source_ip = generate_random_ip(external_chance=0.8)

    # The attacker tries the same password on multiple user accounts (all failed attempts)
    for user in users:
        logs.extend(generate_synthetic_logs(spray_attack_time, host_name, source_ip, user, 'fail', 1))

    return logs

# Helper function to generate a random time during business hours
def generate_random_business_hours_time():
    today = datetime.now().replace(hour=BUSINESS_HOURS_START, minute=0, second=0, microsecond=0)
    random_hours = random.randint(0, BUSINESS_HOURS_END - BUSINESS_HOURS_START)
    random_minutes = random.randint(0, 59)
    random_seconds = random.randint(0, 59)
    return today + timedelta(hours=random_hours, minutes=random_minutes, seconds=random_seconds)

# Helper function to generate a random time outside business hours
def generate_random_off_hours_time():
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    if random.random() < 0.5:
        random_hours = random.randint(0, BUSINESS_HOURS_START - 1)  # Midnight to 9 AM
    else:
        random_hours = random.randint(BUSINESS_HOURS_END, 23)  # 6 PM to Midnight
    random_minutes = random.randint(0, 59)
    random_seconds = random.randint(0, 59)
    return today + timedelta(hours=random_hours, minutes=random_minutes, seconds=random_seconds)

# Function to save logs into a single file
def save_logs(logs):
    os.makedirs('logs', exist_ok=True)
    log_number = 1
    # Check for existing files and increment log number
    while os.path.exists(f"logs/sshloginlogs_{log_number}.txt"):
        log_number += 1
    log_filename = f"logs/sshloginlogs_{log_number}.txt"

    # Write all logs into a single file
    with open(log_filename, 'w') as file:
        for log in logs:
            file.write(log + '\n')

    print(f"Logs saved to {log_filename}")