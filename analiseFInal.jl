using DataFrames, CSV, Statistics


df_res = CSV.read("LISTA_DE_ALOCACAO_OTIMIZADA.csv", DataFrame)

df_tradicional = sort(df_res, :NOTA_CANDIDATO, rev=true)
nota_corte_tradicional = df_tradicional[50, :NOTA_CANDIDATO]
excluidos_pelo_risco = df_res[(df_res.NOTA_CANDIDATO .>= nota_corte_tradicional) .& (df_res.CONVOCADO .== "NÃO"), :]

println("\n=== ANÁLISE DE IMPACTO DO MODELO (CERTEZA DE ALOCAÇÃO) ===")

if nrow(excluidos_pelo_risco) > 0
    sort!(excluidos_pelo_risco, :NOTA_CANDIDATO, rev=true)
    println("Encontrados ", nrow(excluidos_pelo_risco), " candidatos que perderam a vaga devido ao risco de ociosidade:")
    println(first(excluidos_pelo_risco[:, [:NOTA_CANDIDATO, :UF_CANDIDATO, :PROB_REAL]], 10))
else
    println("Ninguém foi rejeitado pelo risco. O mérito puro coincidiu com a eficiência.")
    println("Isso ocorre quando todos os candidatos de topo têm a mesma probabilidade de vinda.")
end

# Apos analisar as pessoas que no algoritmo do sisu, iam pegar a vaga o modelo compara,
# e mostra os excluidos, dado a regra do meu modelo.
convocados_seu_modelo = df_res[df_res.CONVOCADO .== "SIM", :]
println("\n--- COMPARATIVO FINAL ---")
println("Média de Nota (Seu Modelo): ", round(mean(convocados_seu_modelo.NOTA_CANDIDATO), digits=2))
println("Média de Probabilidade (Seu Modelo): ", round(mean(convocados_seu_modelo.PROB_REAL) * 100, digits=2), "%")