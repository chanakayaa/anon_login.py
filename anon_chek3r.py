import ftplib
from smbprotocol.connection import Connection
from smbprotocol.exceptions import SMBException
from smbprotocol.session import Session
from smbprotocol.tree import TreeConnect
#from smbprotocol.file import Open
from smbprotocol.open import Open
 

def print_banner():
    banner = r"""

     _    _   _   ____  _   _   ____ _               _             
    / \  | \ | | / ___|| \ | | / ___| |__   ___  ___| | _____ _ __
   / _ \ |  \| | \___ \|  \| || |   | '_ \ / _ \/ __| |/ / _ \ '__|
  / ___ \| |\  |  ___) | |\  || |___| | | |  __/ (__|   <  __/ |   
/_/   \_\_| \_| |____/|_| \_| \____|_| |_|\___|\___|_|\_\___|_|   
                                                                    
 
                 Tool: ANON CHECKER (FTP & SMB)
                 Author: Pushkar Singh
    """
    print(banner)
 
def check_ftp_anonymous_access(ip_address, check_privilege=False):
    try:
        ftp = ftplib.FTP(ip_address, timeout=5)  # Connect with a 5-second timeout
        ftp.login('anonymous', 'anonymous')  # Attempt anonymous login
 
        if check_privilege:
            try:
                # Check read privilege
                ftp.retrlines('LIST')  # List files in the directory
                print(f"FTP Read access enabled on {ip_address}")
            except:
                print(f"FTP Read access disabled on {ip_address}")
 
            try:
                # Check write privilege
                ftp.storbinary('STOR test.txt', open(__file__, 'rb'))
                ftp.delete('test.txt')  # Clean up after the test
                print(f"FTP Write access enabled on {ip_address}")
            except:
                print(f"FTP Write access disabled on {ip_address}")
 
        ftp.quit()
        return True  # Anonymous access enabled
    except Exception:
        return False  # Anonymous access disabled
 
def check_smb_anonymous_access(ip_address, check_privilege=False):
    try:
        connection = Connection(uuid="", server=ip_address, port=445, username="", password="")
        connection.connect(timeout=5)
 
        if check_privilege:
            try:
                session = Session(connection)
                session.connect()
                tree = TreeConnect(session, f"\\\\{ip_address}\\IPC$")
                tree.connect()
 
                # Check read access
                file_open = Open(tree, "test.txt", "r")
                file_open.close()
                print(f"SMB Read access enabled on {ip_address}")
            except:
                print(f"SMB Read access disabled on {ip_address}")
 
            try:
                # Check write access
                file_open = Open(tree, "test_write.txt", "w")
                file_open.close()
                print(f"SMB Write access enabled on {ip_address}")
            except:
                print(f"SMB Write access disabled on {ip_address}")
 
        connection.disconnect()
        return True  # Anonymous SMB bind enabled
    except SMBException:
        return False  # Anonymous SMB bind disabled
 
def main():
    # Print the fancy banner
    print_banner()
 
    # Ask the user for the IP file location
    ip_file = input("Enter the path to the IP file (e.g., ip.txt): ").strip()
 
    try:
        # Read IPs from the provided file
        with open(ip_file, "r") as file:
            ip_addresses = file.read().splitlines()
    except FileNotFoundError:
        print("Error: File not found! Please check the file path and try again.")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return
 
    # Ask user if they want to check for privileges
    check_privilege = input("Do you want to check for read/write privileges? (yes/no): ").strip().lower() == "yes"
 
    total_ips = len(ip_addresses)
    ftp_accessible_ips = []
    smb_accessible_ips = []
 
    # Check FTP and SMB anonymous access for each IP
    print("\nChecking FTP and SMB anonymous access...")
    for ip in ip_addresses:
        if check_ftp_anonymous_access(ip, check_privilege):
            ftp_accessible_ips.append(ip)
        if check_smb_anonymous_access(ip, check_privilege):
            smb_accessible_ips.append(ip)
 
    # Display results
    print("\nResults:")
    print(f"Total devices scanned: {total_ips}")
    print(f"Devices with FTP anonymous access enabled: {len(ftp_accessible_ips)}")
    print(f"Devices with SMB anonymous bind enabled: {len(smb_accessible_ips)}")
 
    if ftp_accessible_ips:
        print("\nIPs with FTP anonymous access enabled:")
        for ip in ftp_accessible_ips:
            print(ip)
 
    if smb_accessible_ips:
        print("\nIPs with SMB anonymous bind enabled:")
        for ip in smb_accessible_ips:
            print(ip)
 
if __name__ == "__main__":
    main()
