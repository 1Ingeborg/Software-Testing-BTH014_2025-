import os

def parse_hash_file(file_path):
    result = {}
    current_obj = None
    with open(file_path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("[Object Name]"):
                current_obj = line.split("]")[1].strip()
            elif line.startswith("SHA256") and current_obj:
                result[current_obj] = line.split(":")[1].strip()
    return result

def compare_versions(linux_dir, windows_dir):
    print("🔍 Comparing hash outputs between Linux and Windows...\n")
    versions = ["py35", "py36", "py37", "py38", "py310", "py311"]
    for ver in versions:
        linux_file = os.path.join(linux_dir, f"{ver}.txt")
        win_file = os.path.join(windows_dir, f"{ver}.txt")

        if not os.path.exists(linux_file) or not os.path.exists(win_file):
            print(f"⚠️ Missing file for {ver}, skipping.")
            continue

        linux_hashes = parse_hash_file(linux_file)
        win_hashes = parse_hash_file(win_file)

        mismatches = []
        for key in linux_hashes:
            if key in win_hashes:
                if linux_hashes[key] != win_hashes[key]:
                    mismatches.append(key)

        if not mismatches:
            print(f"[✅] {ver}: All object hashes match.")
        else:
            print(f"[❌] {ver}: Mismatched objects: {', '.join(mismatches)}")

if __name__ == "__main__":
    # 修改为你的实际路径
    linux_output = "Linux/.hash_output"
    windows_output = "Window/.hash_output"
    compare_versions(linux_output, windows_output)
