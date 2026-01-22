import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns

df = pl.read_csv('lista_de_espera_sisu_2023_2.csv', separator='|', encoding='latin-1', ignore_errors=True)


df = df.with_columns([
    pl.col("TURNO").str.strip_chars().str.to_uppercase(), 
    pl.col("NOTA_CANDIDATO").str.replace(",", ".").cast(pl.Float64, strict=False)
]).filter(
    pl.col("NOTA_CANDIDATO").is_not_null() & 
    pl.col("TURNO").is_in(["NOTURNO", "INTEGRAL", "MATUTINO", "VESPERTINO"])
)


df_plot = df.sample(n=min(50000, len(df))).to_pandas()


plt.figure(figsize=(12, 7))
sns.violinplot(
    data=df_plot, 
    x="TURNO", 
    y="NOTA_CANDIDATO", 
    palette="muted", 
    inner="quartile", 
    bw_method=0.2      
)

plt.title("Densidade e Distribuição de Notas por Turno", fontsize=15)
plt.xlabel("Turno do Curso", fontsize=12)
plt.ylabel("Nota do Candidato", fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig("5_notas_turno_violin_corrigido.png")
print("✅ Gráfico 5 (Violino) gerado com sucesso!")


# plot para agrupar por estado e turno para ver onde a nota é mais alta
plt.figure(figsize=(12, 8))
heatmap_data = df.group_by(["UF_IES", "TURNO"]).agg(
    pl.col("NOTA_CANDIDATO").mean().alias("MEDIA_NOTA")
).to_pandas().pivot(index="UF_IES", columns="TURNO", values="MEDIA_NOTA")

sns.heatmap(heatmap_data, annot=False, cmap="YlGnBu")
plt.title("Mapa de Calor: Média de Notas por Estado e Turno", fontsize=15)
plt.tight_layout()
plt.savefig("6_heatmap_notas.png")
print("✅ Gráfico 6 (Heatmap) gerado com sucesso!")

print("🚀 Martelada Final concluída. Verifique os arquivos PNG na pasta.")