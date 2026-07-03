# ---------------------------------------------------------
# Dummy Users (Temporary)
# Replace with PostgreSQL in a future sprint.
# ---------------------------------------------------------
from typing import Dict
from app.core.security import hash_password




users_db: Dict[str, Dict[str, str]] = {
    "Tony": {"password": hash_password("password123"), "role": "engineering"},
    "Bruce": {"password": hash_password("securepass"), "role": "marketing"},
    "Sam": {"password": hash_password("financepass"), "role": "finance"},
    "Peter": {"password": hash_password("pete123"), "role": "engineering"},
    "Sid": {"password": hash_password("sidpass123"), "role": "marketing"},
    "Natasha": {"password": hash_password("hrpass123"), "role": "hr"},
    "Alice": {"password": hash_password("ceopass"), "role": "c-levelexecutives"},
    "Bob": {"password": hash_password("employeepass"), "role": "employee"},
}