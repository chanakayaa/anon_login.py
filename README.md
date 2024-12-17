### Summary:

This Python script is a security auditing tool designed to check for **anonymous FTP and SMB access** on a list of IP addresses. It performs the following key functions:

1. **FTP Anonymous Access Check**: The script connects to each IP address via FTP and attempts to log in using anonymous credentials (`anonymous:anonymous`). If successful, it can also check for read and write privileges by attempting to list files and upload/download a test file.

2. **SMB Anonymous Access Check**: It connects to the IP address on port 445 (SMB) and tries to establish an anonymous session. If the connection is successful, it checks for read and write access by attempting to open a test file for reading and writing.

3. **Privilege Checking**: The user is prompted to specify if they want to check for additional privileges (read/write). If chosen, the script will test if the FTP or SMB services allow for these actions.

4. **Results Display**: The script outputs the total number of devices scanned, the number of devices with FTP anonymous access, and the number of devices with SMB anonymous bind access. It then lists the IP addresses that have each of these vulnerabilities.

### Main Features:
- **FTP Access Check**: Attempts to log in anonymously and checks for read and write privileges.
- **SMB Access Check**: Checks for anonymous SMB binds and the ability to read and write files.
- **User Input**: Allows the user to specify the path to a file containing the list of IP addresses to scan.
- **Privilege Checking**: Optionally tests for FTP and SMB read/write privileges.

### Potential Use Cases:
- **Network Security Audits**: Identify devices with insecure anonymous FTP and SMB access in a network.
- **Vulnerability Assessment**: Check for potential entry points for unauthorized access to critical network services.
