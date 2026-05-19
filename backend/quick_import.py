#!/usr/bin/env python3
"""
Quick import script for curated problems
"""

import sys
import os

# Add the backend directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

try:
    from app.services.curated_problem_importer import CuratedProblemImporter

    print("🚀 Importing Curated Problems...")
    print("=" * 40)

    importer = CuratedProblemImporter()
    count = importer.import_curated_problems()

    print(f"✅ Successfully imported {count} curated problems!")
    print("\n📊 Updated Stats:")

    stats = importer.get_import_stats()
    print(f"   Total Problems: {stats.get('total_problems', 0)}")
    print(f"   Easy: {stats.get('difficulty_distribution', {}).get('Easy', 0)}")
    print(f"   Medium: {stats.get('difficulty_distribution', {}).get('Medium', 0)}")
    print(f"   Hard: {stats.get('difficulty_distribution', {}).get('Hard', 0)}")

    print("\n🎉 Your platform now has professional-quality problems!")

except Exception as e:
    print(f"❌ Error: {e}")
    print("Make sure you're in the backend directory and the database is running.")
