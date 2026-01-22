using DataFrames, CSV, Statistics, MLJ, DecisionTree, JuMP, Gurobi

 
println("\n--- 1. LENDO DADOS COMPETITIVOS ---")
df = CSV.read("sisu_preparado.csv", DataFrame)


# Aqui a IA calcula a 'Certeza' de que cada pessoa vai realmente ocupar a vaga
y, X = unpack(df, ==(:EFETIVOU), col -> col in (:NOTA_CANDIDATO, :MESMO_ESTADO))
y = coerce(y, OrderedFactor)
X = coerce(X, :NOTA_CANDIDATO => Continuous, :MESMO_ESTADO => Continuous)

Tree = @load DecisionTreeClassifier pkg=DecisionTree verbosity=0
mach = machine(Tree(max_depth=5), X, y)
MLJ.fit!(mach, verbosity=0)


y_prob = MLJ.predict(mach, X)
niveis = levels(y)
# Nessa parte, se o modelo não encontrar uma boa variação, ele define 0.85 de confianã
df.PROB_REAL = length(niveis) > 1 ? pdf.(y_prob, niveis[2]) : fill(0.85, nrow(df))
println("\n--- 2. EXECUTANDO OTIMIZAÇÃO DA ALOCAÇÃO ---")
model = JuMP.Model(Gurobi.Optimizer)
n_alunos = nrow(df)
vagas_disponiveis = 50  # Aqui é definido a quantidade vagas para um curso, pode ser em breve colocaod
# para vagas de demais cursos.

@variable(model, x[1:n_alunos], Bin)

# Aqui é onde é criada a função para analisar como vai ser a questão do peso na "nota" final 
#desse aluno para pegar a vaga
# (Nota do Aluno * Probabilidade de ele realmente vir)
@objective(model, Max, sum(df.NOTA_CANDIDATO[i] * df.PROB_REAL[i] * x[i] for i in 1:n_alunos))

@constraint(model, sum(x[i] for i in 1:n_alunos) <= vagas_disponiveis)

optimize!(model)

df.CONVOCADO = [value(x[i]) > 0.5 ? "SIM" : "NÃO" for i in 1:n_alunos]

println("Candidatos analisados: ", n_alunos)
println("Vagas preenchidas com alta certeza: ", sum(df.CONVOCADO .== "SIM"))

CSV.write("LISTA_DE_ALOCACAO_OTIMIZADA.csv", df)
println("\n🚀 SUCESSO! O arquivo 'LISTA_DE_ALOCACAO_OTIMIZADA.csv' foi gerado.")