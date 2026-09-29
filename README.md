# JellyMedia Server Toolkit

A small, reusable Termux project for a self-hosted Jellyfin server on Android.

It provides:

- `jellymedia organize` — organize new media downloaded directly into `JellyMedia/`
- `jellymedia mdns` — advertise the Jellyfin server as `jellyfin.local`
- `jellymedia status` — show JellyMedia paths and current LAN IP
- a `termux-services` service so mDNS starts automatically in the background

## Requirements

- Android + Termux
- Jellyfin Server already installed and running
- `termux-services`
- Python 3
- Python package `zeroconf`
- A Wi-Fi/LAN network
- A DHCP reservation for the phone is recommended

This project does **not** expose Jellyfin to the internet.

## Expected layout

```text
/storage/emulated/0/JellyMedia/
├── Movies/
├── TV Shows/
├── Anime/
├── Anime Movies/
├── Documentaries/
├── Kids/
├── Concerts/
└── Other/
```

Put newly downloaded video files directly in the `JellyMedia` root. Then run:

```bash
jellymedia organize
```

The organizer only processes video files in the root of `JellyMedia`; it does not recursively rearrange files already inside library folders.

Examples:

```text
The.Boys.S05E06.1080p.WEB-DL.mkv
→ TV Shows/The Boys/Season 05/The Boys S05E06.mkv

Movie.Name.2026.1080p.WEBRip.x265.mkv
→ Movies/Movie Name (2026)/Movie Name (2026).mkv
```

Existing destination files are never overwritten.

## mDNS

The mDNS service advertises:

```text
http://jellyfin.local:8096
```

The service automatically detects the phone's current Wi-Fi IPv4 address instead of hard-coding it.

If Wi-Fi is turned off, devices on the home LAN cannot reach Jellyfin anyway. When Wi-Fi returns, the service re-advertises the current address.

## Install

From the extracted project directory:

```bash
bash install.sh
```

Then:

```bash
jellymedia status
jellymedia organize
```

Enable the mDNS service:

```bash
sv up jellymedia-mdns
sv status jellymedia-mdns
```

To stop it:

```bash
sv-disable jellymedia-mdns
```

To view logs:

```bash
tail -f $PREFIX/var/log/sv/jellymedia-mdns/current
```

## GitHub

Create a new GitHub repository, then:

```bash
git init
git add .
git commit -m "Initial JellyMedia Termux toolkit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/jellymedia-termux.git
git push -u origin main
```

Do not commit personal media files, credentials, or private network information.
