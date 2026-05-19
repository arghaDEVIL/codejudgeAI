#!/usr/bin/env python3
"""
Enhanced Problem Importer CLI - Import problems with full descriptions
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.enhanced_problem_importer import EnhancedProblemImporter


def main():
    print("🚀 Enhanced Problem Importer - Full Problem Descriptions")
    print("=" * 60)
    print("This importer fetches REAL problem descriptions from web pages!")
    print("=" * 60)

    importer = EnhancedProblemImporter()

    print("\n📊 Available Options:")
    print("1. 📚 Enhanced Sample Problems (3 with detailed descriptions)")
    print("2. 🏆 Codeforces Easy Problems (5 with full descriptions)")
    print("3. 🔥 Codeforces Medium Problems (5 with full descriptions)")
    print("4. 🚀 Import All Enhanced (Sample + Easy)")
    print("0. Exit")

    print("\n⚠️  Note: Codeforces imports take longer (2-3 seconds per problem)")
    print("   because we fetch full problem descriptions from web pages.")

    while True:
        try:
            choice = input("\n🔥 Select an option (0-4): ").strip()

            if choice == "0":
                print("👋 Goodbye!")
                break

            elif choice == "1":
                print("\n📥 Importing enhanced sample problems...")
                print("   These have detailed descriptions, examples, and hints!")
                count = importer.import_sample_problems_with_full_descriptions()
                print(f"✅ Successfully imported {count} enhanced sample problems!")

            elif choice == "2":
                print("\n📥 Importing Easy problems from Codeforces...")
                print("   Fetching full problem descriptions from web pages...")
                print("   This will take about 10-15 seconds...")
                count = importer.import_from_codeforces_with_descriptions(
                    limit=5, min_rating=800, max_rating=1000
                )
                print(
                    f"✅ Successfully imported {count} Easy problems with full descriptions!"
                )

            elif choice == "3":
                print("\n📥 Importing Medium problems from Codeforces...")
                print("   Fetching full problem descriptions from web pages...")
                print("   This will take about 10-15 seconds...")
                count = importer.import_from_codeforces_with_descriptions(
                    limit=5, min_rating=1000, max_rating=1500
                )
                print(
                    f"✅ Successfully imported {count} Medium problems with full descriptions!"
                )

            elif choice == "4":
                print("\n📥 Importing all enhanced problems...")
                print(
                    "   This will import sample problems + 5 Easy Codeforces problems"
                )
                print("   Total time: ~15-20 seconds")

                count1 = importer.import_sample_problems_with_full_descriptions()
                print(f"   ✅ Imported {count1} sample problems")

                count2 = importer.import_from_codeforces_with_descriptions(
                    limit=5, min_rating=800, max_rating=1200
                )
                print(f"   ✅ Imported {count2} Codeforces problems")

                total = count1 + count2
                print(f"🎉 Total imported: {total} problems with full descriptions!")

            else:
                print("❌ Invalid choice. Please select 0-4.")

        except KeyboardInterrupt:
            print("\n\n👋 Interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("   Try again or check your internet connection.")


if __name__ == "__main__":
    main()
