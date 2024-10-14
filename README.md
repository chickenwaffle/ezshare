# ezshare.py

A quick-and-dirty file sharing tool using SFTP.

## What it does
- Securely uploads files over a network using SFTP.
- Automatically obfuscates the file name for added privacy.
- No information is shared or stored with any third party.

## Installation Requirements and Dependencies

**Required:**
- Python 3
- Paramiko (for SFTP functionality)
- Pyperclip (for clipboard operations)

You can install Paramiko and Pyperclip using pip:

```bash
pip install paramiko pyperclip
```

## Usage

### Drag and Drop

1. Clone or download the `ezshare.py` file to your local machine.
2. Make sure you have the required dependencies installed.
3. Simply drag and drop your file onto the script, then follow the instructions provided in the script.

### Command Line Execution

ezshare can also be executed in a shell:

```bash
ezshare <filename>
```

## Contributing
Contributions are welcome! If you have suggestions or improvements, feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
