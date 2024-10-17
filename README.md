# File-Cleanup
<h3>
Combs through multiple files and Directories and seeks Duplicate files to Delete to save on storage space</h3><br>
<br>
<body>
<p>The program combs through all directories in from the start directory to get all files. With all the file paths, each files' contents  are hashed with <code>sha256</code> and compared to each other to compare if the contents are the same. </p>


<p>
The following libraries are required for the program to run:

<code>import os </code><br>
<code>import argparse </code><br>
<code>import time </code><br>
<code>import sys </code><br>
<code>import hashlib </code><br>

</p>

<p>To run this code <code>python main.py [start_Directory] </code></p><br>
<pre>
C:\..\Example\File-Cleanup> python .\main.py -h
usage: main.py [-h] [--quiet] [directory]

Search for duplicate file and folder names.

positional arguments:
  directory   The directory to search in

options:
  -h, --help  show this help message and exit
  --quiet     Suppress detailed output
</pre><br>
<pre>
<h4>Example of this program checking on this Repository</h4>
 Checking for duplicated files 
1 Name: HEAD has duplicate names in the following 1 variation(s):
Hash_id 3fcbfae6f3af7c5f591c3ecc91a80ad64ce7b1e05a07332deaa32ad2c32db7e6
    C:\..\Example\File-Cleanup\.git\logs\HEAD 203.0 B
    C:\..\Example\File-Cleanup\.git\logs\refs\remotes\origin\HEAD 203.0 B

+-----------------------------------+
| Time taken: 0.01 seconds          |
| Total Walks: 17                   |
| Total Files checked: 29           |
| Total Duplicates Found: 2         |
+-----------------------------------+
</pre>

</body>