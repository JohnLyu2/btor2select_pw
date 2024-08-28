This is a repo for HWMCC'24 submission.

## Requirements
I tested with Python 3.11
#### Install Python Packages
```bash
pip install -r requirement.txt
```

#### Compile `kwcount`
```bash
cd btor2kwcount/
./configure.sh
cd build/
make
```

## Usage
```bash
./main.py <btor2 path>
```
The script shall print a tuple (tool, config)