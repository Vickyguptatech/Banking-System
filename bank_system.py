"""
========================================================
  BANKING SYSTEM - Mini Project
  Founder / Developer: Vicky Kumar
========================================================
A menu-driven Python console application that simulates
basic banking operations with persistent JSON storage.

Concepts used: Variables, Data Types, Conditionals, Loops,
Functions, Lists & Dictionaries, String Operations,
Modules (random, datetime, json, time, os)
========================================================
"""

import json
import os
import random
import time
from datetime import datetime

DATA_FILE = "accounts.json"


# ---------------------------------------------------------
#  UTILITY / ANIMATION FUNCTIONS
# ---------------------------------------------------------
def typewriter(text, delay=0.02):
    """Prints text letter by letter for a nice animated effect."""
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()


def loading(text="Processing", dots=3, delay=0.3):
    """Simple loading animation using dots."""
    print(text, end="", flush=True)
    for _ in range(dots):
        time.sleep(delay)
        print(".", end="", flush=True)
    time.sleep(delay)
    print(" ✅")


def banner():
    art = r"""
   ____              _    _             
  |  _ \            | |  (_)            
  | |_) | __ _ _ __  | | ___ _ __   __ _ 
  |  _ < / _` | '_ \ | |/ / | '_ \ / _` |
  | |_) | (_| | | | ||   <| | | | | (_| |
  |____/ \__,_|_| |_|_|\_\_|_| |_|\__, |
                                   __/ |
        S Y S T E M               |___/
"""
    print(art)
    typewriter("💰 Welcome to Vicky Bank — Your Trusted Digital Banking System 💰", 0.015)
    print("-" * 60)


def pause():
    input("\nPress Enter to continue...")


# ---------------------------------------------------------
#  DATA HANDLING (JSON persistence)
# ---------------------------------------------------------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def generate_account_number(data):
    while True:
        acc_no = str(random.randint(100000, 999999))
        if acc_no not in data:
            return acc_no


def now_str():
    return datetime.now().strftime("%d-%m-%Y %I:%M %p")


# ---------------------------------------------------------
#  CORE FEATURES
# ---------------------------------------------------------
def create_account(data):
    print("\n📝 CREATE NEW ACCOUNT")
    print("-" * 30)
    name = input("Enter your full name: ").strip()
    phone = input("Enter your phone number: ").strip()

    while True:
        pin = input("Set a 4-digit PIN: ").strip()
        if pin.isdigit() and len(pin) == 4:
            break
        print("⚠️  PIN must be exactly 4 digits. Try again.")

    acc_no = generate_account_number(data)

    data[acc_no] = {
        "name": name,
        "phone": phone,
        "pin": pin,
        "balance": 0,
        "history": []
    }
    save_data(data)

    loading("\nCreating your account")
    print("\n🎉 Account created successfully!")
    print(f"👤 Name           : {name}")
    print(f"🏦 Account Number : {acc_no}")
    print("⚠️  Please save your account number safely. You'll need it to log in.")
    pause()


def login(data):
    print("\n🔐 LOGIN")
    print("-" * 30)
    acc_no = input("Enter Account Number: ").strip()
    if acc_no not in data:
        print("❌ Account not found.")
        pause()
        return None

    pin = input("Enter PIN: ").strip()
    if pin != data[acc_no]["pin"]:
        print("❌ Incorrect PIN.")
        pause()
        return None

    loading("Logging you in")
    print(f"\n✅ Welcome back, {data[acc_no]['name']}!")
    time.sleep(0.5)
    return acc_no


def check_balance(data, acc_no):
    print(f"\n💰 Current Balance: ₹{data[acc_no]['balance']}")
    pause()


def deposit(data, acc_no):
    print("\n➕ DEPOSIT MONEY")
    try:
        amount = float(input("Enter amount to deposit: ₹"))
        if amount <= 0:
            print("⚠️  Enter a valid positive amount.")
            pause()
            return
    except ValueError:
        print("⚠️  Invalid input.")
        pause()
        return

    loading("Processing deposit")
    data[acc_no]["balance"] += amount
    data[acc_no]["history"].append({
        "type": "Deposit",
        "amount": amount,
        "date": now_str(),
        "balance_after": data[acc_no]["balance"]
    })
    save_data(data)
    print(f"✅ ₹{amount} deposited successfully! New Balance: ₹{data[acc_no]['balance']}")
    pause()


def withdraw(data, acc_no):
    print("\n➖ WITHDRAW MONEY")
    try:
        amount = float(input("Enter amount to withdraw: ₹"))
        if amount <= 0:
            print("⚠️  Enter a valid positive amount.")
            pause()
            return
    except ValueError:
        print("⚠️  Invalid input.")
        pause()
        return

    if amount > data[acc_no]["balance"]:
        print("❌ Insufficient balance!")
        pause()
        return

    loading("Processing withdrawal")
    data[acc_no]["balance"] -= amount
    data[acc_no]["history"].append({
        "type": "Withdraw",
        "amount": amount,
        "date": now_str(),
        "balance_after": data[acc_no]["balance"]
    })
    save_data(data)
    print(f"✅ ₹{amount} withdrawn successfully! New Balance: ₹{data[acc_no]['balance']}")
    pause()


def transfer(data, acc_no):
    print("\n🔄 TRANSFER MONEY")
    receiver = input("Enter receiver's account number: ").strip()

    if receiver not in data:
        print("❌ Receiver account not found.")
        pause()
        return
    if receiver == acc_no:
        print("⚠️  You cannot transfer to your own account.")
        pause()
        return

    try:
        amount = float(input("Enter amount to transfer: ₹"))
        if amount <= 0:
            print("⚠️  Enter a valid positive amount.")
            pause()
            return
    except ValueError:
        print("⚠️  Invalid input.")
        pause()
        return

    if amount > data[acc_no]["balance"]:
        print("❌ Insufficient balance!")
        pause()
        return

    loading("Transferring funds")
    data[acc_no]["balance"] -= amount
    data[receiver]["balance"] += amount

    data[acc_no]["history"].append({
        "type": f"Transfer to {receiver}",
        "amount": amount,
        "date": now_str(),
        "balance_after": data[acc_no]["balance"]
    })
    data[receiver]["history"].append({
        "type": f"Received from {acc_no}",
        "amount": amount,
        "date": now_str(),
        "balance_after": data[receiver]["balance"]
    })
    save_data(data)
    print(f"✅ ₹{amount} transferred to {data[receiver]['name']} ({receiver}) successfully!")
    pause()


def view_history(data, acc_no):
    print("\n📜 TRANSACTION HISTORY")
    print("-" * 50)
    history = data[acc_no]["history"]
    if not history:
        print("No transactions yet.")
    else:
        for i, txn in enumerate(history, 1):
            print(f"{i}. [{txn['date']}] {txn['type']} — ₹{txn['amount']} "
                  f"(Balance: ₹{txn['balance_after']})")
    pause()


def change_pin(data, acc_no):
    print("\n🔑 CHANGE PIN")
    old_pin = input("Enter current PIN: ").strip()
    if old_pin != data[acc_no]["pin"]:
        print("❌ Incorrect current PIN.")
        pause()
        return

    new_pin = input("Enter new 4-digit PIN: ").strip()
    confirm_pin = input("Confirm new PIN: ").strip()

    if new_pin != confirm_pin:
        print("⚠️  PINs do not match.")
        pause()
        return
    if not (new_pin.isdigit() and len(new_pin) == 4):
        print("⚠️  PIN must be exactly 4 digits.")
        pause()
        return

    loading("Updating PIN")
    data[acc_no]["pin"] = new_pin
    save_data(data)
    print("✅ PIN changed successfully!")
    pause()


# ---------------------------------------------------------
#  MENUS
# ---------------------------------------------------------
def account_menu(data, acc_no):
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(f"👋 Hello, {data[acc_no]['name']}  |  Acc No: {acc_no}")
        print("=" * 40)
        print("1. 💰 Check Balance")
        print("2. ➕ Deposit")
        print("3. ➖ Withdraw")
        print("4. 🔄 Transfer")
        print("5. 📜 Transaction History")
        print("6. 🔑 Change PIN")
        print("7. 🚪 Logout")
        print("=" * 40)

        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            check_balance(data, acc_no)
        elif choice == "2":
            deposit(data, acc_no)
        elif choice == "3":
            withdraw(data, acc_no)
        elif choice == "4":
            transfer(data, acc_no)
        elif choice == "5":
            view_history(data, acc_no)
        elif choice == "6":
            change_pin(data, acc_no)
        elif choice == "7":
            print("👋 Logging out... See you soon!")
            time.sleep(1)
            break
        else:
            print("⚠️  Invalid choice. Try again.")
            pause()


def main_menu():
    data = load_data()
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        banner()
        print("1. 🆕 Create Account")
        print("2. 🔐 Login")
        print("3. ❌ Exit")
        print("-" * 60)

        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            create_account(data)
        elif choice == "2":
            acc_no = login(data)
            if acc_no:
                account_menu(data, acc_no)
        elif choice == "3":
            typewriter("\n🙏 Thank you for using Vicky Bank. Goodbye!")
            break
        else:
            print("⚠️  Invalid choice.")
            pause()


if __name__ == "__main__":
    main_menu()
