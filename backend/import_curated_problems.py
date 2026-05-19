#!/usr/bin/env python3
"""
Import Curated Problems - High-quality problems with full descriptions
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.curated_problem_importer import CuratedProblemImporter

if __name__ == "__main__":
    importer = CuratedProblemImporter()
    importer.import_curated_problems()
