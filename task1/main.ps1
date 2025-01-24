$ip = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -eq 'Ethernet 2'}).IPAddress
Invoke-WebRequest -Uri "http://$ip/test.zip" -OutFile "$env:USERPROFILE\test.zip"
Expand-Archive -Path "$env:USERPROFILE\test.zip" -DestinationPath "$env:USERPROFILE\"
$Action = New-ScheduledTaskAction -Execute "$env:USERPROFILE\write.exe; $env:USERPROFILE\hash.ps1"
$Trigger = New-ScheduledTaskTrigger -At 12:00 -Daily
Register-ScheduledTask -Action $Action -Trigger $Trigger -TaskName "TimeToWrite"
