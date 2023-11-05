import subprocess
import json

def get_issue_fields():
    try:
        # Run jq command to extract all fields of the issue from GITHUB_EVENT_PATH
        result = subprocess.run(['jq', '.issue', '$GITHUB_EVENT_PATH'], capture_output=True, text=True)
        print(f'Command output: {result.stdout}')  # Debugging line
        # Parse the output as JSON
        issue_fields = json.loads(result.stdout.strip())
        return issue_fields
    except Exception as e:
        print(f"Error: {e}")
        return None

def write_to_file(data, filename):
    try:
        # Write data to the specified file in JSON format
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Issue fields written to {filename}")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    issue_fields = get_issue_fields()
    if issue_fields:
        # Specify the filename where you want to write the issue fields as JSON
        filename = "issue_fields.json"
        write_to_file(issue_fields, filename)
    else:
        print("Failed to retrieve issue fields.")
