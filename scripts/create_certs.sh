#!/bin/bash

# Add the following line to your /etc/hosts file:
echo "127.0.0.1 app.benny.com" | sudo tee -a /etc/hosts
echo "added app.benny.com to /etc/hosts"

set -euo pipefail

if (( $EUID != 0 )); then
    echo >&2 'Error: This script expects to be run with sudo privileges.'
    exit 1
fi

if ! hash mkcert 2>/dev/null; then
    echo >&2 'Error: mkcert command not found.'
    echo >&2 'You need to install mkcert locally first.'
    echo >&2 'For example, on macOS, you can use: brew install mkcert'
    exit 1
fi

MKCERT_DIR=$(mkcert -CAROOT)

if [[ -z "$MKCERT_DIR" || ! -r "$MKCERT_DIR/rootCA.pem" ]]; then
    mkcert -install
fi

# Ensure nginx directory exists or create it
mkdir -p nginx/

mkcert \
    -cert-file nginx/local.crt \
    -key-file nginx/local.key \
    app.benny.com

# Update certificate and key ownership
chown $SUDO_USER nginx/local.crt nginx/local.key

echo "Certificates created successfully!"
