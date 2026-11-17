from datetime import datetime, timedelta, timezone
from skyfield.api import Loader
from skyfield import almanac

SP = timezone(timedelta(hours=-3))  # horário de Brasília

loader = Loader("data")  # baixa as efemérides (~17 MB) na 1ª vez
ts = loader.timescale()
eph = loader("de421.bsp")

SIGNOS = ["Áries", "Touro", "Gêmeos", "Câncer", "Leão", "Virgem",
          "Libra", "Escorpião", "Sagitário", "Capricórnio", "Aquário", "Peixes"]

CORPOS = {
    "Sol": "sun", "Lua": "moon", "Mercúrio": "mercury", "Vênus": "venus",
    "Marte": "mars barycenter", "Júpiter": "jupiter barycenter",
    "Saturno": "saturn barycenter", "Urano": "uranus barycenter",
    "Netuno": "neptune barycenter", "Plutão": "pluto barycenter",
}

FASES = ["Lua Nova", "Lua Crescente", "Quarto Crescente", "Gibosa Crescente",
         "Lua Cheia", "Gibosa Minguante", "Quarto Minguante", "Lua Minguante"]


def longitude(corpo, t):
    _, lon, _ = eph["earth"].at(t).observe(eph[corpo]).apparent().ecliptic_latlon(epoch="date")
    return lon.degrees


def posicoes(dt):
    t1 = ts.from_datetime(dt)
    t2 = ts.from_datetime(dt + timedelta(days=1))
    resultado = {}
    for nome, corpo in CORPOS.items():
        lon1, lon2 = longitude(corpo, t1), longitude(corpo, t2)
        movimento = (lon2 - lon1 + 180) % 360 - 180
        resultado[nome] = {
            "longitude": lon1,
            "signo": SIGNOS[int(lon1 // 30)],
            "grau": round(lon1 % 30, 2),
            "retrogrado": movimento < 0,
        }
    return resultado


def fase_da_lua(dt):
    angulo = almanac.moon_phase(eph, ts.from_datetime(dt)).degrees
    return FASES[int(((angulo + 22.5) % 360) // 45)]


if __name__ == "__main__":
    agora = datetime.now(SP)
    print(f"Céu de {agora:%d/%m/%Y %H:%M} (Brasília)\n")
    for planeta, info in posicoes(agora).items():
        retro = " (retrógrado)" if info["retrogrado"] else ""
        print(f"{planeta:10} {info['grau']:5}° {info['signo']}{retro}")
    print(f"\nFase da Lua: {fase_da_lua(agora)}")