import sys
from datetime import datetime, timedelta
from ceu import posicoes, fase_da_lua, SP
from grafico import desenhar


def checar(nome, dt, signo_esperado):
    sol = posicoes(dt)["Sol"]
    ok = sol["signo"] == signo_esperado and sol["grau"] < 2
    print(f"{'OK  ' if ok else 'ERRO'} {nome}: Sol a {sol['grau']}° de {sol['signo']}")
    return ok


print("--- Testes de referência ---")
checar("Dia após o equinócio de março de 2026", datetime(2026, 3, 21, 12, tzinfo=SP), "Áries")
checar("Dia após o solstício de junho de 2026", datetime(2026, 6, 22, 12, tzinfo=SP), "Câncer")

print("\n--- Fases da Lua nos próximos 30 dias ---")
hoje = datetime.now(SP)
for i in range(0, 30, 3):
    d = hoje + timedelta(days=i)
    print(f"{d:%d/%m}  {fase_da_lua(d)}")

# Gráfico de uma data escolhida: python src\testar.py 2026-12-24
if len(sys.argv) > 1:
    d = datetime.strptime(sys.argv[1], "%Y-%m-%d").replace(hour=12, tzinfo=SP)
    desenhar(d, "output/grafico_teste.png")
    print(f"\nGráfico gerado para {d:%d/%m/%Y}: output/grafico_teste.png")