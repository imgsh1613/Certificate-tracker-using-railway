#!/usr/bin/env python3
"""
Database setup script for deployment
Run this after deployment to initialize the database
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the database setup
try:
    from database import *
    print("✅ Database setup completed successfully!")
    print("🎯 Your application is ready to use!")
    print("\nNext steps:")
    print("1. Register as a teacher or student")
    print("2. If you're a teacher, add students using their email addresses")
    print("3. Students can upload certificates for verification")
except Exception as e:
    print(f"❌ Database setup failed: {str(e)}")
    sys.exit(1)
