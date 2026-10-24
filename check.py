import os
import sys
import time
import requests

TIMEOUT = 10
# Los secretos se leen de variables de entorno, NUNCA se escriben en el código
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")


def check(url):
    inicio = time.monotonic()
    try:
        r = requests.get(url, timeout=TIMEOUT)
        ms = int((time.monotonic() - inicio) * 1000)
        return r.ok, f"{r.status_code} en {ms} ms"
    except requests.RequestException as e:
        return False, type(e).__name__


def alertar(mensaje):
    """Envía un mensaje a Telegram. Si no hay credenciales, avisa y sigue."""
    if not TOKEN or not CHAT_ID:
        print("⚠️  Telegram no configurado, omito la alerta")
        return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": mensaje}, timeout=TIMEOUT)


def main():
    with open("sites.txt") as f:
        urls = [l.strip() for l in f if l.strip() and not l.startswith("#")]

    caidos = []
    for url in urls:
        ok, detalle = check(url)
        print(f"{'✅ OK    ' if ok else '❌ CAÍDO'} {url} -> {detalle}")
        if not ok:
            caidos.append(f"• {url} ({detalle})")

    if caidos:
        alertar("🚨 Vigía detectó caídas:\n" + "\n".join(caidos))

    sys.exit(1 if caidos else 0)


if __name__ == "__main__":
    main()