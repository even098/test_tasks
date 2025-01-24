$ip = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -eq 'Ethernet 2'}).IPAddress
$response = Invoke-WebRequest -Uri "http://$ip/index.html" -Method GET
$localHash = Get-FileHash "$env:USERPROFILE\test.zip" -Algorithm SHA256
$regex = [regex] '<p>([a-fA-F0-9]+)</p>'
if ($regex.Match($response.Content).Success) {
    $webHash = $regex.Match($response.Content).Groups[1].Value
}
if ($webHash -ne $localHash.Hash) {
    Stop-Process -Name "write.exe"
    Remove-Item "$env:USERPROFILE\test.zip"
    Remove-Item "$env:USERPROFILE\write.exe"
    Remove-Item "$env:USERPROFILE\hash.ps1"
    Invoke-WebRequest -Uri "http://$ip/test.zip" -OutFile "$env:USERPROFILE\test.zip"
    Expand-Archive -Path "$env:USERPROFILE\test.zip" -DestinationPath "$env:USERPROFILE\"
}