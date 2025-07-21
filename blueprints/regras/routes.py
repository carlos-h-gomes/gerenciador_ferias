from . import regras_bp
from flask import render_template, request, redirect, url_for, flash
from utils.sheets import get_regras, get_regras_cached, add_regra, update_regra, delete_regra, get_times, get_squads, get_pessoas, get_datas

import json

# ✅ Rota principal Regras
@regras_bp.route('/regras-ui', methods=['GET', 'POST'])
def cadastro_regras():
    if request.method == 'POST':
        tipo = request.form['tipo']
        descricao = request.form.get('descricao', '')
        parametros = {}

        # 🔧 Montagem dinâmica dos parâmetros conforme o tipo selecionado
        if tipo == 'Limite por squad':
            parametros['squad'] = request.form['squad']
            parametros['max_pessoas'] = request.form['max_pessoas']
        elif tipo == 'Limite por time':
            parametros['time'] = request.form['time']
            parametros['max_pessoas'] = request.form['max_pessoas']
        elif tipo == 'Incompatibilidade de pessoas':
            parametros['pessoas'] = request.form.getlist('pessoas')
        elif tipo == 'Limite por data':
            parametros['data'] = request.form['data']
            parametros['max_pessoas'] = request.form['max_pessoas']
            parametros['min_pessoas'] = request.form['min_pessoas']

        # 🔄 Adiciona regra e limpa cache
        add_regra(tipo, descricao, json.dumps(parametros, ensure_ascii=False))
        get_regras_cached.cache_clear()
        flash('Regra cadastrada com sucesso!', 'success')
        return redirect(url_for('regras.cadastro_regras'))

    # 🔍 GET ➔ Carrega dados com cache
    try:
        regras = get_regras_cached()
        times = get_times()
        squads = get_squads()
        pessoas = get_pessoas()
        datas = get_datas()
    except Exception as e:
        flash('Erro ao acessar dados do Google Sheets. Tente novamente em instantes.', 'danger')
        regras, times, squads, pessoas, datas = [], [], [], [], []

    return render_template('regras_cadastro.html', regras=regras, times=times, squads=squads, pessoas=pessoas, datas=datas)

# ✅ Rota editar Regra
@regras_bp.route('/editar-regra/<int:id>', methods=['GET', 'POST'])
def editar_regra(id):
    if request.method == 'POST':
        tipo = request.form['tipo']
        descricao = request.form.get('descricao', '')
        parametros = {}

        # 🔧 Montagem dinâmica dos parâmetros conforme o tipo selecionado
        if tipo == 'Limite por squad':
            parametros['squad'] = request.form['squad']
            parametros['max_pessoas'] = request.form['max_pessoas']
        elif tipo == 'Limite por time':
            parametros['time'] = request.form['time']
            parametros['max_pessoas'] = request.form['max_pessoas']
        elif tipo == 'Incompatibilidade de pessoas':
            parametros['pessoas'] = request.form.getlist('pessoas')
        elif tipo == 'Limite por data':
            parametros['data'] = request.form['data']
            parametros['max_pessoas'] = request.form['max_pessoas']
            parametros['min_pessoas'] = request.form['min_pessoas']

        # 🔄 Atualiza regra e limpa cache
        update_regra(id, tipo, descricao, json.dumps(parametros, ensure_ascii=False))
        get_regras_cached.cache_clear()
        flash('Regra atualizada com sucesso!', 'success')
        return redirect(url_for('regras.cadastro_regras'))

    # GET ➔ Buscar regra específica para edição com cache
    try:
        regras = get_regras_cached()
    except Exception as e:
        flash('Erro ao acessar Google Sheets. Tente novamente em instantes.', 'danger')
        return redirect(url_for('regras.cadastro_regras'))

    regra_edit = next((r for r in regras if str(r['ID']) == str(id)), None)

    # 🔧 Converte parametros customizados ou JSON para dict
    print('🔎 regra_edit:', regra_edit)

    if regra_edit and regra_edit.get('Parâmetros'):
        parametros_raw = regra_edit['Parâmetros']
        print('🚨 parametros_raw:', parametros_raw)  # <-- log claro

        parametros_dict = {}
        try:
            parametros_dict = json.loads(parametros_raw)
            print('✅ parametros_dict (json):', parametros_dict)
        except json.JSONDecodeError as e:
            print('⚠️ JSON decode error:', e)
            # Parser fallback para chave=valor;
            for item in parametros_raw.split(';'):
                if '=' in item:
                    chave, valor = item.split('=', 1)
                    parametros_dict[chave.strip()] = valor.strip()
            print('✅ parametros_dict (fallback):', parametros_dict)

        regra_edit['Parametros_dict'] = parametros_dict
    else:
        print('❌ Sem Parametros ou regra_edit None')
        regra_edit['Parametros_dict'] = {}


    try:
        times = get_times()
        squads = get_squads()
        pessoas = get_pessoas()
        datas = get_datas()
    except Exception as e:
        flash('Erro ao acessar dados adicionais.', 'danger')
        times, squads, pessoas, datas = [], [], [], []

    return render_template('regras_editar.html', regra=regra_edit, times=times, squads=squads, pessoas=pessoas, datas=datas)

# ✅ Rota remover Regra
@regras_bp.route('/remover-regra/<int:id>')
def remover_regra(id):
    delete_regra(id)
    get_regras_cached.cache_clear()
    flash('Regra removida com sucesso!', 'success')
    return redirect(url_for('regras.cadastro_regras'))
