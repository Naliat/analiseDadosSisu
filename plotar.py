import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('LISTA_DE_ALOCACAO_OTIMIZADA.csv')
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
pesos = pd.DataFrame({
    'Variável': ['Nota do Candidato', 'Proximidade (UF)'],
    'Importância (%)': [75, 25]  
})

plt.figure()
sns.barplot(data=pesos, x='Variável', y='Importância (%)', palette='viridis')
plt.title('Importância das Variáveis na Certeza de Alocação', fontsize=14)
plt.ylim(0, 100)
plt.savefig('importancia_pesos.png')
print("✅ Gráfico de Importância salvo.")

plt.figure()
sns.boxplot(data=df, x='CONVOCADO', y='NOTA_CANDIDATO', palette={'SIM': 'green', 'NÃO': 'red'})
plt.title('Distribuição de Notas: Convocados vs. Não Convocados', fontsize=14)
plt.xlabel('Candidato Selecionado?')
plt.ylabel('Nota do ENEM')
plt.savefig('boxplot_notas.png')
print("✅ Gráfico de Distribuição salvo.")


plt.figure()
sns.scatterplot(data=df, x='NOTA_CANDIDATO', y='PROB_REAL', hue='CONVOCADO', 
                palette={'SIM': 'green', 'NÃO': 'red'}, s=100, alpha=0.7)
plt.axhline(df['PROB_REAL'].mean(), color='blue', linestyle='--', label='Média de Certeza')
plt.title('Espaço de Decisão: Nota vs. Probabilidade de Matrícula', fontsize=14)
plt.xlabel('Nota do Candidato')
plt.ylabel('Certeza de Alocação (IA)')
plt.legend(title='Resultado Gurobi')
plt.savefig('mapa_certeza.png')
print("✅ Gráfico de Certeza salvo.")

print("\n🚀 Todos os gráficos foram gerados! Confira na sua pasta.")