import paramiko
from pathlib import Path
import pprint


def model_output():
# --- Configuration ---
    PRIVATE_KEY_FILE = Path(__file__).parent.parent / 'ssh' / 'my_resume_private_pem.pem'
    USER_NAME = 'root'
    HOST_NAME = '161.35.237.254'
    PORT = 22

    # --- SSH Connection ---

    # 1. Create a client instance
    client = paramiko.SSHClient()

    # 2. Set the policy to automatically add the host key (THE FIX)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # 3. Load your private key from the file
    # Note: It's good practice to convert the Path object to a string
    pkey = paramiko.RSAKey.from_private_key_file(str(PRIVATE_KEY_FILE))

    # 4. Connect using all the configured parts
    # print(f"Connecting to {HOST_NAME}...")
    client.connect(hostname=HOST_NAME, port=PORT, username=USER_NAME, pkey=pkey)
    # print("✅ Connection successful!")
    stdin, stdout, stderr = client.exec_command('tail -n 50 weatheralgo/log.log')

    output = stdout.read().decode()
    error = stderr.read().decode()

    # print("Output:", output)
    # print("Error:", error)

    # You can now use the client to run commands, etc.

    # 5. Always close the connection when you're done
    client.close()
    
    result = output or error
    # print(result)
    
    return result

# print(model_output())

# x = model_output()
# print(x)