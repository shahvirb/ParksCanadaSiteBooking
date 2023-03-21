1 .. 1 | % {
	Start-Process -NoNewWindow powershell.exe -ArgumentList "python .\main.py", "-i 0"
	Start-Process -NoNewWindow powershell.exe -ArgumentList "python .\main.py", "-i 1"
	Start-Process -NoNewWindow powershell.exe -ArgumentList "python .\main.py", "-i 2"
}