from . import pessoas_bp
from flask import render_template, request, redirect, url_for, flash
from utils.sheets import get_pessoas, add_pessoa, update_pessoa, delete_pessoa, get_times, get_squads

# 🔧 Função auxiliar para buscar gestor conforme times selecionados
def buscar_gestor(times_selecionados):
    times = get_times()
    gestores = []
    for t in times:
        if t['Nome'] in times_selecionados and t['Gestor'] not in gestores:
            gestores.append(t['Gestor'])
    return ', '.join(gestores)

# ✅ Rota principal Pessoas
@pessoas_bp.route('/pessoas-ui', methods=['GET', 'POST'])
def cadastro_pessoas():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        times = request.form.getlist('times')
        squads = request.form.getlist('squads')
        gestor = buscar_gestor(times)

        if nome and email and times and squads:
            add_pessoa(nome, email, times, squads, gestor)
            flash('Pessoa cadastrada com sucesso!', 'success')
        else:
            flash('Preencha todos os campos.', 'danger')
        return redirect(url_for('pessoas.cadastro_pessoas'))

    pessoas = get_pessoas()
    pessoas_sorted = sorted(pessoas, key=lambda x: x['Nome'])
    times = get_times()
    squads = get_squads()
    return render_template('pessoas_cadastro.html', pessoas=pessoas_sorted, times=times, squads=squads)

# ✅ Rota editar Pessoa
@pessoas_bp.route('/editar-pessoa/<int:id>', methods=['GET', 'POST'])
def editar_pessoa(id):
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        times = request.form.getlist('times')
        squads = request.form.getlist('squads')
        gestor = buscar_gestor(times)
        update_pessoa(id, nome, email, times, squads, gestor)
        flash('Pessoa atualizada com sucesso!', 'success')
        return redirect(url_for('pessoas.cadastro_pessoas'))

    # GET ➔ Buscar pessoa específica para edição
    pessoas = get_pessoas()
    pessoa = next((p for p in pessoas if str(p['ID']) == str(id)), None)
    times = get_times()
    squads = get_squads()

    return render_template('pessoas_editar.html', pessoa=pessoa, times=times, squads=squads)

# ✅ Rota remover Pessoa
@pessoas_bp.route('/remover-pessoa/<int:id>')
def remover_pessoa(id):
    delete_pessoa(id)
    flash('Pessoa removida com sucesso!', 'success')
    return redirect(url_for('pessoas.cadastro_pessoas'))

