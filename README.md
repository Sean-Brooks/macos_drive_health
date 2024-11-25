# macos_drive_health
Drive Health for Apple Silicon

### Description
Checks if Homebrew is installed
  - If Homebrew is not found, an attempt is made to install

Checks if smartctl is installed
- If smartctl is not found, an attempt is made to install it via Homebrew

Attempts to import tabulate
- If the import fails, an attempt to install it via two different pip methods begins

Retrieves and prints the health data

```
Tabulate... ---> Installed!
Homebrew... ---> Installed!
smartmontools... ---> Installed!

mac_mini_m4 | Sun Nov 24 23:09:04 EST 2024
+--------------+----------+
| Attribute    | Health   |
+==============+==========+
| Write Health | 99.53%   |
+--------------+----------+
| Read Health  | 99.55%   |
+--------------+----------+
```
