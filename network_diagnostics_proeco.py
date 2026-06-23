import flet as ft
import socket
import subprocess
import platform
import threading
from datetime import datetime
import os


def main(page: ft.Page):
    page.title = "Network Diagnostics Tool"
    page.window_width = 500
    page.window_height = 850
    
    # ============ CONFIGURAZIONE PROECO ============
    PROECO_SERVERS = {
        "srv2k19": "192.168.0.14",      # IT Server Proeco
        "srv2022 (DC)": "192.168.0.2",  # Domain Controller
    }
    
    VPN_GATEWAY = "192.168.113.1"  # OpenVPN Gateway (TAP Adapter)
    GRAFANA_URL = "192.168.200.100:3000"  # Monitoring stack (Proxmox)
    
    # ============ FUNZIONI DI UTILITÀ ============
    
    def log_output(message: str):
        """Aggiunge un messaggio al log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        output_log.value += f"[{timestamp}] {message}\n"
        output_log.update()
    
    def clear_log_click(e):
        """Pulisce il log"""
        output_log.value = ""
        output_log.update()
    
    def export_report(e):
        """Esporta il report in file .txt"""
        if not output_log.value:
            log_output("❌ Nessun log da esportare")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"proeco_diagnostics_{timestamp}.txt"
        filepath = os.path.join(os.path.expanduser("~"), "Desktop", filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("PROECO NETWORK DIAGNOSTICS REPORT\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 60 + "\n\n")
                f.write(output_log.value)
            
            log_output(f"✅ Report salvato: {filepath}")
        except Exception as ex:
            log_output(f"❌ Errore nel salvataggio: {str(ex)}")
    
    # ============ FUNZIONI NETWORK GENERICHE ============
    
    def run_ping(e):
        """Esegue ping"""
        host = input_host.value.strip()
        if not host:
            log_output("❌ Inserisci un hostname o IP")
            return
        
        count_val = int(ping_count.value)
        
        def ping_worker():
            log_output(f"🔄 Ping in corso verso {host} ({count_val} pacchetti)...")
            try:
                param = "-n" if platform.system().lower() == "windows" else "-c"
                result = subprocess.run(
                    ["ping", param, str(count_val), host],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    log_output("✅ Host raggiungibile")
                    lines = result.stdout.split('\n')
                    for line in lines[-5:]:
                        if line.strip():
                            log_output(line.strip())
                else:
                    log_output("❌ Host non raggiungibile")
            except Exception as ex:
                log_output(f"❌ Errore: {str(ex)}")
        
        thread = threading.Thread(target=ping_worker, daemon=True)
        thread.start()
    
    def run_dns(e):
        """Esegue DNS lookup"""
        host = input_host.value.strip()
        if not host:
            log_output("❌ Inserisci un hostname o IP")
            return
        
        def dns_worker():
            log_output(f"🔄 DNS Lookup per {host}...")
            try:
                ip = socket.gethostbyname(host)
                log_output(f"✅ {host} -> {ip}")
                
                try:
                    hostname, aliaslist, ipaddrlist = socket.gethostbyaddr(ip)
                    log_output(f"   Reverse DNS: {hostname}")
                except:
                    log_output(f"   Reverse DNS: Non disponibile")
            except socket.gaierror:
                log_output(f"❌ Impossibile risolvere {host}")
            except Exception as ex:
                log_output(f"❌ Errore: {str(ex)}")
        
        thread = threading.Thread(target=dns_worker, daemon=True)
        thread.start()
    
    def run_tracert(e):
        """Esegue tracert"""
        host = input_host.value.strip()
        if not host:
            log_output("❌ Inserisci un hostname o IP")
            return
        
        def tracert_worker():
            log_output(f"🔄 Tracert verso {host}...")
            try:
                cmd = "tracert" if platform.system().lower() == "windows" else "traceroute"
                result = subprocess.run(
                    [cmd, host],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                if result.returncode == 0:
                    log_output("✅ Tracert completato:")
                    for line in result.stdout.split('\n')[:15]:
                        if line.strip():
                            log_output(line.strip())
                else:
                    log_output("❌ Tracert fallito")
            except Exception as ex:
                log_output(f"❌ Errore: {str(ex)}")
        
        thread = threading.Thread(target=tracert_worker, daemon=True)
        thread.start()
    
    def run_port_scan(e):
        """Scansiona porte"""
        host = input_host.value.strip()
        ports_str = port_input.value.strip()
        
        if not host or not ports_str:
            log_output("❌ Inserisci host e porte (es: 80,443,3389)")
            return
        
        def port_worker():
            log_output(f"🔄 Scansione porte su {host}...")
            try:
                port_list = [int(p.strip()) for p in ports_str.split(',')]
                
                for port in port_list:
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(2)
                        result = sock.connect_ex((host, port))
                        
                        if result == 0:
                            log_output(f"✅ Porta {port}: APERTA")
                        else:
                            log_output(f"❌ Porta {port}: CHIUSA")
                        
                        sock.close()
                    except:
                        log_output(f"⚠️  Porta {port}: Errore")
                
                log_output("✅ Scansione completata")
            except Exception as ex:
                log_output(f"❌ Errore: {str(ex)}")
        
        thread = threading.Thread(target=port_worker, daemon=True)
        thread.start()
    
    # ============ PROECO-SPECIFIC FUNCTIONS ============
    
    def check_proeco_servers(e):
        """Controlla health dei server Proeco"""
        def servers_worker():
            log_output("\n" + "="*50)
            log_output("🔍 PROECO SERVER HEALTH CHECK")
            log_output("="*50)
            
            for server_name, server_ip in PROECO_SERVERS.items():
                log_output(f"\n📌 Checking {server_name} ({server_ip})...")
                
                try:
                    param = "-n" if platform.system().lower() == "windows" else "-c"
                    result = subprocess.run(
                        ["ping", param, "1", server_ip],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    
                    if result.returncode == 0:
                        log_output(f"   ✅ {server_name}: ONLINE")
                        # Check RDP port (3389)
                        try:
                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            sock.settimeout(2)
                            rdp_result = sock.connect_ex((server_ip, 3389))
                            sock.close()
                            
                            if rdp_result == 0:
                                log_output(f"   ✅ RDP (3389): ACCESSIBLE")
                            else:
                                log_output(f"   ⚠️  RDP (3389): Not accessible")
                        except:
                            pass
                    else:
                        log_output(f"   ❌ {server_name}: OFFLINE")
                
                except Exception as ex:
                    log_output(f"   ❌ Error: {str(ex)}")
            
            log_output("\n" + "="*50)
        
        thread = threading.Thread(target=servers_worker, daemon=True)
        thread.start()
    
    def check_vpn_status(e):
        """Controlla stato OpenVPN"""
        def vpn_worker():
            log_output("\n" + "="*50)
            log_output("🔐 OPENVPN STATUS CHECK")
            log_output("="*50)
            
            log_output(f"\n📌 Checking VPN Gateway: {VPN_GATEWAY}")
            
            try:
                param = "-n" if platform.system().lower() == "windows" else "-c"
                result = subprocess.run(
                    ["ping", param, "1", VPN_GATEWAY],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0:
                    log_output(f"✅ VPN Gateway: REACHABLE")
                    
                    # Check VPN port (1194 UDP)
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        sock.settimeout(2)
                        sock.sendto(b"test", (VPN_GATEWAY, 1194))
                        log_output(f"✅ VPN Port (1194/UDP): RESPONSIVE")
                    except:
                        log_output(f"⚠️  VPN Port (1194/UDP): Not responding (normal for UDP)")
                else:
                    log_output(f"❌ VPN Gateway: UNREACHABLE")
            
            except Exception as ex:
                log_output(f"❌ Error: {str(ex)}")
            
            log_output("\n" + "="*50)
        
        thread = threading.Thread(target=vpn_worker, daemon=True)
        thread.start()
    
    def open_grafana(e):
        """Apre Grafana in browser"""
        log_output(f"\n📊 Grafana URL: http://{GRAFANA_URL}")
        log_output("Apri il link nel tuo browser per accedere al monitoring")
        
        import webbrowser
        webbrowser.open(f"http://{GRAFANA_URL}")
    
    # ============ UI COMPONENTS ============
    
    # Titolo principale
    title = ft.Text("🔧 Network Diagnostics Tool", size=24, weight="bold")
    subtitle = ft.Text("Proeco IT Infrastructure", size=12, color="grey")
    
    # Input host
    input_host = ft.TextField(
        label="Hostname o IP",
        hint_text="Es: 8.8.8.8 o google.com",
        width=450,
    )
    
    # ===== STANDARD TOOLS TAB =====
    ping_count = ft.Dropdown(
        label="Numero ping",
        width=150,
        options=[
            ft.dropdown.Option("1"),
            ft.dropdown.Option("4"),
            ft.dropdown.Option("10"),
        ],
        value="4"
    )
    ping_btn = ft.Button("Ping", on_click=run_ping, width=150)
    
    dns_btn = ft.Button("DNS Lookup", on_click=run_dns, width=150)
    tracert_btn = ft.Button("Tracert", on_click=run_tracert, width=150)
    
    port_input = ft.TextField(
        label="Porte (es: 80,443,3389)",
        hint_text="Separate da virgola",
        width=450
    )
    port_btn = ft.Button("Scansiona Porte", on_click=run_port_scan, width=150)
    
    standard_tools = ft.Container(
        content=ft.Column([
            ft.Text("🌐 Standard Network Tools:", weight="bold", size=12),
            ft.Row([ping_count, ping_btn]),
            ft.Row([dns_btn, tracert_btn]),
            port_input,
            port_btn,
        ]),
        padding=10,
    )
    
    # ===== PROECO TOOLS TAB =====
    proeco_health_btn = ft.Button(
        "🖥️  Proeco Servers Health",
        on_click=check_proeco_servers,
        width=450,
        bgcolor="#1f77d2",
        color="white"
    )
    
    vpn_status_btn = ft.Button(
        "🔐 OpenVPN Status",
        on_click=check_vpn_status,
        width=450,
        bgcolor="#2ecc71",
        color="white"
    )
    
    grafana_btn = ft.Button(
        "📊 Open Grafana Monitoring",
        on_click=open_grafana,
        width=450,
        bgcolor="#ff9f43",
        color="white"
    )
    
    proeco_tools = ft.Container(
        content=ft.Column([
            ft.Text("⚡ Proeco Infrastructure Tools:", weight="bold", size=12),
            proeco_health_btn,
            vpn_status_btn,
            grafana_btn,
        ]),
        padding=10,
    )
    
    # Output Log
    output_log = ft.TextField(
        multiline=True,
        min_lines=14,
        read_only=True,
        width=450,
    )
    
    # Control buttons
    clear_btn = ft.Button("🗑️  Pulisci Log", on_click=clear_log_click, width=150)
    export_btn = ft.Button("💾 Esporta Report", on_click=export_report, width=150)
    
    # ============ LAYOUT PRINCIPALE ============
    
    main_column = ft.Column(
        controls=[
            ft.Container(padding=10),
            title,
            subtitle,
            ft.Divider(),
            input_host,
            ft.Divider(),
            standard_tools,
            ft.Divider(),
            proeco_tools,
            ft.Divider(),
            ft.Text("📋 Output Log:", weight="bold", size=12),
            output_log,
            ft.Row([clear_btn, export_btn], spacing=10),
        ],
        scroll=ft.ScrollMode.AUTO,
        spacing=5,
    )
    
    page.add(ft.Container(
        content=main_column,
        padding=15
    ))


if __name__ == "__main__":
    ft.run(main)
