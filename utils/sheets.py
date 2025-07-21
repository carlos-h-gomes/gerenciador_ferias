import gspread
from google.oauth2.service_account import Credentials
from functools import lru_cache
import json
from datetime import datetime


# 🔧 Configurações gerais
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CREDS_FILE = 'ferias-folgas-####8.json'
SPREADSHEET_ID = '######'

creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
gc = gspread.authorize(creds)

# 🔄 Função genérica para obter a worksheet
def get_worksheet(sheet_name):
    sh = gc.open_by_key(SPREADSHEET_ID)
    return sh.worksheet(sheet_name)

# ✅ CRUD Times
def get_times():
    ws = get_worksheet('Times')
    return ws.get_all_records()

def add_time(nome, gestor, cor):
    ws = get_worksheet('Times')
    ids = [int(row['ID']) for row in ws.get_all_records() if row['ID']] or [0]
    next_id = max(ids) + 1
    ws.append_row([next_id, nome, gestor, cor])


def update_time(id_value, nome, gestor):
    ws = get_worksheet('Times')
    data = ws.get_all_records()
    for idx, row in enumerate(data, start=2):
        if str(row['ID']) == str(id_value):
            ws.update_cell(idx, 2, nome)
            ws.update_cell(idx, 3, gestor)
            break

def delete_time(id_value):
    ws = get_worksheet('Times')
    data = ws.get_all_records()
    for idx, row in enumerate(data, start=2):
        if str(row['ID']) == str(id_value):
            ws.delete_rows(idx)
            break

# ✅ CRUD Squads
def get_squads():
    ws = get_worksheet('Squads')
    return ws.get_all_records()

def add_squad(nome, time):
    ws = get_worksheet('Squads')
    ids = [int(row['ID']) for row in ws.get_all_records() if row['ID']] or [0]
    next_id = max(ids) + 1
    ws.append_row([next_id, nome, time])

def update_squad(id_value, nome, time):
    ws = get_worksheet('Squads')
    data = ws.get_all_records()
    for idx, row in enumerate(data, start=2):
        if str(row['ID']) == str(id_value):
            ws.update_cell(idx, 2, nome)  # Coluna B = Nome
            ws.update_cell(idx, 3, time)  # Coluna C = Time
            break

def delete_squad(id_value):
    ws = get_worksheet('Squads')
    data = ws.get_all_records()
    for idx, row in enumerate(data, start=2):
        if str(row['ID']) == str(id_value):
            ws.delete_rows(idx)
            break

# ✅ CRUD Pessoas
def get_pessoas():
    ws = get_worksheet('Pessoas')
    return ws.get_all_records()

def add_pessoa(nome, email, times, squads, gestor):
    ws = get_worksheet('Pessoas')
    ids = [int(row['ID']) for row in ws.get_all_records() if row['ID']] or [0]
    next_id = max(ids) + 1
    times_str = ', '.join(times) if isinstance(times, list) else times
    squads_str = ', '.join(squads) if isinstance(squads, list) else squads
    ws.append_row([next_id, nome, email, gestor, times_str, squads_str])
    get_pessoas_cached.cache_clear()

def update_pessoa(id_value, nome, email, times, squads, gestor):
    ws = get_worksheet('Pessoas')
    data = ws.get_all_records()
    times_str = ', '.join(times) if isinstance(times, list) else times
    squads_str = ', '.join(squads) if isinstance(squads, list) else squads
    for idx, row in enumerate(data, start=2):
        if str(row['ID']) == str(id_value):
            ws.update_cell(idx, 2, nome)    # Coluna B
            ws.update_cell(idx, 3, email)   # Coluna C
            ws.update_cell(idx, 4, gestor)  # Coluna D
            ws.update_cell(idx, 5, times_str)  # Coluna E
            ws.update_cell(idx, 6, squads_str) # Coluna F
            break
    get_pessoas_cached.cache_clear()


def delete_pessoa(id_value):
    ws = get_worksheet('Pessoas')
    data = ws.get_all_records()
    for idx, row in enumerate(data, start=2):
        if str(row['ID']) == str(id_value):
            ws.delete_rows(idx)
            break
    get_pessoas_cached.cache_clear()

# ✅ CRUD Datas (Feriados, Plantões, Recessos)
def get_datas():
    ws = get_worksheet('Feriados')
    return ws.get_all_records()

def add_data(data, descricao, tipo):
    ws = get_worksheet('Feriados')
    ids = [int(row['ID']) for row in ws.get_all_records() if row['ID']] or [0]
    next_id = max(ids) + 1
    ws.append_row([next_id, data, descricao, tipo])

def update_data(id_value, data, descricao, tipo):
    ws = get_worksheet('Feriados')
    dados = ws.get_all_records()
    for idx, row in enumerate(dados, start=2):
        if str(row['ID']) == str(id_value):
            ws.update_cell(idx, 2, data)       # Coluna B = Data
            ws.update_cell(idx, 3, descricao)  # Coluna C = Descrição
            ws.update_cell(idx, 4, tipo)       # Coluna D = Tipo
            break


def delete_data(id_value):
    ws = get_worksheet('Feriados')
    dados = ws.get_all_records()
    for idx, row in enumerate(dados, start=2):
        if str(row['ID']) == str(id_value):
            ws.delete_rows(idx)
            break

# ✅ CRUD Regras
def get_regras():
    ws = get_worksheet('Regras')
    return ws.get_all_records()

def add_regra(tipo, descricao, parametros):
    ws = get_worksheet('Regras')
    ids = [int(row['ID']) for row in ws.get_all_records() if row['ID']] or [0]
    next_id = max(ids) + 1
    ws.append_row([next_id, descricao, tipo, parametros])

def update_regra(id_value, tipo, descricao, parametros):
    ws = get_worksheet('Regras')
    data = ws.get_all_records()
    for idx, row in enumerate(data, start=2):
        if str(row['ID']) == str(id_value):
            ws.update_cell(idx, 2, tipo)        # Coluna B = Tipo
            ws.update_cell(idx, 3, descricao)   # Coluna C = Descrição
            ws.update_cell(idx, 4, parametros)  # Coluna D = Parametros
            break


def delete_regra(id_value):
    ws = get_worksheet('Regras')
    dados = ws.get_all_records()
    for idx, row in enumerate(dados, start=2):
        if str(row['ID']) == str(id_value):
            ws.delete_rows(idx)
            break

# ✅ CRUD Férias (exemplo inicial)
def get_ferias():
    ws = get_worksheet('Ferias')
    return ws.get_all_records()

def add_ferias(pessoa, inicio, fim, status, obs):
    ws = get_worksheet('Ferias')
    ids = [int(row['ID']) for row in ws.get_all_records() if row['ID']] or [0]
    next_id = max(ids) + 1
    ws.append_row([next_id, pessoa, inicio, fim, status, obs])

# Outras funções adicionais (Rodízio) podem ser implementadas conforme definição de estrutura na planilha



@lru_cache(maxsize=1)
def get_regras_cached():
    return get_regras()

@lru_cache(maxsize=1)
def get_pessoas_cached():
    return get_pessoas()

# 🔧 Rodizio Feriados

def get_rodizio():
    ws = get_worksheet('Rodizio Feriados')
    records = ws.get_all_records()
    return records

def add_rodizio(data, descricao, quem_trabalha):
    ws = get_worksheet('Rodizio Feriados')
    ids = [int(row['ID']) for row in ws.get_all_records() if row['ID']] or [0]
    next_id = max(ids) + 1
    ws.append_row([next_id, data, descricao, quem_trabalha])

def update_rodizio(id_value, data, descricao, quem_trabalha):
    ws = get_worksheet('Rodizio Feriados')
    data_rows = ws.get_all_records()
    for idx, row in enumerate(data_rows, start=2):
        if str(row['ID']) == str(id_value):
            ws.update_cell(idx, 2, data)
            ws.update_cell(idx, 3, descricao)
            ws.update_cell(idx, 4, quem_trabalha)
            break

def delete_rodizio(id_value):
    ws = get_worksheet('Rodizio Feriados')
    data_rows = ws.get_all_records()
    for idx, row in enumerate(data_rows, start=2):
        if str(row['ID']) == str(id_value):
            ws.delete_rows(idx)
            break


# 🔧 Gerenciador de Férias

def get_ferias():
    ws = get_worksheet('Férias')
    return ws.get_all_records()

def add_ferias(pessoa, inicio, fim, status, obs):
    ws = get_worksheet('Férias')
    ids = [int(row['ID']) for row in ws.get_all_records() if row['ID']] or [0]
    next_id = max(ids) + 1
    ws.append_row([next_id, pessoa, inicio, fim, status, obs])

def update_ferias(id_value, pessoa, inicio, fim, status, obs):
    ws = get_worksheet('Férias')
    data = ws.get_all_records()
    for idx, row in enumerate(data, start=2):
        if str(row['ID']) == str(id_value):
            ws.update_cell(idx, 2, pessoa)
            ws.update_cell(idx, 3, inicio)
            ws.update_cell(idx, 4, fim)
            ws.update_cell(idx, 5, status)
            ws.update_cell(idx, 6, obs)
            break

def delete_ferias(id_value):
    ws = get_worksheet('Férias')
    data = ws.get_all_records()
    for idx, row in enumerate(data, start=2):
        if str(row['ID']) == str(id_value):
            ws.delete_rows(idx)
            break


def validar_regras_ferias(pessoa, inicio, fim):
    regras = get_regras()
    ferias = get_ferias()
    pessoas = get_pessoas()
    mensagens = []

    # 🔧 Busca squads e times da pessoa atual
    pessoa_info = next((p for p in pessoas if p['Nome'] == pessoa), {})
    squads_pessoa = pessoa_info.get('Squad', '').split(',') if pessoa_info.get('Squad') else []
    times_pessoa = pessoa_info.get('Times') or pessoa_info.get('Time') or ''

    for regra in regras:
        parametros = regra.get('Parâmetros', '') or regra.get('Parametros', '')
        if not parametros:
            continue

        try:
            param_dict = json.loads(parametros)
        except:
            param_dict = {}

        tipo = regra['Tipo']

        # ✅ 1. Incompatibilidade de pessoas
        if tipo == 'Incompatibilidade de pessoas':
            pessoas_incomp = param_dict.get('pessoas', [])
            for f in ferias:
                pessoa_existente = f.get('Pessoa')
                inicio_existente = f.get('Data Início') or f.get('Data de inicio')
                fim_existente = f.get('Data Fim') or f.get('Data de fim')

                if pessoa_existente == pessoa:
                    continue

                if pessoa_existente in pessoas_incomp and pessoa in pessoas_incomp:
                    if datas_sobrepoem(inicio, fim, inicio_existente, fim_existente):
                        mensagens.append(f"Incompatibilidade detectada: {pessoa} não pode tirar férias junto com {pessoa_existente}.")

        # ✅ 2. Limite por squad
        elif tipo == 'Limite por squad':
            squad_regra = param_dict.get('squad')
            max_pessoas = int(param_dict.get('max_pessoas', 0))
            count = 0
            for f in ferias:
                pessoa_f = f.get('Pessoa')
                pessoa_info_f = next((p for p in pessoas if p['Nome'] == pessoa_f), {})
                squads_f = pessoa_info_f.get('Squad', '').split(',') if pessoa_info_f.get('Squad') else []

                if squad_regra in squads_f:
                    inicio_existente = f.get('Data Início') or f.get('Data de inicio')
                    fim_existente = f.get('Data Fim') or f.get('Data de fim')
                    if datas_sobrepoem(inicio, fim, inicio_existente, fim_existente):
                        count += 1

            if squad_regra in squads_pessoa:
                count += 1  # conta também a pessoa atual

            if count > max_pessoas:
                mensagens.append(f"Limite excedido: Squad '{squad_regra}' tem {count} pessoas de férias (máx permitido: {max_pessoas}).")

        # ✅ 3. Limite por time
        elif tipo == 'Limite por time':
            time_regra = param_dict.get('time')
            max_pessoas = int(param_dict.get('max_pessoas', 0))
            count = 0
            for f in ferias:
                pessoa_f = f.get('Pessoa')
                pessoa_info_f = next((p for p in pessoas if p['Nome'] == pessoa_f), {})
                time_f = pessoa_info_f.get('Times') or pessoa_info_f.get('Time')

                if time_f == time_regra:
                    inicio_existente = f.get('Data Início') or f.get('Data de inicio')
                    fim_existente = f.get('Data Fim') or f.get('Data de fim')
                    if datas_sobrepoem(inicio, fim, inicio_existente, fim_existente):
                        count += 1

            if times_pessoa == time_regra:
                count += 1  # conta também a pessoa atual

            if count > max_pessoas:
                mensagens.append(f"Limite excedido: Time '{time_regra}' tem {count} pessoas de férias (máx permitido: {max_pessoas}).")

    return mensagens

def datas_sobrepoem(inicio1, fim1, inicio2, fim2):
    """Retorna True se dois períodos se sobrepõem"""
    try:
        # Converter datas para YYYY-MM-DD se estiverem em DD/MM/YYYY
        if '/' in inicio1:
            inicio1 = datetime.strptime(inicio1, "%d/%m/%Y").strftime("%Y-%m-%d")
        if '/' in fim1:
            fim1 = datetime.strptime(fim1, "%d/%m/%Y").strftime("%Y-%m-%d")
        if '/' in inicio2:
            inicio2 = datetime.strptime(inicio2, "%d/%m/%Y").strftime("%Y-%m-%d")
        if '/' in fim2:
            fim2 = datetime.strptime(fim2, "%d/%m/%Y").strftime("%Y-%m-%d")

        i1 = datetime.strptime(inicio1, "%Y-%m-%d")
        f1 = datetime.strptime(fim1, "%Y-%m-%d")
        i2 = datetime.strptime(inicio2, "%Y-%m-%d")
        f2 = datetime.strptime(fim2, "%Y-%m-%d")
        return i1 <= f2 and i2 <= f1
    except Exception as e:
        print(f"Erro datas_sobrepoem: {e}")
        return False



if __name__ == "__main__":
    print(get_times())
