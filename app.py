"""
app.py — Playground Streamlit para testar o chatbot de perguntas e respostas.
Uso:
    streamlit run app.py
"""
import streamlit as st
import torch
from transformers import GPT2LMHeadModel, GPT2TokenizerFast

st.set_page_config(page_title="Chatbot PT-BR", page_icon="🤖")

# Modelo publicado no Hugging Face Hub (ver publicar_modelo.py).
# Isso é necessário porque o deploy no Streamlit Cloud não tem acesso
# à pasta local "modelo-chatbot" gerada pelo finetune.py — ela não vai
# pro GitHub por ser pesada demais.
MODEL_DIR = "gabifcavalheiro/chatbot-canarim-ptbr"


@st.cache_resource
def carregar_modelo():
    tokenizer = GPT2TokenizerFast.from_pretrained(MODEL_DIR)
    model = GPT2LMHeadModel.from_pretrained(MODEL_DIR)
    model.eval()
    return tokenizer, model


tokenizer, model = carregar_modelo()

st.title("🤖 Chatbot em Português")
st.write(
    "Modelo GPT-2 em português, ajustado (fine-tuned) com o dataset "
    "Canarim-Instruct-PTBR para responder perguntas. "
    "Digite uma pergunta e ajuste os parâmetros de geração abaixo."
)

pergunta = st.text_area("Sua pergunta:", value="")

col1, col2, col3 = st.columns(3)
with col1:
    max_length = st.slider("Tamanho máximo (tokens)", 20, 300, 120)
with col2:
    temperature = st.slider(
        "Temperatura (criatividade)", 0.1, 1.5, 0.7,
        help="Valores baixos = mais previsível/coerente. Valores altos = mais criativo/arriscado."
    )
with col3:
    top_p = st.slider(
        "Top-p (foco)", 0.1, 1.0, 0.9,
        help="Restringe a escolha de próximas palavras às mais prováveis, cumulativamente."
    )

if st.button("Perguntar"):
    if not pergunta.strip():
        st.warning("Digite uma pergunta primeiro.")
    else:
        with st.spinner("Pensando..."):
            prompt_formatado = f"Pergunta: {pergunta}\nResposta:"
            entrada = tokenizer.encode(prompt_formatado, return_tensors="pt")
            with torch.no_grad():
                saida = model.generate(
                    entrada,
                    max_length=entrada.shape[1] + max_length,
                    do_sample=True,
                    temperature=temperature,
                    top_p=top_p,
                    top_k=50,
                    repetition_penalty=1.3,  # penaliza repetição de tokens já usados
                    pad_token_id=tokenizer.eos_token_id,
                )
            texto_gerado = tokenizer.decode(saida[0], skip_special_tokens=True)
            # Extrai só a parte gerada depois de "Resposta:"
            resposta = texto_gerado.split("Resposta:", 1)[-1].strip()
        st.markdown("### Resposta:")
        st.write(resposta)

st.markdown("---")
st.caption(
    "Projeto de Fine-tuning com Hugging Face Transformers — "
    "MLE Pós-graduação FIAP, Fase 4."
)