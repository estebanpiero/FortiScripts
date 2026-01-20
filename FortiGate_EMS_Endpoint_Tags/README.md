# FortiGate EMS Tags

A Python utility to retrieve FortiClient endpoint information and security posture tags from FortiGate devices via SSH.

## Features

- Connect to FortiGate devices via SSH
- List all FortiClient endpoints managed by EMS
- Retrieve security posture tags for each endpoint
- Export data in JSON and CSV formats
- Support for SSH key-based authentication

## Requirements

- Python 3.6+
- paramiko library

## Installation

```bash
pip install paramiko
```

## Usage

### Basic Usage

```bash
python3 list_ec_tags.py --host <fortigate_ip> --user <username> --password <password>
```

### SSH Key Authentication

```bash
python3 list_ec_tags.py --host <fortigate_ip> --user <username> --keyfile /path/to/private_key
```

### Export Options

```bash
# Export to JSON
python3 list_ec_tags.py --host <fortigate_ip> --user <username> --password <password> --json endpoints.json

# Export to CSV
python3 list_ec_tags.py --host <fortigate_ip> --user <username> --password <password> --csv endpoints.csv
```

## Command Line Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--host` | Yes | FortiGate device IP address or hostname |
| `--user` | Yes | SSH username |
| `--password` | No | SSH password (use with caution) |
| `--keyfile` | No | Path to SSH private key file |
| `--port` | No | SSH port (default: 22) |
| `--json` | No | Output file path for JSON export |
| `--csv` | No | Output file path for CSV export |

## Output Format

The tool displays endpoint information in a tabular format:

```
RECORD IP              HOSTNAME                  UID                              TAGS
--------------------------------------------------------------------------------------------------------
1      192.168.1.100   DESKTOP-ABC123           a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6 Compliant, Updated
2      192.168.1.101   LAPTOP-XYZ789            b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7 Non-Compliant, Outdated
```

## Data Structure

Each endpoint contains:
- **Record**: Sequential record number
- **IP Address**: Endpoint IP address
- **Hostname**: Endpoint hostname
- **EMS Serial**: EMS server serial number
- **Tenant ID**: EMS tenant identifier
- **UID**: FortiClient unique identifier
- **Tags**: Security posture tags

## Security Considerations

- Avoid using `--password` in production; use SSH keys instead
- Ensure SSH access is properly secured on FortiGate devices
- Store credentials securely and never commit them to version control
- Use least-privilege accounts for SSH access

## Troubleshooting

### Connection Issues
- Verify FortiGate SSH access is enabled
- Check firewall rules and network connectivity
- Ensure correct credentials and permissions

### Command Failures
- Verify FortiGate firmware supports EMS commands
- Check if EMS is properly configured
- Ensure sufficient privileges for diagnostic commands

## License

This project is provided as-is for educational and operational purposes.

## Contributing

1. Follow PEP 8 style guidelines
2. Add appropriate error handling
3. Include unit tests for new features
4. Update documentation as needed