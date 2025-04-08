import os
import py_compile


def check_syntax(base_dir=".", output_file="code_check_report.txt"):
    with open(output_file, "w", encoding="utf-8") as report:
        report.write("🔍 Python Syntax Check Report\n\n")
        for root, _, files in os.walk(base_dir):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    try:
                        py_compile.compile(file_path, doraise=True)
                        report.write(f"✅ {file_path}\n")
                    except py_compile.PyCompileError as e:
                        report.write(f"❌ {file_path} has syntax error:\n")
                        report.write(f"{e}\n\n")

        report.write("\n✅ Done. Open this file to review results.\n")


if __name__ == "__main__":
    check_syntax()
    print("[✔] Syntax check complete. See 'code_check_report.txt' for details.")
