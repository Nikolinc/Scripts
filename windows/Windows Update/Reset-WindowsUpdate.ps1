# Включение служб Windows Update
Set-Service wuauserv -StartupType Automatic -ErrorAction SilentlyContinue
Set-Service bits -StartupType Automatic -ErrorAction SilentlyContinue
Set-Service cryptsvc -StartupType Automatic -ErrorAction SilentlyContinue
Set-Service trustedinstaller -StartupType Automatic -ErrorAction SilentlyContinue

Start-Service wuauserv -ErrorAction SilentlyContinue
Start-Service bits -ErrorAction SilentlyContinue
Start-Service cryptsvc -ErrorAction SilentlyContinue
Start-Service trustedinstaller -ErrorAction SilentlyContinue

# Сброс политик Windows Update
Remove-Item -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU" -Recurse -Force -ErrorAction SilentlyContinue

# Сброс параметров в реестре, которые отключают обновления
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\WindowsUpdate\UX\Settings" -Name "FlightSettingsMaxBuildAgeInDays" -Value 0 -ErrorAction SilentlyContinue

# Очистка папок обновлений
Stop-Service wuauserv -Force -ErrorAction SilentlyContinue
Stop-Service bits -Force -ErrorAction SilentlyContinue

Remove-Item "C:\Windows\SoftwareDistribution" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "C:\Windows\System32\catroot2" -Recurse -Force -ErrorAction SilentlyContinue

# Перезапуск служб после очистки
Start-Service wuauserv -ErrorAction SilentlyContinue
Start-Service bits -ErrorAction SilentlyContinue

# Восстановление системных компонентов
DISM /Online /Cleanup-Image /RestoreHealth
sfc /scannow

Write-Host "Все ограничения сняты. Перезагрузите компьютер." -ForegroundColor Green