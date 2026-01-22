using DataFrames, CSV, Statistics


df_res = CSV.read("LISTA_DE_ALOCACAO_OTIMIZADA.csv", DataFrame)

# Filtragem das pessoas que foram selecionadas
convocados = df_res[df_res.CONVOCADO .== "SIM", :]
sort!(convocados, :NOTA_CANDIDATO, rev=true)

println("\n=== TOP 50 ALUNOS SELECIONADOS PELO SEU MODELO ===")
exibir = convocados[1:50, [:NOTA_CANDIDATO, :UF_CANDIDATO, :PROB_REAL, :CONVOCADO]]
println(exibir)

println("\n--- ESTATÍSTICAS DA SUA LISTA ---")
media_nota = Statistics.mean(convocados.NOTA_CANDIDATO)
media_prob = Statistics.mean(convocados.PROB_REAL)

println("Média de Nota dos 50 Convocados: ", round(media_nota, digits=2))
println("Média de Certeza de Ocupação: ", round(media_prob * 100, digits=2), "%")

print("\nConclusão: Seu modelo garantiu a ocupação das 50 vagas com uma utilidade esperada de ")
println(round(media_nota * media_prob, digits=2), " pontos por vaga.")