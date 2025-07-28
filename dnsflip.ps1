# dnsflip.ps1
#
# This PowerShell script toggles the DNS server settings for a specified network interface between a Pi-hole DNS server and public DNS servers (Google DNS).
#
# - Checks if the script is run as Administrator.
# - Detects the current DNS configuration for the interface specified by $interfaceAlias.
# - If currently using Pi-hole, prompts to switch to public DNS servers (8.8.8.8, 8.8.4.4).
# - If currently using public DNS, prompts to switch back to Pi-hole (by resetting DNS to DHCP/static config).
# - Prompts the user for confirmation before making changes.
#
# Usage:
#   Run this script as Administrator in PowerShell.
#   Modify $interfaceAlias, $piHoleAddress, and $publicDNS as needed for your environment.

# Check if running as Administrator
if (-not ([Security.Principal.WindowsPrincipal] `
    [Security.Principal.WindowsIdentity]::GetCurrent()
).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "Please run this script as Administrator." -ForegroundColor Red
    exit
}

# Target interface
$interfaceAlias = "Ethernet 2"
$piHoleAddress = "192.168.1.3"
$publicDNS = @("8.8.8.8", "8.8.4.4")

# Get current DNS addresses
$currentDNS = (Get-DnsClientServerAddress -InterfaceAlias $interfaceAlias -AddressFamily IPv4).ServerAddresses

if ($currentDNS -contains $piHoleAddress) {
    $response = Read-Host "The current DNS server is Pi-hole. Do you want to change to public DNS servers? (Y/n)"
    if ($response.ToLower() -eq "y") {
        Set-DnsClientServerAddress -InterfaceAlias $interfaceAlias -ServerAddresses $publicDNS
        Write-Host "DNS changed to public servers: $($publicDNS -join ', ')"
    } else {
        Write-Host "DNS servers are unchanged."
    }
} else {
    $response = Read-Host "Currently set to public DNS servers. Do you want to change to Pi-hole? (Y/n)"
    if ($response.ToLower() -eq "y") {
        Set-DnsClientServerAddress -InterfaceAlias $interfaceAlias -ResetServerAddresses
        Write-Host "DNS reset to Pi-hole (via DHCP or static config)."
    } else {
        Write-Host "DNS servers are unchanged."
    }
}