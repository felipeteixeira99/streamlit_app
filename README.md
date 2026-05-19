# 💰 Painel Financeiro Pessoal com Selic Automática

Acompanhe a evolução do seu patrimônio, simule metas 
financeiras e visualize projeções com a taxa Selic 
atualizada automaticamente via API do Banco Central.

## O que o app faz

- Importa seu extrato financeiro via CSV
- Mostra evolução patrimonial por instituição ao longo do tempo
- Calcula médias móveis de 6, 12 e 24 meses automaticamente
- Busca a taxa Selic vigente direto da API do Banco Central
- Simula quanto você vai acumular dado seu salário, 
  custos fixos e rendimento sobre patrimônio atual
- Acompanha atingimento de meta mês a mês com gráfico de progresso

## Tecnologias

Python · Streamlit · Pandas · API Banco Central (BCB)

## Como rodar

pip install -r requirements.txt
streamlit run main.py

## Entrada esperada

CSV com colunas: Data (dd/mm/aaaa), Instituição, Valor

## Exemplo de uso

1. Exporte seus saldos mensais por banco em CSV
2. Faça upload no app
3. Configure salário, custos fixos e meta anual
4. Acompanhe o progresso mês a mês
