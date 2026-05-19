#!/usr/bin/env python3
"""
Problem Importer CLI - Easy way to import problems from various sources
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.problem_importer import ProblemImporter


def main():
    print("🚀 Problem Importer - Automated Problem Collection")
    print("=" * 50)

    importer = ProblemImporter()

    # Show current stats
    print("\n📊 Current Database Stats:")
    stats = importer.get_import_stats()
    print(f"   Total Problems: {stats.get('total_problems', 0)}")
    print(f"   Easy: {stats.get('difficulty_distribution', {}).get('Easy', 0)}")
    print(f"   Medium: {stats.get('difficulty_distribution', {}).get('Medium', 0)}")
    print(f"   Hard: {stats.get('difficulty_distribution', {}).get('Hard', 0)}")

    print("\n🎯 Available Import Sources:")
    print("1. Sample Problems (6 curated problems)")
    print("2. Codeforces API (Easy: 800-1000 rating)")
    print("3. Codeforces API (Medium: 1000-1500 rating)")
    print("4. Codeforces API (Hard: 1500+ rating)")
    print("5. Import All Sample + Codeforces Easy")
    print("6. Show detailed statistics")
    print("0. Exit")

    while True:
        try:
            choice = input("\n🔥 Select an option (0-6): ").strip()

            if choice == "0":
                print("👋 Goodbye!")
                break
            elif choice == "1":
                print("\n📥 Importing sample problems...")
                count = importer.import_sample_problems()
                print(f"✅ Successfully imported {count} sample problems!")

            elif choice == "2":
                print("\n📥 Importing Easy problems from Codeforces...")
                count = importer.import_from_codeforces(
                    limit=15, min_rating=800, max_rating=1000
                )
                print(f"✅ Successfully imported {count} Easy problems!")

            elif choice == "3":
                print("\n📥 Importing Medium problems from Codeforces...")
                count = importer.import_from_codeforces(
                    limit=15, min_rating=1000, max_rating=1500
                )
                print(f"✅ Successfully imported {count} Medium problems!")

            elif choice == "4":
                print("\n📥 Importing Hard problems from Codeforces...")
                count = importer.import_from_codeforces(
                    limit=10, min_rating=1500, max_rating=2000
                )
                print(f"✅ Successfully imported {count} Hard problems!")

            elif choice == "5":
                print("\n📥 Importing sample problems + Easy Codeforces problems...")
                count1 = importer.import_sample_problems()
                count2 = importer.import_from_codeforces(
                    limit=20, min_rating=800, max_rating=1200
                )
                total = count1 + count2
                print(
                    f"✅ Successfully imported {total} problems ({count1} sample + {count2} Codeforces)!"
                )

            elif choice == "6":
                print("\n📊 Detailed Statistics:")
                stats = importer.get_import_stats()
                print(f"   Total Problems: {stats.get('total_problems', 0)}")

                diff_dist = stats.get("difficulty_distribution", {})
                print(f"   🟢 Easy: {diff_dist.get('Easy', 0)}")
                print(f"   🟡 Medium: {diff_dist.get('Medium', 0)}")
                print(f"   🔴 Hard: {diff_dist.get('Hard', 0)}")

                print(f"\n   📚 Total Tags: {stats.get('total_tags', 0)}")
                print("   🏷️  Top Tags:")
                for tag, count in stats.get("top_tags", [])[:8]:
                    print(f"      {tag}: {count} problems")

            else:
                print("❌ Invalid choice. Please select 0-6.")

        except KeyboardInterrupt:
            print("\n\n👋 Interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
