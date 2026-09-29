#!/data/data/com.termux/files/usr/bin/python
import os
import socket
import subprocess
import time
from zeroconf import Zeroconf, ServiceInfo

SERVICE_NAME = os.environ.get("JELLYMEDIA_SERVICE_NAME", "Jellyfin")
SERVICE_TYPE = "_http._tcp.local."
PORT = int(os.environ.get("JELLYMEDIA_PORT", "8096"))


def get_lan_ip():
    """Get the current IPv4 address used for the LAN/Wi-Fi route."""
    try:
        out = subprocess.check_output(
            ["ip", "-4", "addr", "show", "wlan0"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
        for line in out.splitlines():
            line = line.strip()
            if line.startswith("inet "):
                return line.split()[1].split("/")[0]
    except Exception:
        pass

    # Fallback: determine the source address for a LAN route.
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("192.168.0.1", 1))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return None


def advertise(ip):
    service_name = f"{SERVICE_NAME}.{SERVICE_TYPE}"
    server_name = "jellyfin.local."

    info = ServiceInfo(
        SERVICE_TYPE,
        service_name,
        addresses=[socket.inet_aton(ip)],
        port=PORT,
        properties={
            b"path": b"/",
            b"name": SERVICE_NAME.encode(),
        },
        server=server_name,
    )

    zc = Zeroconf()
    zc.register_service(info)
    return zc, info


def main():
    print("JellyMedia mDNS advertiser starting...", flush=True)

    zc = None
    info = None
    last_ip = None

    try:
        while True:
            ip = get_lan_ip()

            if ip != last_ip:
                if zc is not None and info is not None:
                    try:
                        zc.unregister_service(info)
                    except Exception:
                        pass
                    zc.close()
                    zc = None
                    info = None

                if ip:
                    zc, info = advertise(ip)
                    last_ip = ip
                    print(
                        f"✅ http://jellyfin.local:{PORT} → {ip}:{PORT}",
                        flush=True,
                    )
                else:
                    last_ip = None
                    print("📵 No Wi-Fi/LAN IPv4 address; waiting...", flush=True)

            time.sleep(10)

    except KeyboardInterrupt:
        pass
    finally:
        if zc is not None and info is not None:
            try:
                zc.unregister_service(info)
            except Exception:
                pass
            zc.close()


if __name__ == "__main__":
    main()
