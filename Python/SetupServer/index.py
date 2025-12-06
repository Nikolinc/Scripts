#!/usr/bin/env python3
import subprocess, os

USER = subprocess.getoutput("whoami")
SSH_PORT = 6468
PUBLIC_KEY = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCsj5ihQiIpbXZ+fXSGvl2GsAqozHKowQ3rZnp5LmrRTlkjDp6dmDLUeuQ3sbpZGA990JmgJmLG77I4aznrmYd3z5DLgc2kUxRs5br+mT5S8iz4rR/Yoeykj8HDRz5q0BmCFNtBbBMmCbiMB0C0ccn4aGQkk/tON2QAzLpFJf6J+2AqTOaPYB//83d6A+2R9AfOzfC1yo441qJxTcmDHoFgV+o3+6emnqIWeQOAKBRi5SnkSUOCtALDPbEta5wq/RbawY3eOaE1YLeEEUI2Kwh6TA6BQ2hNM97r8c5+OTRMbsBN2TQDxS8ouqEtIN96/xHffeZwbfK8qsaQMGwEZZC/tYonwINcMr2LuViw/9s2sGu2mC0Fp23LmVkPEGYBGAGkiGTp1XHpRkpzMf1fBvA2QaRJJubkqg3leOjUnGve+pZFKXQHmUNij8ZWksnFT6hoqKiNdFWN4Uhmyb5CkphtOCIxvGrIHucbuXPREiCKwpJ4F3Prfw3C6pUOpcY18q0= tsigu@DESKTOP-5CL5M30"

def run(cmd):
    print(f"[RUN] {cmd}");
    return subprocess.run(cmd, shell=True, text=True, capture_output=True).stdout.strip()

# Обновление
run("apt update -y && apt upgrade -y")

# Добавление ключа SSH
ssh_dir = f"/{USER}/.ssh" if USER != "root" else "/root/.ssh"
os.makedirs(ssh_dir, mode=0o700, exist_ok=True)
auth_keys = os.path.join(ssh_dir, "authorized_keys")
if not os.path.exists(auth_keys) or PUBLIC_KEY not in open(auth_keys).read():
    with open(auth_keys, "a") as f: f.write(PUBLIC_KEY+"\n")
    os.chmod(auth_keys, 0o600)
    print(f"Ключ добавлен в {auth_keys}")

# Настройка SSH
sshd_config="/etc/ssh/sshd_config"
run(f"sed -i 's/^#Port .*/Port {SSH_PORT}/; s/^Port .*/Port {SSH_PORT}/' {sshd_config}")
run(f"sed -i 's/^#PasswordAuthentication yes/PasswordAuthentication no/; s/^PasswordAuthentication .*/PasswordAuthentication no/' {sshd_config}")
run("systemctl restart sshd")
print(f"SSH настроен на порт {SSH_PORT} и авторизация по паролю отключена.")

# Firewall
run(f"iptables -P INPUT DROP")
run(f"iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT")
run(f"iptables -A INPUT -p tcp --dport {SSH_PORT} -j ACCEPT")
print(f"Firewall настроен: открыт только SSH порт {SSH_PORT}")