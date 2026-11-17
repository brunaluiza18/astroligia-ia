import math
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from ceu import posicoes, fase_da_lua, SP

# ---------- PALETA (troque à vontade) ----------
FUNDO = "#0B1026"
OURO = "#E8B84A"
TEXTO = "#F5E9D0"
ELEMENTOS = {
    "fogo": "#FF7A3D", "terra": "#7FBF7A", "ar": "#F2D16B", "agua": "#5BB4FF",
}
ORDEM_ELEMENTOS = ["fogo", "terra", "ar", "agua"] * 3

SIMBOLOS_SIGNO = ["♈", "♉", "♊", "♋", "♌", "♍", "♎", "♏", "♐", "♑", "♒", "♓"]
SIMBOLOS_PLANETA = {
    "Sol": "☉", "Lua": "☽", "Mercúrio": "☿", "Vênus": "♀", "Marte": "♂",
    "Júpiter": "♃", "Saturno": "♄", "Urano": "♅", "Netuno": "♆", "Plutão": "♇",
}


def xy(lon, r):
    """Áries (0°) fica na esquerda e os signos giram no sentido anti-horário."""
    ang = math.radians(180 + lon)
    return r * math.cos(ang), r * math.sin(ang)


def espalhar(lons, minimo=10, voltas=300):
    """Afasta os rótulos de planetas que estão muito juntos."""
    pos = list(lons)
    for _ in range(voltas):
        mexeu = False
        for i in range(len(pos)):
            for j in range(i + 1, len(pos)):
                d = (pos[j] - pos[i] + 180) % 360 - 180
                if abs(d) < minimo:
                    empurra = (minimo - abs(d)) / 2 + 0.01
                    sinal = 1 if d >= 0 else -1
                    pos[i] -= sinal * empurra
                    pos[j] += sinal * empurra
                    mexeu = True
        if not mexeu:
            break
    return [p % 360 for p in pos]


def desenhar(dt, caminho):
    pos = posicoes(dt)
    fig = plt.figure(figsize=(10.8, 10.8), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(-1.03, 1.03)
    ax.set_ylim(-1.03, 1.03)
    ax.set_aspect("equal")
    ax.axis("off")

    # círculos
    ax.add_patch(Circle((0, 0), 1.0, facecolor=FUNDO, edgecolor=OURO, lw=3))
    ax.add_patch(Circle((0, 0), 0.82, fill=False, edgecolor=OURO, lw=1.5))
    ax.add_patch(Circle((0, 0), 0.46, fill=False, edgecolor=OURO, lw=1.5))

    # signos
    for i in range(12):
        x1, y1 = xy(i * 30, 0.82)
        x2, y2 = xy(i * 30, 1.0)
        ax.plot([x1, x2], [y1, y2], color=OURO, lw=1.2)
        x, y = xy(i * 30 + 15, 0.91)
        ax.text(x, y, SIMBOLOS_SIGNO[i], color=ELEMENTOS[ORDEM_ELEMENTOS[i]],
                fontsize=30, ha="center", va="center")

    # planetas
    nomes = list(pos.keys())
    reais = [pos[n]["longitude"] for n in nomes]
    exibidos = espalhar(reais)

    for nome, lon, lon_rotulo in zip(nomes, reais, exibidos):
        xa, ya = xy(lon, 0.46)
        xb, yb = xy(lon_rotulo, 0.60)
        ax.plot([xa, xb], [ya, yb], color=OURO, lw=0.8, alpha=0.7)
        ax.plot(xa, ya, "o", color=OURO, ms=5)

        x, y = xy(lon_rotulo, 0.66)
        ax.text(x, y, SIMBOLOS_PLANETA[nome], color=TEXTO,
                fontsize=26, ha="center", va="center")

        if pos[nome]["retrogrado"]:
            xr, yr = xy(lon_rotulo, 0.745)
            ax.text(xr, yr, "R", color=OURO, fontsize=13,
                    fontweight="bold", ha="center", va="center")

    # centro
    ax.text(0, 0.06, fase_da_lua(dt), color=TEXTO, fontsize=20, ha="center", va="center")
    ax.text(0, -0.06, f"{dt:%d/%m/%Y}", color=OURO, fontsize=16, ha="center", va="center")

    fig.savefig(caminho, transparent=True)
    plt.close(fig)


if __name__ == "__main__":
    agora = datetime.now(SP)
    desenhar(agora, "output/grafico_hoje.png")
    print("Pronto: output/grafico_hoje.png")