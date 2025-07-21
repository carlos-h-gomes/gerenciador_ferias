from . import operacao_bp
from flask import render_template, request, redirect, url_for, flash
from utils.sheets import (
    get_rodizio, add_rodizio, update_rodizio, delete_rodizio,
    get_datas, get_pessoas, get_squads,
    get_ferias, add_ferias, update_ferias, delete_ferias, validar_regras_ferias
)
from datetime import datetime

# ✅ Rota principal Operação
@operacao_bp.route('/operacao-ui', methods=['GET', 'POST'])
def gerenciador_operacao():
    if request.method == 'POST':
        data = request.form['data']
        descricao = request.form['descricao']
        pessoas_trabalhando = request.form.getlist('pessoas')
        horarios = {}
        squads = {}

        for pessoa in pessoas_trabalhando:
            horarios[pessoa] = request.form.get(f'horario_{pessoa}', '')
            squads[pessoa] = request.form.get(f'squad_{pessoa}', '')

        # Monta string final no formato "Ana (08h), Matheus (07h)"
        quem_trabalha = ', '.join([
            f"{pessoa} ({squads[pessoa]} {horarios[pessoa]})" if squads[pessoa] and horarios[pessoa]
            else f"{pessoa} ({squads[pessoa]})" if squads[pessoa]
            else f"{pessoa} ({horarios[pessoa]})" if horarios[pessoa]
            else pessoa
            for pessoa in pessoas_trabalhando
        ])

        add_rodizio(data, descricao, quem_trabalha)
        flash('Operação registrada com sucesso!', 'success')
        return redirect(url_for('operacao.gerenciador_operacao'))

    datas = get_datas()
    pessoas = get_pessoas()
    squads = get_squads()
    rodizio = get_rodizio()

    # 🔧 Formata datas e ordena decrescente
    for o in rodizio:
        try:
            o['Data'] = datetime.strptime(o['Data'], "%Y-%m-%d").strftime("%d/%m/%Y")
        except:
            pass

    rodizio_sorted = sorted(
        rodizio,
        key=lambda x: datetime.strptime(x['Data'], "%d/%m/%Y"),
        reverse=True
    )

    return render_template(
        'operacao_gerenciador.html',
        datas=datas, pessoas=pessoas, squads=squads, rodizio=rodizio_sorted
    )

# ✅ Rota editar Operação
@operacao_bp.route('/editar-operacao/<int:id>', methods=['GET', 'POST'])
def editar_operacao(id):
    if request.method == 'POST':
        data = request.form['data']
        descricao = request.form['descricao']
        pessoas_trabalhando = request.form.getlist('pessoas')
        horarios = {}
        squads = {}

        for pessoa in pessoas_trabalhando:
            horarios[pessoa] = request.form.get(f'horario_{pessoa}', '')
            squads[pessoa] = request.form.get(f'squad_{pessoa}', '')

        quem_trabalha = ', '.join([
            f"{pessoa} ({squads[pessoa]} {horarios[pessoa]})" if squads[pessoa] and horarios[pessoa]
            else f"{pessoa} ({squads[pessoa]})" if squads[pessoa]
            else f"{pessoa} ({horarios[pessoa]})" if horarios[pessoa]
            else pessoa
            for pessoa in pessoas_trabalhando
        ])

        update_rodizio(id, data, descricao, quem_trabalha)
        flash('Operação atualizada com sucesso!', 'success')
        return redirect(url_for('operacao.gerenciador_operacao'))

    rodizio = get_rodizio()
    for o in rodizio:
        try:
            o['Data'] = datetime.strptime(o['Data'], "%Y-%m-%d").strftime("%d/%m/%Y")
        except:
            pass

    operacao_edit = next((o for o in rodizio if str(o['ID']) == str(id)), None)

    # 🔧 Parser para pré-preencher horários e squads
    horarios = {}
    squads_pessoa = {}

    if operacao_edit:
        # 🔧 Converte data para formato ISO (YYYY-MM-DD) para input type="date"
        try:
            data_iso = datetime.strptime(operacao_edit['Data'], "%d/%m/%Y").strftime("%Y-%m-%d")
            operacao_edit['Data_iso'] = data_iso
        except:
            operacao_edit['Data_iso'] = ''

        registros = operacao_edit['Quem Trabalha'].split(', ')
        for reg in registros:
            if '(' in reg:
                nome = reg.split('(')[0].strip()
                info = reg.split('(')[1].replace(')', '').strip()

                if ' ' in info:
                    parts = info.split(' ')
                    squads_pessoa[nome] = parts[0]
                    horarios[nome] = parts[1] if len(parts) > 1 else ''
                else:
                    horarios[nome] = info
                    squads_pessoa[nome] = ''
            else:
                nome = reg.strip()
                horarios[nome] = ''
                squads_pessoa[nome] = ''

    datas = get_datas()
    pessoas = get_pessoas()
    squads = get_squads()

    return render_template(
        'operacao_editar.html',
        operacao=operacao_edit,
        datas=datas, pessoas=pessoas, squads=squads,
        horarios=horarios, squads_pessoa=squads_pessoa
    )


# ✅ Rota remover Operação
@operacao_bp.route('/remover-operacao/<int:id>', methods=['POST'])
def remover_operacao(id):
    delete_rodizio(id)
    flash('Operação removida com sucesso!', 'success')
    return redirect(url_for('operacao.gerenciador_operacao'))



# ✅ Rota Gerenciador de Férias
@operacao_bp.route('/ferias-ui', methods=['GET', 'POST'])
def gerenciador_ferias():
    if request.method == 'POST':
        pessoa = request.form['pessoa']
        inicio = request.form['inicio']
        fim = request.form['fim']
        status = request.form['status']
        obs = request.form['obs']

        # 🔧 Validação de regras (somente notifica)
        mensagens = validar_regras_ferias(pessoa, inicio, fim)
        msg_total = ''
        if mensagens:
            msg_total += '⚠️ Conflitos detectados:\n' + '\n'.join(mensagens) + '\n'

        # 🔧 Cadastro real acontecendo aqui
        add_ferias(pessoa, inicio, fim, status, obs)

        msg_total += '✅ Férias cadastradas com sucesso!'
        flash(msg_total, 'success')
        return redirect(url_for('operacao.gerenciador_ferias'))


    ferias = get_ferias()
    pessoas = get_pessoas()

    # 🔧 Filtro de ano seguro com fallback de header
    ano = request.args.get('ano') or str(datetime.now().year)
    ferias_filtradas = []

    for f in ferias:
        data_inicio = f.get('Data Início') or f.get('Data de inicio') or ''
        if data_inicio.startswith(ano):
            # 🔧 Converte datas para DD/MM/YYYY para exibição
            for campo in ['Data Início', 'Data de inicio', 'Data Fim', 'Data de fim']:
                if f.get(campo):
                    try:
                        f[campo] = datetime.strptime(f[campo], "%Y-%m-%d").strftime("%d/%m/%Y")
                    except:
                        pass
            ferias_filtradas.append(f)

    return render_template(
        'ferias_gerenciador.html',
        ferias=ferias_filtradas,
        pessoas=pessoas,
        ano=ano
    )

# ✅ Rota editar férias
@operacao_bp.route('/editar-ferias/<int:id>', methods=['GET', 'POST'])
def editar_ferias(id):
    if request.method == 'POST':
        pessoa = request.form['pessoa']
        inicio = request.form['inicio']
        fim = request.form['fim']
        status = request.form['status']
        obs = request.form['obs']

        # 🔧 Validação de regras (somente notifica)
        mensagens = validar_regras_ferias(pessoa, inicio, fim)
        if mensagens:
            flash('⚠️ Conflitos detectados:\n' + '\n'.join(mensagens), 'warning')

        update_ferias(id, pessoa, inicio, fim, status, obs)
        flash('Férias atualizadas com sucesso!', 'success')
        return redirect(url_for('operacao.gerenciador_ferias'))

    ferias = get_ferias()
    ferias_edit = next((f for f in ferias if str(f['ID']) == str(id)), None)
    pessoas = get_pessoas()

    # 🔧 Pré-processa datas para input type="date"
    if ferias_edit:
        for campo in ['Data Início', 'Data de inicio']:
            if ferias_edit.get(campo):
                try:
                    ferias_edit['inicio_iso'] = datetime.strptime(ferias_edit[campo], "%d/%m/%Y").strftime("%Y-%m-%d")
                except:
                    ferias_edit['inicio_iso'] = ferias_edit[campo]
        for campo in ['Data Fim', 'Data de fim']:
            if ferias_edit.get(campo):
                try:
                    ferias_edit['fim_iso'] = datetime.strptime(ferias_edit[campo], "%d/%m/%Y").strftime("%Y-%m-%d")
                except:
                    ferias_edit['fim_iso'] = ferias_edit[campo]
    else:
        ferias_edit['inicio_iso'] = ''
        ferias_edit['fim_iso'] = ''

    return render_template(
        'ferias_editar.html',
        ferias=ferias_edit,
        pessoas=pessoas
    )

# ✅ Rota remover férias
@operacao_bp.route('/remover-ferias/<int:id>', methods=['POST'])
def remover_ferias(id):
    delete_ferias(id)
    flash('Férias removidas com sucesso!', 'success')
    return redirect(url_for('operacao.gerenciador_ferias'))