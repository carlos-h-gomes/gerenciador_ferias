from . import datas_bp
from flask import render_template, request, redirect, url_for, flash
from utils.sheets import get_datas, add_data, update_data, delete_data
import requests
from datetime import datetime, date

# 🔧 Função para converter datas em múltiplos formatos
def convert_date(date_str):
    try:
        return datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return datetime.min

# ✅ Rota principal Datas
@datas_bp.route('/datas-ui', methods=['GET', 'POST'])
def cadastro_datas():
    if request.method == 'POST':
        data = request.form['data']
        tipo = request.form['tipo']
        descricao = request.form['descricao']
        if data and tipo and descricao:
            data_formatada = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")
            add_data(data_formatada, descricao, tipo)
            flash('Data cadastrada com sucesso!', 'success')
        else:
            flash('Preencha todos os campos.', 'danger')
        return redirect(url_for('datas.cadastro_datas'))

    # 🔧 Filtro de ano dinâmico
    ano_selecionado = request.args.get('ano') or str(date.today().year)
    datas = get_datas()
    datas_filtradas = [d for d in datas if d['Data'].endswith(f"/{ano_selecionado}") or d['Data'].startswith(f"{ano_selecionado}-")]

    datas_sorted = sorted(datas_filtradas, key=lambda x: convert_date(x['Data']))
    return render_template('datas_cadastro.html', datas=datas_sorted, ano=ano_selecionado)


# ✅ Rota editar Data
@datas_bp.route('/editar-data/<int:id>', methods=['GET', 'POST'])
def editar_data(id):
    if request.method == 'POST':
        data = request.form['data']
        tipo = request.form['tipo']
        descricao = request.form['descricao']
        data_formatada = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")
        update_data(id, data_formatada, descricao, tipo)
        flash('Data atualizada com sucesso!', 'success')
        return redirect(url_for('datas.cadastro_datas'))

    datas = get_datas()
    data_edit = next((d for d in datas if str(d['ID']) == str(id)), None)

    if data_edit:
        try:
            # Converte para YYYY-MM-DD para preencher input type="date"
            data_edit['Data_iso'] = datetime.strptime(data_edit['Data'], "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            data_edit['Data_iso'] = data_edit['Data']

    return render_template('datas_editar.html', data_edit=data_edit)

# ✅ Rota remover Data
@datas_bp.route('/remover-data/<int:id>', methods=['POST'])
def remover_data(id):
    delete_data(id)
    flash('Data removida com sucesso!', 'success')
    return redirect(url_for('datas.cadastro_datas'))

# ✅ Rota importar feriados BrasilAPI com seleção de ano
@datas_bp.route('/importar-feriados', methods=['POST'])
def importar_feriados():
    ano = request.form['ano']
    response = requests.get(f"https://brasilapi.com.br/api/feriados/v1/{ano}")
    if response.status_code == 200:
        feriados = response.json()
        for f in feriados:
            date_format = datetime.strptime(f['date'], "%Y-%m-%d").strftime("%d/%m/%Y")
            add_data(date_format, f['name'], 'Feriado')
        flash(f'Feriados de {ano} importados com sucesso!', 'success')
    else:
        flash('Erro ao importar feriados da BrasilAPI.', 'danger')
    return redirect(url_for('datas.cadastro_datas'))
