import subprocess
import json

def get_issue_body():
    try:
        # Run jq command to extract issue body from GITHUB_EVENT_PATH
        result = subprocess.run(['jq', '-r', '.issue.body', '$GITHUB_EVENT_PATH'], capture_output=True, text=True)
        # Parse the output as JSON
        issue_body = json.loads(result.stdout.strip())
        return issue_body
    except Exception as e:
        print(f"Error: {e}")
        return None

def write_to_file(issue_body, filename):
    try:
        # Write issue body to the specified file
        with open(filename, 'w') as file:
            file.write(issue_body)
        print(f"Issue body written to {filename}")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    issue_body = get_issue_body()
    if issue_body:
        # Specify the filename where you want to write the issue body
        filename = "issue_body.txt"
        write_to_file(issue_body, filename)
    else:
        print("Failed to retrieve issue body.")
