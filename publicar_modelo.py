"""
publicar_modelo.py — Publica o modelo fine-tunado no Hugging Face Hub,
para que o app.py possa carregá-lo remotamente (necessário para o deploy
no Streamlit Cloud, já que a pasta modelo-chatbot/ não vai pro GitHub).

Pré-requisito: ter uma conta no Hugging Face (huggingface.co) e um
token de escrita (write token).

Como usar:
1. Ative o venv: venv\\Scripts\\activate
2. Rode: python publicar_modelo.py
3. Na primeira vez, vai pedir seu token do Hugging Face — cole quando pedir
4. Aguarde o upload (pode demorar alguns minutos, ~500MB)
"""

from huggingface_hub import login
from transformers import GPT2LMHeadModel, GPT2TokenizerFast

# ── Ajuste aqui ───────────────────────────────────────────────
MODEL_DIR_LOCAL = "modelo-chatbot"                      # pasta local gerada pelo finetune.py
REPO_ID = "gabifcavalheiro/chatbot-canarim-ptbr"          # nome que o modelo terá no Hugging Face Hub
# ──────────────────────────────────────────────────────────────


def main():
    print("Fazendo login no Hugging Face...")
    print("(se pedir token, gere um em https://huggingface.co/settings/tokens")
    print(" com permissão de 'Write')")
    login()

    print(f"\nCarregando modelo local de '{MODEL_DIR_LOCAL}'...")
    tokenizer = GPT2TokenizerFast.from_pretrained(MODEL_DIR_LOCAL)
    model = GPT2LMHeadModel.from_pretrained(MODEL_DIR_LOCAL)

    print(f"\nPublicando em '{REPO_ID}' (isso pode demorar alguns minutos)...")
    model.push_to_hub(REPO_ID)
    tokenizer.push_to_hub(REPO_ID)

    print(f"\nConcluído! Modelo disponível em: https://huggingface.co/{REPO_ID}")
    print(f"Use '{REPO_ID}' como MODEL_DIR no app.py.")


if __name__ == "__main__":
    main()