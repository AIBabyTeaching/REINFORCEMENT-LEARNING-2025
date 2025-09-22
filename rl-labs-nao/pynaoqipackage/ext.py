import os

def extract_folder_structure(directory):
    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        # Print the current directory path
        print(f"Directory: {root}")
        
        # Print the subdirectories
        if dirs:
            print("Subdirectories:")
            for dir_name in dirs:
                print(f"    {dir_name}")
        else:
            print("    No subdirectories")

        # Print the files
        if files:
            print("Files:")
            for file_name in files:
                print(f"    {file_name}")
        else:
            print("    No files")
        
        print()  # Empty line for better readability

# Example usage:
directory_path = ['lib','share','bin']
for path in directory_path:
	extract_folder_structure(path)
