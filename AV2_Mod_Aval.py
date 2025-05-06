import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.diagnostic import het_breuschpagan
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('dataset_22.csv')

categorical_vars = ['sistema_operacional', 'tipo_hd', 'tipo_processador']
df[categorical_vars] = df[categorical_vars].astype('category')
df = pd.get_dummies(df, columns=categorical_vars, drop_first=True)

df = df.dropna()
y = df['tempo_resposta'].astype(float)
X = df.drop(columns='tempo_resposta').astype(float)
X = sm.add_constant(X)

model = sm.OLS(y, X).fit()

numerical_df = df.select_dtypes(include=['float64', 'int64'])
statistics = {
    'Média': numerical_df.mean(),
    'Mediana': numerical_df.median(),
    'Mínimo': numerical_df.min(),
    'Máximo': numerical_df.max(),
    'Desvio Padrão': numerical_df.std()
}
stats_df = pd.DataFrame(statistics).round(2)
print("\n--- Estatísticas Descritivas ---")
print(stats_df)

plt.figure(figsize=(16, 10))
for i, col in enumerate(numerical_df.columns, 1):
    plt.subplot(2, 3, i)
    sns.histplot(df[col], kde=True, bins=20, color='skyblue')
    plt.title(f'Distribuição de {col}')
    plt.xlabel(col)
    plt.ylabel('Frequência')
plt.tight_layout()
plt.show()

print("\n--- Modelo 1 (com todas as variáveis) ---")
print(model.summary())

X_vif = X.copy()
vif_data = pd.DataFrame()
vif_data["Variável"] = X_vif.columns
vif_data["VIF"] = [variance_inflation_factor(X_vif.values, i) for i in range(X_vif.shape[1])]
print("\n--- Fatores de Inflação da Variância (VIF) ---")
print(vif_data)

residuos = model.resid
valores_ajustados = model.fittedvalues
plt.figure(figsize=(8, 5))
sns.scatterplot(x=valores_ajustados, y=residuos)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel("Valores ajustados")
plt.ylabel("Resíduos")
plt.title("Resíduos vs Ajustados")
plt.tight_layout()
plt.show()

bp_test = het_breuschpagan(residuos, model.model.exog)
labels = ['LM Stat', 'LM p-value', 'F Stat', 'F p-value']
print("\n--- Teste de Breusch-Pagan (Heterocedasticidade) ---")
print(dict(zip(labels, bp_test)))

X_reduced = X.drop(columns='latencia_ms')
model_reduced = sm.OLS(y, X_reduced).fit()

print("\n--- Comparação dos Modelos ---")
print("Modelo 1 (com todas as variáveis):")
print(f"R² ajustado: {model.rsquared_adj:.4f}")
print(f"Estatística F: {model.fvalue:.2f}")
print(f"P-valor F: {model.f_pvalue:.2e}")

print("\nModelo 2 (sem 'latencia_ms'):")
print(f"R² ajustado: {model_reduced.rsquared_adj:.4f}")
print(f"Estatística F: {model_reduced.fvalue:.2f}")
print(f"P-valor F: {model_reduced.f_pvalue:.2e}")
