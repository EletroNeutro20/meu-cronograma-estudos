import streamlit as st
import json
import os
from datetime import datetime, timedelta
import pandas as pd

# Arquivos para salvar os dados
ARQUIVO_DADOS = "progresso_edital_web.json"
ARQUIVO_REVISOES = "agendamento_revisoes.json"

st.set_page_config(page_title="Portal de Estudos Inteligente", page_icon="🎓", layout="wide")

# --- BANCO DE DADOS LOCAL (JSON) ---
EDITAL_PADRAO = {
    "CONHECIMENTOS BÁSICOS": {
        "Língua Portuguesa": {
            "Fase 1: Morfologia": ["Domínio da ortografia oficial", "Emprego das classes de palavras", "Emprego de tempos e modos verbais"],
            "Fase 2: Sintaxe do Período Simples": ["Domínio da estrutura morfossintática", "Colocação dos pronomes átonos", "Emprego dos sinais de pontuação"],
            "Fase 3: Sintaxe do Período Composto": ["Relações de coordenação", "Relações de subordinação", "Domínio dos mecanismos de coesão"],
            "Fase 4: Concordância e Regência": ["Concordância verbal e nominal", "Regência verbal e nominal", "Emprego do sinal indicativo de crase"],
            "Fase 5: Texto e Reescrita": ["Reconhecimento de tipos e gêneros textuais", "Compreensão e interpretação de textos", "Reescrita: Significação e substituição", "Reescrita: Reorganização de períodos"]
        },
        "Língua Inglesa": {
            "Fase Única": ["Vocabulário e Cognatos", "Gramática Estrutural Essencial", "Técnicas de Leitura Instrumental", "Compreensão de textos escritos"]
        }
    },
    "CONHECIMENTOS ESPECÍFICOS": {
        "Fase 1: Base Matemática": {
            "Matemática Elementar": ["Lógica", "Conjuntos", "Relações", "Funções", "Progressões"],
            "Ferramentas para Cálculo/Física": ["Logaritmos", "Trigonometria", "Geometria Plana", "Geometria Espacial"],
            "Análise de Dados": ["Análise Combinatória", "Probabilidade", "Estatística Descritiva", "Matemática Financeira"]
        },
        "Fase 2: Avançados e Química": {
            "Matemática Superior": ["Geometria Analítica", "Cálculo Diferencial e Integral", "Álgebra Linear", "Cálculo Vetorial e Matricial"],
            "Química Geral": ["Estequiometria e soluções", "Funções inorgânicas e equilíbrio", "Química orgânica"]
        },
        "Fase 3: Física Clássica": {
            "Física Mecânica": ["Movimento de uma partícula", "Quantidade de movimento e força", "Impulso e trabalho"],
            "Física Aplicada/Estática": ["Estática dos corpos rígidos", "Momento de inércia de figuras planas"],
            "Outras Físicas": ["Acústica", "Ótica", "Eletricidade e Eletromagnetismo"]
        },
        "Fase 4: Engenharia de Matéria": {
            "Sólidos": ["Resistência dos materiais: Tração/compressão", "Resistência dos materiais: Tensões/deformações", "Força cortante e momento fletor", "Teoria da elasticidade"],
            "Fluidos": ["Mecânica dos fluidos: Propriedades/Análise", "Hidrostática e corpos imersos/flutuantes", "Conservação de massa, movimento e energia"],
            "Térmica e Transporte": ["Gases, misturas e soluções ideais", "Termodinâmica: Propriedades, trabalho, calor", "Primeira e segunda Leis da Termodinâmica", "Transferência de calor: Condução, convecção, radiação", "Transferência de massa"]
        },
        "Fase 5: Engenharia do Petróleo": {
            "Ciências da Terra": ["Fundamentos de geologia de petróleo", "Geofísica de petróleo"],
            "Poço e Reservatório": ["Perfuração de poços", "Avaliação das formações", "Completação de poços", "Reservatórios de petróleo"],
            "Produção e Processamento": ["Elevação e escoamento de petróleo", "Sistemas submarinos de produção", "Processamento primário de petróleo"]
        }
    }
}

# Inicializar Editais e Status
if "dados" not in st.session_state:
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f: st.session_state.dados = json.load(f)
    else:
        progresso_inicial = {b: {m: {f: {t: "Pendente" for t in ts} for f, ts in fs.items()} for m, fs in ms.items()} for b, ms in EDITAL_PADRAO.items()}
        st.session_state.dados = progresso_inicial

# Inicializar Agendador de Revisões
if "revisoes" not in st.session_state:
    if os.path.exists(ARQUIVO_REVISOES):
        with open(ARQUIVO_REVISOES, "r", encoding="utf-8") as f: st.session_state.revisoes = json.load(f)
    else:
        st.session_state.revisoes = []

def salvar_dados():
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f: json.dump(st.session_state.dados, f, ensure_ascii=False, indent=4)
def salvar_revisoes():
    with open(ARQUIVO_REVISOES, "w", encoding="utf-8") as f: json.dump(st.session_state.revisoes, f, ensure_ascii=False, indent=4)

# --- LISTA CHATA DE TODOS OS TÓPICOS PARA CRONOGRAMAS ---
todos_topicos_lista = []
for b, ms in EDITAL_PADRAO.items():
    for m, fs in ms.items():
        for f, ts in fs.items():
            for t in ts:
                todos_topicos_lista.append(f"{m} -> {t}")

# --- INTERFACE WEB ---
st.title("🎓 Portal do Estudante: Edital, Revisões & Cronograma")
st.markdown("---")

# Abas Principais do Sistema
aba_painel, aba_revisoes, aba_cronograma = st.tabs(["📋 Meu Progresso no Edital", "📅 Agendador de Revisões", "⚙️ Gerador de Cronograma (X e Y)"])

# ==========================================
# ABA 1: PROGRESSO NO EDITAL
# ==========================================
with aba_painel:
    # Cálculo das métricas básicas
    total, concluidos = 0, 0
    for b, ms in st.session_state.dados.items():
        for m, fs in ms.items():
            for f, ts in fs.items():
                for t, s in ts.items():
                    total += 1
                    if s != "Pendente": concluidos += 1
    
    prog_geral = (concluidos/total)*100 if total > 0 else 0
    st.metric(label="Sua evolução total no Edital", value=f"{prog_geral:.1f}%", delta=f"{concluidos} de {total} tópicos dominados")
    st.progress(prog_geral / 100)
    
    sub_aba_b, sub_aba_e = st.tabs(["📌 Conhecimentos Básicos", "🔬 Conhecimentos Específicos"])
    status_opcoes = ["Pendente", "Teoria Concluída", "Revisado", "Exercícios Feitos"]
    
    with sub_aba_b:
        for m, fs in st.session_state.dados["CONHECIMENTOS BÁSICOS"].items():
            st.subheader(f"🔹 {m}")
            for f, ts in fs.items():
                with st.expander(f"➔ {f}"):
                    for t, s in ts.items():
                        c1, c2 = st.columns([0.7, 0.3])
                        c1.markdown(f"**{t}**")
                        novo_s = c2.selectbox("Alterar Status", status_opcoes, index=status_opcoes.index(s), key=f"b_{m}_{f}_{t}")
                        if novo_s != s:
                            st.session_state.dados["CONHECIMENTOS BÁSICOS"][m][f][t] = novo_s
                            salvar_dados()
                            st.rerun()

    with sub_aba_e:
        for f, ms in st.session_state.dados["CONHECIMENTOS ESPECÍFICOS"].items():
            st.header(f"🧱 {f}")
            for m, ts in ms.items():
                with st.expander(f"📍 {m}"):
                    for t, s in ts.items():
                        c1, c2 = st.columns([0.7, 0.3])
                        c1.text(t)
                        novo_s = c2.selectbox("Alterar Status", status_opcoes, index=status_opcoes.index(s), key=f"e_{f}_{m}_{t}")
                        if novo_s != s:
                            st.session_state.dados["CONHECIMENTOS ESPECÍFICOS"][f][m][t] = novo_s
                            salvar_dados()
                            st.rerun()

# ==========================================
# ABA 2: AGENDADOR DE REVISÕES (Espaçadas)
# ==========================================
with aba_revisoes:
    st.header("📆 Sistema de Revisão Espaçada")
    st.caption("Cadastre o assunto que você estudou hoje e o sistema criará os alertas automáticos de revisão.")
    
    with st.form("nova_revisao"):
        c_assunto = st.selectbox("Selecione o Assunto Estudado:", todos_topicos_lista)
        c_data = st.date_input("Data de estudo:", datetime.today())
        metodo = st.selectbox("Método de Alerta:", ["Padrão Concurso (24h, 7d, 30d)", "Apenas 7 dias", "Personalizado (Escolher Data)"])
        data_personalizada = st.date_input("Se escolheu Personalizado, qual a data?", datetime.today() + timedelta(days=2))
        
        btn_salvar = st.form_submit_button("Agendar Alertas de Revisão")
        
        if btn_salvar:
            novas_datas = []
            if metodo == "Padrão Concurso (24h, 7d, 30d)":
                novas_datas.append((c_data + timedelta(days=1)).strftime('%Y-%m-%d'))
                novas_datas.append((c_data + timedelta(days=7)).strftime('%Y-%m-%d'))
                novas_datas.append((c_data + timedelta(days=30)).strftime('%Y-%m-%d'))
            elif metodo == "Apenas 7 dias":
                novas_datas.append((c_data + timedelta(days=7)).strftime('%Y-%m-%d'))
            else:
                novas_datas.append(data_personalizada.strftime('%Y-%m-%d'))
            
            for dt in novas_datas:
                st.session_state.revisoes.append({
                    "assunto": c_assunto,
                    "data_revisao": dt,
                    "concluida": False
                })
            salvar_revisoes()
            st.success("🗓️ Revisões agendadas e salvas com sucesso!")
            st.rerun()

    st.subheader("🚨 Suas próximas revisões agendadas")
    if len(st.session_state.revisoes) == 0:
        st.info("Nenhuma revisão agendada por enquanto. Bons estudos na teoria!")
    else:
        df_rev = pd.DataFrame(st.session_state.revisoes)
        # Filtrar e ordenar por data
        df_rev = df_rev.sort_values(by="data_revisao")
        
        for idx, row in df_rev.iterrows():
            status_emoji = "✅ Feita" if row['concluida'] else "⏳ Pendente"
            col_a, col_b, col_c = st.columns([0.5, 0.3, 0.2])
            col_a.markdown(f"**{row['assunto']}**")
            col_b.write(f"📅 Agendada para: {row['data_revisao']} ({status_emoji})")
            
            if not row['concluida']:
                if col_c.button("Marcar Feita", key=f"check_rev_{idx}"):
                    st.session_state.revisoes[idx]['concluida'] = True
                    salvar_revisoes()
                    st.rerun()

# ==========================================
# ABA 3: GERADOR DE CRONOGRAMA (Fazer X e Y)
# ==========================================
with aba_cronograma:
    st.header("⚙️ Gerador Automático de Fila de Estudos")
    st.markdown("""
    Insira as suas variáveis de tempo e disponibilidade:
    * **Variável X:** Quantos tópicos novos você quer estudar por dia.
    * **Variável Y:** Quantos dias na semana você vai se dedicar aos estudos.
    """)
    
    col_x, col_y = st.columns(2)
    var_x = col_x.number_input("Variável X (Tópicos por dia):", min_value=1, max_value=10, value=2)
    var_y = col_y.number_input("Variável Y (Dias de estudo por semana):", min_value=1, max_value=7, value=5)
    
    data_inicio = st.date_input("A partir de quando quer iniciar esse cronograma?", datetime.today())
    
    if st.button("Gerar Meu Cronograma Otimizado"):
        # Descobrir tópicos que ainda estão "Pendentes" no progresso
        topicos_pendentes = []
        for b, ms in st.session_state.dados.items():
            for m, fs in ms.items():
                for f, ts in fs.items():
                    for t, s in ts.items():
                        if s == "Pendente":
                            topicos_pendentes.append(f"{m} ({f}) -> {t}")
                            
        if len(topicos_pendentes) == 0:
            st.balloons()
            st.success("Você já zerou o edital! Use a aba de revisões para não esquecer.")
        else:
            st.subheader("📅 Seu Planejamento de Estudos Semanal")
            
            dados_cronograma = []
            data_atual = data_inicio
            contador_dias_estudados = 0
            indice_topico = 0
            
            while indice_topico < len(topicos_pendentes):
                # Verificar se o dia atual é um dia de estudo baseado na variável Y
                # Se Y=5, estuda de segunda a sexta (weekday de 0 a 4)
                if data_atual.weekday() < var_y:
                    # Pega X tópicos para esse dia
                    for _ in range(var_x):
                        if indice_topico < len(topicos_pendentes):
                            dados_cronograma.append({
                                "Data": data_atual.strftime('%d/%m/%Y (%A)'),
                                "Matéria e Tópico a Estudar": topicos_pendentes[indice_topico]
                            })
                            indice_topico += 1
                
                data_atual += timedelta(days=1)
            
            df_crono = pd.DataFrame(dados_cronograma)
            st.table(df_crono)
            st.caption(f"Cronograma gerado com sucesso. Total de {len(df_crono)} alocações diárias baseadas no seu ritmo de {var_x} matérias por dia útil.")
