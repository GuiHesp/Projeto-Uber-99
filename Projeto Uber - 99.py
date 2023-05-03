#!/usr/bin/env python
# coding: utf-8

# # PROJETO UBER/99

# In[ ]:


import pandas as pd
import random
import numpy as np

tabela = pd.read_excel(r"testeuber.xlsx")
display(tabela)


# ### Gerando os ganhos

# In[ ]:


for linha in tabela.index:
    tabela.loc[linha, "Uber"] = np.random.randint(100, 200)
    tabela.loc[linha, "99."] = np.random.randint(50, 100)
    tabela.loc[linha, "Gasolina"] = np.random.randint(50, 70)

display(tabela)

tabela.info()


# ### Dividindo a data para pegar os Domingos

# In[ ]:


from datetime import datetime

tabela["Dia da Semana"] = tabela["Data"].dt.day_name()
tabela


# ### Descartando os Domingos

# In[ ]:


tabela.drop(tabela.loc[tabela['Dia da Semana']=='Sunday'].index, inplace=True)
tabela


# ### Resetando o index da tabela

# In[ ]:


tabela = tabela.reset_index(drop=True) #drop true para tirar a coluna q iria ser criada de index
tabela


# ### Calculando Lucro dos dias trabalhados

# In[ ]:


tabela["Lucro"] = tabela["Uber"] + tabela["99."] - tabela["Gasolina"]
tabela


# ### 15% para reserva com gastos do carro

# In[ ]:


tabela["15%"] = tabela["Lucro"] * 0.15
tabela["15%"] = tabela["15%"].astype(int)
tabela


# ### Julgando os dias para ver se batemos a meta estabelecida

# In[ ]:


meta = 130
for linha in tabela.index:
    if tabela.loc[linha, "Lucro"] >= meta:
        tabela.loc[linha, "Meta"] = 'Sucesso'
    else:
        tabela.loc[linha, "Meta"] = 'X'
display(tabela)
tabela.info()


# ### Ajeitando Data para o formato Brasileiro

# In[ ]:


from datetime import datetime

tabela["Data"] = pd.to_datetime(tabela["Data"], format=("%Y,%m,%d")).dt.strftime('%d/%m/%Y')

tabela


# ### Calculando os valores do mês trabalhado

# In[ ]:


gas = tabela["Gasolina"].sum()

soma_uber = tabela["Uber"].sum()
soma_99 = tabela["99."].sum()
soma_salariobruto = soma_uber + soma_99

soma_media = tabela["Lucro"].sum()
soma_15 = tabela["15%"].sum()


# ### Reposicionando Colunas para melhorar o entendimento da tabela

# In[ ]:


tabela = tabela[['Data', 'Dia da Semana', 'Uber', '99.','Gasolina', 'Lucro', '15%', 'Meta']]
tabela


# ### Enviando por email o resultado do mês

# In[ ]:


import smtplib
import email.message

 

def enviar_email():  
    corpo_email = f"""
    <p><strong>Resumo Mensal de trabalho:</strong></p>
    <p><b>Salário Bruto</b>: R$ {soma_salariobruto:,.2f} reais.</p>
    <p><b>Salário Líquido (descontando Gasolina: {gas:,.2f} reais.)</b>: R$ {soma_media:,.2f} reais.</p>
    <p><b>Reserva do Carro(15%)</b>: R$ {soma_15:,.2f} reais.</p>
    <p><b>Salário Final</b>: R$ {soma_media - soma_15:,.2f} reais.</p>
    {tabela.to_html(index=False)}
    <p>Tamo Junto!.</p>
    """

    msg = email.message.Message()
    msg['Subject'] = "Resumo Mensal Uber/99"
    msg['From'] = 'email'
    msg['To'] = 'email'
    password = 'password' 
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email )

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    # Login Credentials for sending the mail
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('Email enviado')
        

enviar_email()

