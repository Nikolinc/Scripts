#!/usr/bin/env python3
import subprocess
import platform
import os

OS_VERSION:str = None
USER:str = "root"
PUBLIC_KEY="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCsj5ihQiIpbXZ+fXSGvl2GsAqozHKowQ3rZnp5LmrRTlkjDp6dmDLUeuQ3sbpZGA990JmgJmLG77I4aznrmYd3z5DLgc2kUxRs5br+mT5S8iz4rR/Yoeykj8HDRz5q0BmCFNtBbBMmCbiMB0C0ccn4aGQkk/tON2QAzLpFJf6J+2AqTOaPYB//83d6A+2R9AfOzfC1yo441qJxTcmDHoFgV+o3+6emnqIWeQOAKBRi5SnkSUOCtALDPbEta5wq/RbawY3eOaE1YLeEEUI2Kwh6TA6BQ2hNM97r8c5+OTRMbsBN2TQDxS8ouqEtIN96/xHffeZwbfK8qsaQMGwEZZC/tYonwINcMr2LuViw/9s2sGu2mC0Fp23LmVkPEGYBGAGkiGTp1XHpRkpzMf1fBvA2QaRJJubkqg3leOjUnGve+pZFKXQHmUNij8ZWksnFT6hoqKiNdFWN4Uhmyb5CkphtOCIxvGrIHucbuXPREiCKwpJ4F3Prfw3C6pUOpcY18q0= tsigu@DESKTOP-5CL5M30"
PORT = 6468

def run(cmd: str):
  print(f"[RUN] {cmd}")
  result =  subprocess.run(cmd.split(" "), shell=True, text=True, capture_output=True)
  return result.stdout.strip()

def detect_system():
  system_name = platform.system()

  if system_name == "Linux":
    if os.path.exists("/etc/os-release"):
            with open("/etc/os-release", "r") as f:
                for line in f:
                    if line.startswith("ID="):
                        os_id = line.strip().split("=")[1].replace('"', "")
                        return os_id
    return "linux-unknown"

  elif system_name == "Darwin":
      return "macos"

  else:
    return "unknown"

def add_ssh_key():
  ssh_dir = f"/{USER}/.ssh" if USER != "root" else "/root/.ssh"
  auth_keys = os.path.join(ssh_dir, "authorized_keys")

  choice = input("Использовать дефолтный ключ? (y/n): ").strip().lower()
  if choice == "y":
    key = PUBLIC_KEY
  else:
    key = input("Введите ваш публичный ключ SSH: ").strip()

  os.makedirs(ssh_dir, mode=0o700, exist_ok=True)

  if os.path.exists(auth_keys):
    with open(auth_keys, "r") as f:
        if key.strip() in f.read():
          print("Ключ уже добавлен")
          return
  with open(auth_keys, "a") as f:
    f.write(key.strip() + "\n")

  os.chmod(auth_keys, 0o600)
  print(f"Ключ добавлен в {auth_keys}")

def configure_ssh():
  sshd_config = "/etc/ssh/sshd_config"

  choice = input("Использовать дефолтный порт 6468? (y/n): ").strip().lower()
  if choice == "y":
    port = PUBLIC_KEY
  else:
    port = input("Введите желаемый порт SSH: ").strip()


  run(f"sed -i 's/^#Port .*/Port {port}/; s/^Port .*/Port {port}/' {sshd_config}")
  run(f"sed -i 's/^#PasswordAuthentication yes/PasswordAuthentication no/; s/^PasswordAuthentication .*/PasswordAuthentication no/' {sshd_config}",)
  run("systemctl restart sshd")

  print(f"SSH настроен на порт {port} и авторизация по паролю отключена.")

def update_upgrade():
  match OS_VERSION:
      case "debian":
        pm = "apt"
      case "ubuntu":
        pm = "apt"
      case "centos":
        pm = "yum"
      case "macos":
        pm = "brew"

  run(f"{pm} update -y && {pm} upgrade -y")

def start_firewall():
  portslist = run("ss -tln | awk '{print $4}' | grep -oE '[0-9]+$'").splitlines()

  run('iptables -P INPUT DROP')
  run('iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT')

  for port in portslist:
    run(f"iptables -A INPUT -p tcp --dport {port} -j ACCEPT")

  print("Firewall настроен: открыты только текущие порты")

if __name__ == "__main__":
  OS_VERSION = detect_system()
  USER = run("whoami")
  update_upgrade()
  add_ssh_key()
  configure_ssh()
  start_firewall()


