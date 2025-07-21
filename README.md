
# 🗓️ Gestor de Férias

Sistema web desenvolvido com Flask para facilitar o planejamento e controle de férias, folgas e escalas operacionais. Ideal para equipes de RH, lideranças e operações que precisam manter visibilidade e evitar sobreposição de ausências.

---

## 🚀 Funcionalidades principais

- 📅 Cadastro e edição de férias e folgas por pessoa
- 🔍 Visualização por calendário e dashboards analíticos
- ⚙️ Regras customizadas por time e operação
- 🧩 Painel administrativo e navegação centralizada (hub)

---

## 🖼️ Exemplos visuais

### 📊 Dashboard Analítico
Painel com totais de férias/folgas, filtros por time e gráficos de capacidade:

<img width="1559" height="1135" alt="print_ferias_dashboard" src="https://github.com/user-attachments/assets/5d003c71-090f-4ace-b22a-be8c58ed2149" />


---

### 🧭 Hub de Navegação
Menu centralizado com acesso às principais áreas do sistema:

<img width="2210" height="1147" alt="print_ferias_hub" src="https://github.com/user-attachments/assets/1f55c963-4f1c-427d-9a3b-5fe547e0c2f4" />

---

### 📐 Cadastro de Regras Operacionais
Interface para definir limites e exceções por equipe:

<img width="2210" height="1147" alt="print_ferias_regras" src="https://github.com/user-attachments/assets/14575a3b-cd39-42bb-a2c1-9045ed0a0541" />


---

## ⚙️ Tecnologias utilizadas

- Python
- Flask
- pandas
- Jinja2 (HTML templating)
- Bootstrap (CSS)

---

## 📂 Estrutura de diretórios

```bash
feriasFolgas20/
├── app.py
├── templates/
│   ├── analitica_dashboard.html
│   ├── calendario.html
│   ├── ferias_gerenciador.html
│   ├── operacao_gerenciador.html
│   ├── regras_cadastro.html
│   └── ...
├── static/
│   └── ...
└── utils/
```

---

## 📦 Como executar localmente

```bash
git clone https://github.com/seu-usuario/gestor-ferias-bot.git
cd gestor-ferias-bot
pip install -r requirements.txt
python app.py
```

---

## 🌐 Versão online (Replit)

[🔗 Acessar projeto original no Replit](https://replit.com/@Carlos-Henri132/feriasFolgas20)

