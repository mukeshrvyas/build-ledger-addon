# Build Ledger Add-on for Home Assistant

End-to-end encrypted cost tracker for art/woodwork builds. Installs via **Settings → Add-ons** in Home Assistant OS.

## Installation

1. Add this repository to Home Assistant:
   - Go to **Settings → Add-ons → Add-on Store**
   - Click the **three dots (⋮)** → **Repositories**
   - Paste: `https://github.com/YOUR_USERNAME/build-ledger-addon`
   - Click **Add**
2. Install **Build Ledger** from the add-on list
3. Configure the **Server URL** in the add-on settings (your Cloudflare domain, e.g. `https://build-ledger.yourdomain.com`)
4. Click **Start**

## Configuration

| Option | Description |
|--------|-------------|
| Server URL | Your Cloudflare domain/subdomain, e.g. `https://build-ledger.yourdomain.com` |
| App Name | Display name, default: Build Ledger |
| APK Enabled | Enable APK download link |
| APK Path | Path to APK file inside the add-on, default: `/app/www/apk/build-ledger.apk` |

## Uninstall (Clean Removal)

1. Go to **Settings → Add-ons → Build Ledger**
2. Click **Uninstall**
3. When prompted, confirm deletion of all associated data:
   - App code
   - Encrypted vaults (`/config/build_ledger/data/`)
   - Documents and photos (`/config/build_ledger/docs/`)
   - Add-on configuration
4. Everything is removed cleanly. No traces remain.

## Mobile App (APK)

If you place `build-ledger.apk` in the `www/apk/` folder of this repository, users can download it from:
https://your-domain.com/apk/build-ledger.apk


## Requirements

- Home Assistant OS
- Custom add-on repository access
- Cloudflare domain/subdomain pointing to your Home Assistant IP (or Cloudflare Tunnel)

## License

MIT