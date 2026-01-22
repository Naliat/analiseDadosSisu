import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns
import pyarrow

print("--- Iniciando Processamento Paralelo (12 Threads i5) ---")


df = pl.read_csv(
    'lista_de_espera_sisu_2023_2.csv',
    separator='|',
    encoding='latin-1',
    ignore_errors=True,
    infer_schema_length=10000
)
df = df.with_columns([
    pl.col("NOTA_CANDIDATO").str.replace(",", ".").cast(pl.Float64, strict=False),
    pl.col("NOTA_CORTE").str.replace(",", ".").cast(pl.Float64, strict=False)
]).with_columns([
    (pl.col("NOTA_CANDIDATO") - pl.col("NOTA_CORTE")).alias("DIFERENCA_CORTE")
]).filter(pl.col("NOTA_CANDIDATO").is_not_null())

sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
print("Gerando Gráfico 1...")
regioes = df.group_by("UF_CANDIDATO").count().sort("count", descending=True).to_pandas()
sns.barplot(data=regioes, y="UF_CANDIDATO", x="count", palette="viridis")
plt.title("Concentração por Estado")
plt.savefig("1_regioes.png")
print("Gerando Gráfico 2...")
notas_array = df["NOTA_CANDIDATO"].to_numpy()
plt.figure()
sns.histplot(notas_array, bins=50, color="teal")
plt.title("Distribuição de Notas")
plt.savefig("2_notas.png")
print("Gerando Gráfico 3...")
distancia_array = df["DIFERENCA_CORTE"].to_numpy()
plt.figure()
sns.boxplot(x=distancia_array, color="salmon")
plt.title("Diferença para Nota de Corte")
plt.savefig("3_distancia.png")
print("Gerando Gráfico 4...")
turnos = df.group_by("TURNO").count().to_pandas()
plt.figure()
plt.pie(turnos["count"], labels=turnos["TURNO"], autopct='%1.1f%%', colors=sns.color_palette("pastel"))
plt.title("Distribuição por Turno")
plt.savefig("4_turnos.png")

print("🚀 Gráficos gerados com sucesso usando 100% da CPU!")