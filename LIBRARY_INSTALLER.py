import subprocess

# List of libraries to install
libraries = [
    'pygame',
    'customtkinter'  # Replace with the actual name of your custom library
    ]

# Function to install libraries
def install_libraries():
    for lib in libraries:
        try:
            subprocess.check_call(['pip', 'install', lib])
            print(f"Successfully installed {lib}")
        except subprocess.CalledProcessError:
            print(f"Failed to install {lib}")

if __name__ == "__main__":
    install_libraries()