# Scan to Print
[![maintenance-status](https://img.shields.io/badge/maintenance-as--is-yellow.svg?style=for-the-badge)](https://gist.github.com/angelside/364976fbcf7001a5da7e79ad8ed91fec) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=white) ![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white) [![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge&logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciICB2aWV3Qm94PSIwIDAgNDggNDgiIHdpZHRoPSI0OHB4IiBoZWlnaHQ9IjQ4cHgiPjxwYXRoIGZpbGw9IiM0Y2FmNTAiIGQ9Ik0yNCw1QzEzLjUsNSw1LDEzLjYsNSwyNC4xYzAsOC4yLDUuMSwxNS4xLDEyLjMsMTcuOWw0LjItMTEuNUMxOC44LDI5LjUsMTcsMjcsMTcsMjQgYzAtMy45LDMuMS03LDctN3M3LDMuMSw3LDdjMCwzLTEuOCw1LjUtNC41LDYuNUwzMC43LDQyQzM3LjksMzkuMiw0MywzMi4zLDQzLDI0LjFDNDMsMTMuNiwzNC41LDUsMjQsNXoiLz48cGF0aCBmaWxsPSIjMmU3ZDMyIiBkPSJNMTcuOSw0My4zbC0wLjktMC40QzkuMiw0MCw0LDMyLjQsNCwyNC4xQzQsMTMsMTMsNCwyNCw0YzExLDAsMjAsOSwyMCwyMC4xIGMwLDguMy01LjIsMTUuOS0xMi45LDE4LjhsLTAuOSwwLjRsLTQuOC0xMy4zbDAuOS0wLjRjMi4zLTAuOSwzLjgtMy4xLDMuOC01LjZjMC0zLjMtMi43LTYtNi02cy02LDIuNy02LDZjMCwyLjUsMS41LDQuNywzLjgsNS42IGwwLjksMC40TDE3LjksNDMuM3ogTTI0LDZDMTQuMSw2LDYsMTQuMSw2LDI0LjFjMCw3LjEsNC4zLDEzLjcsMTAuNywxNi41bDMuNS05LjZDMTcuNiwyOS43LDE2LDI3LDE2LDI0YzAtNC40LDMuNi04LDgtOCBzOCwzLjYsOCw4YzAsMy0xLjYsNS43LTQuMiw3bDMuNSw5LjZDMzcuNywzNy44LDQyLDMxLjMsNDIsMjQuMUM0MiwxNC4xLDMzLjksNiwyNCw2eiIvPjwvc3ZnPg==)](./LICENSE)

> Python CLI tool that allows to scan-to-print from barcode to zebra label printer.

When you run the application, it will enter an infinite loop and prompt you for an input *(which can correspond to any key in the data.json file)*. Upon entering or scanning the input, the application will send a ZPL code to the designated printer IP using a socket request. It will then display the success or error status *(only network status, if the application can reach the IP address, it will be considered successful, regardless of the printer's status)* of the printing process and will request another input from you.

You can only print one at a time. For batch printing, I use a completely different custom application. If desired, you can modify the application to loop through all data in data.json and apply socket_request() to each IP.

Here's how I am using the application: I have barcodes on each printer/desk, and I am utilizing a Windows tablet with a built-in Zebra barcode scanner (Zebra ET5).

![screenshot](https://github.com/angelside/scan-to-print/assets/7515/864de62e-f4b3-4392-b3df-6c58dd40e696)


## 📦 Installation

Cloning the repo

```bash
git clone https://github.com/angelside/ricoh-supply-cli-py.git scan-to-print
```

```
cd scan-to-print
```

Use the package manager [poetry](https://python-poetry.org/docs/) to install. Run the below command inside the project directory.

```bash
poetry install
```

## ⚙️Configuration

Configuration files

- data.json *(Not in git repo)*
- label.txt *(Current file has a small label)*

 **data.json sample**

"Barcode" : "Printer IP address"

 ```json
 {
    "Desk-1": "192.168.0.2",
    "Desk-2": "192.168.0.3",
    "Desk-3": "192.168.0.4",
}
 ```

 **label.txt samples**

small label
```
^XA
^LT0
^LH0,0
^JMA
~SD15
^FO0,0^GB530,77,55^FS
^CI28
^PA0,1,1,0
^FT15,115^A0N,25,20^FB520,1,13,L^FH\^CI28^FD$location^FS^CI27
^FT355,115^A0N,25,18^FB520,1,13,L^FH\^CI28^FD$time^FS^CI27
^FT0,175^A0N,25,20^FB520,1,10,C^FH\^CI28^FD$message^FS^CI27
^XZ
```
big label

```
^XA
^LT0
^LH0,0
^JMA
~SD15
^CI28
^PA0,1,1,0
^FO1,1^GB810,164,148^FS
^FT4,347^A0N,72,71^FB808,1,18,C^FH\^CI28^FD$location^FS^CI27
^FT4,512^A0N,51,51^FB808,1,13,C^FH\^CI28^FD$message^FS^CI27
^FT120,657^A0N,25,25^FH\^CI28^FD$time^FS^CI27
^XZ
```
- *You can create yor own zpl template code as you wish. Yo can preview zpl templates from [Labelary Online ZPL Viewer](http://labelary.com/viewer.html).*

### **Built in template variables:**

**$location**
This is the "key" in the json file

**$time**
Current time

**$message**
Opps, this is hardcoded in the main.py file *(IT zebra printer quality test)*

## 🔨 Usage

Without build, just run the python file.

```bash
python main.py
```

With build (tested only in Windows)
*You can build a binary file, and use it.*

```bash
pip install -U pyinstaller
pyinstaller --noconfirm --onefile --console --icon "./printer.ico" --name "scan-to-print"  "./main.py"

./scan-to-print.exe
```

### 📋 Sample results

```bash
> py .\main.py
=== Scan to Print ===

Location:
```

## 💥 Features

- Simple label with full black top.
- Report missing config files *(data.json, label.txt)*.
- Achieve correct CLI colors in Windows Command Prompt using the "colorama" package.
- Ctrl+C for exit

## 🎯 Tested Zebra printer models

- ZD 620
- ZD 621
- GK 420d

## 🤝 Contributing

Before contributing issues or pull requests, could you review the [Contributing Guidelines](./.github/CONTRIBUTING.md) first?

## 💬 Questions?

Feel free to [open an issue](https://github.com/angelside/scan-to-print/issues/new).

## 🤩 Support

💙 If you like this project, give it a ⭐ and share it with friends!

## 🏛️ License

This project is open-sourced software licensed under the [MIT license](./LICENSE).
