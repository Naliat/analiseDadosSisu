using JuMP
using Gurobi

estudantes = ["Tailan", "Joao", "Maria"]
notas = [800, 750, 900] # Maria tem a maior nota, Joao a menor
vagas_disponiveis = 2

# Criando modelo 
model = Model(Gurobi.Optimizer)

@variable(model, x[1:3], Bin)

#Maximizar a soma das notas dos alocados (Mérito)
@objective(model, Max, sum(notas[i] * x[i] for i in 1:3))

@constraint(model, sum(x[i] for i in 1:3) <= vagas_disponiveis)

optimize!(model)
for i in 1:3
    status = value(x[i]) > 0.5 ? "APROVADO" : "REPROVADO"
    println("Estudante: $(estudantes[i]) | Nota: $(notas[i]) | Status: $status")
end