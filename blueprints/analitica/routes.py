from . import analitica_bp
from flask import render_template, request
from utils.sheets import get_pessoas_cached, get_times, get_squads, get_regras, get_datas, get_ferias
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from collections import defaultdict
import json
import random

# ✅ Função utilitária
def datas_sobrepoem(inicio1, fim1, inicio2, fim2):
    try:
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

# 🔧 Função para gerar cor aleatória em HEX
def gerar_cor_hex():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

# ✅ Rota principal Dashboard Analítico
@analitica_bp.route('/analitica-ui', methods=['GET'])
def dashboard_analitica():
    pessoas = get_pessoas_cached()
    gestores = list(set([p.get('Gestor') for p in pessoas if p.get('Gestor')]))
    times = get_times()
    squads = get_squads()
    regras = get_regras()
    datas = get_datas()
    ferias = get_ferias()

    # 🔧 Garante cores fixas para todos os times e salva na planilha se não existir
    for time in times:
        if not time.get('Cor'):
            time['Cor'] = gerar_cor_hex()
            # 🔧 Aqui você implementa sua função para salvar na planilha
            # Exemplo:
            # update_time_color(time['ID'], time['Cor'])
            print(f"[INFO] Cor gerada para Time '{time['Nome']}': {time['Cor']}")

    # 🔧 Mapeia cores dos times
    cores_times = { t['Nome']: t['Cor'] for t in times }

    # 🔧 Filtros globais
    filtro_gestor = request.args.get('gestor')
    filtro_time = request.args.get('time')
    filtro_squad = request.args.get('squad')
    filtro_periodo = request.args.get('periodo')
    filtro_view = request.args.get('view') or 'month'
    periodo_navegacao = request.args.get('periodo_navegacao') or 'current'

    # 🔧 Data base ajustada por view
    try:
        if filtro_view == 'year':
            current_date = datetime.strptime(filtro_periodo, "%Y") if filtro_periodo else datetime.now()
        elif filtro_view == 'month':
            current_date = datetime.strptime(filtro_periodo, "%Y-%m") if filtro_periodo else datetime.now()
        else:
            current_date = datetime.strptime(filtro_periodo, "%Y-%m-%d") if filtro_periodo else datetime.now()
    except:
        current_date = datetime.now()

    # 🔧 Navegação ajustada
    if periodo_navegacao == 'prev':
        if filtro_view == 'month':
            current_date -= relativedelta(months=1)
        elif filtro_view == 'week':
            current_date -= timedelta(days=7)
        elif filtro_view == 'day':
            current_date -= timedelta(days=1)
        elif filtro_view == 'year':
            current_date = current_date.replace(year=current_date.year - 1)
    elif periodo_navegacao == 'next':
        if filtro_view == 'month':
            current_date += relativedelta(months=1)
        elif filtro_view == 'week':
            current_date += timedelta(days=7)
        elif filtro_view == 'day':
            current_date += timedelta(days=1)
        elif filtro_view == 'year':
            current_date = current_date.replace(year=current_date.year + 1)

    # 🔧 Filtros aplicados
    pessoas_filtradas = pessoas
    if filtro_gestor:
        pessoas_filtradas = [p for p in pessoas_filtradas if p.get('Gestor') == filtro_gestor]
    if filtro_time:
        pessoas_filtradas = [p for p in pessoas_filtradas if filtro_time in (p.get('Times') or p.get('Time') or '')]
    if filtro_squad:
        pessoas_filtradas = [p for p in pessoas_filtradas if filtro_squad in (p.get('Squad') or '')]

    # ✅ Alertas reais
    alertas = []
    for regra in regras:
        tipo = regra.get('Tipo')
        parametros = regra.get('Parâmetros', '') or regra.get('Parametros', '')

        try:
            param_dict = json.loads(parametros)
        except:
            param_dict = {}

        if tipo == 'Incompatibilidade de pessoas':
            pessoas_incomp = param_dict.get('pessoas', [])
            for i in range(len(pessoas_incomp)):
                for j in range(i + 1, len(pessoas_incomp)):
                    pessoa_a = pessoas_incomp[i]
                    pessoa_b = pessoas_incomp[j]

                    ferias_a = [f for f in ferias if f.get('Pessoa') == pessoa_a]
                    ferias_b = [f for f in ferias if f.get('Pessoa') == pessoa_b]

                    for fa in ferias_a:
                        for fb in ferias_b:
                            if datas_sobrepoem(
                                fa.get('Data Início') or fa.get('Data de inicio', ''),
                                fa.get('Data Fim') or fa.get('Data de fim', ''),
                                fb.get('Data Início') or fb.get('Data de inicio', ''),
                                fb.get('Data Fim') or fb.get('Data de fim', '')
                            ):
                                periodo = f"{fa.get('Data Início') or fa.get('Data de inicio')} a {fa.get('Data Fim') or fa.get('Data de fim')}"
                                alertas.append(f"⚠️ Incompatibilidade: {pessoa_a} e {pessoa_b} estão de férias simultaneamente no período {periodo}.")

    # ✅ Gráfico de férias por mês (com meses em português)
    meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    ferias_qtd = [0]*12
    for f in ferias:
        if f.get('Pessoa') not in [p.get('Nome') for p in pessoas_filtradas]:
            continue
        try:
            data_inicio = f.get('Data de inicio') or f.get('Data Início')
            if data_inicio:
                mes = int(datetime.strptime(data_inicio, '%Y-%m-%d').strftime('%m'))
                ferias_qtd[mes-1] += 1
        except Exception as e:
            print(f"[ERRO parse ferias] {e}")

    # ✅ Agenda (eventos)
    agenda_dict = defaultdict(list)
    for d in datas:
        data = d.get('Data')
        if data:
            try:
                data_iso = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
            except:
                data_iso = data
            agenda_dict[data_iso].append({
                "tipo": d.get('Tipo'),
                "descricao": d.get('Descrição')
            })

    for f in ferias:
        if f.get('Pessoa') not in [p.get('Nome') for p in pessoas_filtradas]:
            continue

        data_inicio_str = f.get('Data de inicio') or f.get('Data Início')
        data_fim_str = f.get('Data fim') or f.get('Data Fim')

        if not data_inicio_str or not data_fim_str:
            continue

        try:
            data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d')
            data_fim = datetime.strptime(data_fim_str, '%Y-%m-%d')
        except Exception as e:
            print(f"[ERRO parse datas ferias] {e}")
            continue

        # 🔧 Descobre time da pessoa e sua cor
        pessoa_info = next((p for p in pessoas_filtradas if p.get('Nome') == f.get('Pessoa')), {})
        time_pessoa = pessoa_info.get('Time') or pessoa_info.get('Times') or "Outro"
        cor_time = cores_times.get(time_pessoa, "#9e9e9e")

        current_day = data_inicio
        while current_day <= data_fim:
            date_str = current_day.strftime('%Y-%m-%d')
            agenda_dict[date_str].append({
                "tipo": "Férias",
                "descricao": f"{f.get('Pessoa')} ({time_pessoa})",
                "time": time_pessoa,
                "cor_time": cor_time
            })
            current_day += timedelta(days=1)


    # 🔧 Converte agenda_dict em lista de eventos com cores diferenciadas
    agenda_events = []
    cores_tipos = {
        "Plantão": "#ff9800", # laranja
        "Outro": "#2196f3"    # azul
    }

    for date, events in agenda_dict.items():
        for ev in events:
            tipo = ev['tipo']
            if tipo == "Férias":
                cor = ev.get("cor_time", "#4caf50")
            else:
                cor = cores_tipos.get(tipo, "#9e9e9e")  # cinza default

            agenda_events.append({
                "title": f"{tipo}: {ev['descricao']}",
                "start": date,
                "color": cor
            })

    return render_template('analitica_dashboard.html',
           gestores=gestores,
           times=times,
           squads=squads,
           pessoas=pessoas_filtradas,
           alertas=alertas,
           meses=meses,
           ferias_qtd=ferias_qtd,
           agenda_events=agenda_events,
           current_date=current_date,
           datetime=datetime,
           timedelta=timedelta,
           filtro_view=filtro_view)
