import sys
import time
import requests

TIMEOUT = 10  # segundos máximos de espera por sitio


def check(url):
    """Revisa una URL. Devuelve (está_bien, detalle)."""
    inicio = time.monotonic()
    try:
        r = requests.get(url, timeout=TIMEOUT)
        ms = int((time.monotonic() - inicio) * 1000)
        return r.ok, f"{r.status_code} en {ms} ms"  # r.ok = código menor a 400
    except requests.RequestException as e:
        return False, type(e).__name__  # DNS, timeout, conexión rechazada...


def main():
    with open("sites.txt") as f:
        urls = [l.strip() for l in f if l.strip() and not l.startswith("#")]

    caidos = 0
    for url in urls:
        ok, detalle = check(url)
        print(f"{'!!! OK    ' if ok else '❌ CAÍDO'} {url} -> {detalle}")
        if not ok:
            caidos += 1

    sys.exit(1 if caidos else 0)  # código de salida: 0 = todo bien, 1 = hubo caídas


if __name__ == "__main__":
    main()