# audit_files.py
import os

print("\n📂 Auditing Python files in this project...")

for root, _, files in os.walk("."):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            print(f"\n🗂️ {file}")
            print(f"📍 Path: {path}")
            try:
                with open(path, encoding="utf-8") as f:
                    preview = [f.readline().strip() for _ in range(10)]
                    print("🔍 Preview:")
                    for line in preview:
                        print("   ", line)
            except Exception as e:
                print(f"⚠️ Could not read file: {e}")

print("\n✅ Audit complete.")
