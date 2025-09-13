import subprocess

def get_wifi_passwords():
    # Get list of all Wi-Fi profiles
    profiles_output = subprocess.check_output("netsh wlan show profiles", shell=True, text=True)
    profiles = []

    for line in profiles_output.splitlines():
        if "All User Profile" in line:
            profile_name = line.split(":")[1].strip()
            profiles.append(profile_name)

    wifi_details = []

    for profile in profiles:
        # Get details of each profile
        profile_details = subprocess.check_output(
            f'netsh wlan show profile name="{profile}" key=clear',
            shell=True, text=True
        )

        password = "N/A"
        for line in profile_details.splitlines():
            if "Key Content" in line:
                password = line.split(":")[1].strip()

        wifi_details.append({
            "SSID": profile,
            "Password": password
        })

    return wifi_details


def save_to_file(data, filename="wifi_passwords.txt"):
    with open(filename, "w", encoding="utf-8") as file:
        for wifi in data:
            file.write(f"SSID     : {wifi['SSID']}\n")
            file.write(f"Password : {wifi['Password']}\n")
            file.write("=" * 50 + "\n")

    print(f"[>] Wi-Fi passwords saved to {filename}")


if __name__ == "__main__":
    print("[>] Extracting saved Wi-Fi passwords...")
    wifi_data = get_wifi_passwords()

    if wifi_data:
        save_to_file(wifi_data)
        print("[>] Extraction complete!")
    else:
        print("[!] No Wi-Fi profiles found.")
