import subprocess
import sys

# Try importing tabulate, and install it if necessary
try:
    from tabulate import tabulate
    print("Tabulate... ---> Installed!")
except ImportError:
    print("tabulate is not installed. Installing tabulate...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "tabulate", "--break-system-packages"])
        from tabulate import tabulate

        print("tabulate installed successfully.")
    except subprocess.CalledProcessError:
        try:
            from tabulate import tabulate

            print("Tabulate... ---> Installed Successfully!")
        except ImportError:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "tabulate"])
                from tabulate import tabulate

                print("Tabulate... ---> Installed Successfully!")
            except subprocess.CalledProcessError as e:
                print(f"Failed to install tabulate: {e}")
                sys.exit(1)

SHELL_COMMANDS = {
    'Write Health': "smartctl -A /dev/disk0 | grep 'Data.*W' | cut -d '[' -f 2 | awk '{print $1}'",
    'Read Health': "smartctl -A /dev/disk0 | grep 'Data.*R' | cut -d '[' -f 2 | awk '{print $1}'"
}


def is_installed(command):
    """Check if a command is installed by trying to locate it."""
    try:
        subprocess.check_output(["which", command], stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False


def install_homebrew():
    """Install Homebrew if it is not installed."""
    try:
        print("Homebrew is not installed. Installing Homebrew...")
        subprocess.check_call(
            ["/bin/bash", "-c", "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"]
        )
        print("Homebrew installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Homebrew: {e}")
        sys.exit(1)


def install_smartctl():
    """Install smartctl via Homebrew if smartctl is not installed."""
    try:
        print("smartctl is not installed. Installing via Homebrew...")
        subprocess.check_call(["brew", "install", "smartmontools"])
        print("smartctl installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install smartctl via Homebrew: {e}")
        sys.exit(1)


def get_health_data():
    """Execute SMART command and calculate health percentage."""
    health_percentages = {}
    for attr, command in SHELL_COMMANDS.items():
        try:
            # Run the shell command
            result = subprocess.check_output(command, shell=True, stderr=subprocess.PIPE)
            # Process the output (using 256 TB as maximum read/write value(s))
            raw_value = 256 - float(result.decode("utf-8").split()[0])
            health_percentage = round(raw_value / 256 * 100, 2)
            health_percentages.update({attr: f"{health_percentage}%"})
        except subprocess.CalledProcessError as e:
            # Handle error in case the command fails
            print(f"Error executing command: {command}\n{e}")
            health_percentages.update({attr: "Error"})

    return health_percentages


def main():
    """Main function to print the health status."""
    # Check if Homebrew is installed; if not, install it
    if not is_installed("brew"):
        install_homebrew()
    else:
        print("Homebrew... ---> Installed!")

    # Check if smartctl is installed; if not, install it
    if not is_installed("smartctl"):
        install_smartctl()
    else:
        print("smartmontools... ---> Installed!")

    # Get health data
    health_data = get_health_data()

    # Prepare the data for the table
    table_data = []
    headers = ["Attribute", "Health"]
    for attr_key, value in health_data.items():
        table_data.append([attr_key, value])

    # Print the table
    print(f"\n{subprocess.check_output('/bin/hostname', shell=True, stderr=subprocess.PIPE).decode('utf-8').strip()}"
          f" | {subprocess.check_output('date', shell=True, stderr=subprocess.PIPE).decode('utf-8').strip()}")
    print(tabulate(table_data, headers=headers, tablefmt="grid"))


if __name__ == "__main__":
    main()
