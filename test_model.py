"""
Script de teste rápido para gerar respostas do modelo fine-tunado
e documentar exemplos para o relatório/vídeo do Tech Challenge.

Como usar:
1. Coloque este arquivo na pasta do seu projeto (pos-ml-4)
2. Ajuste MODEL_PATH abaixo se o nome da pasta do modelo salvo for diferente
3. Ative o venv: venv\\Scripts\\activate
4. Rode: python test_model.py
5. Copie a saída do terminal e me envie de volta
"""

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# ── Ajuste aqui se necessário ────────────────────────────────
MODEL_PATH = "./modelo-chatbot"  # pasta onde o finetune.py salvou o modelo

# Parâmetros de geração — sinta-se livre para editar e testar variações
GEN_PARAMS = {
    "max_new_tokens": 120,
    "temperature": 0.7,
    "top_p": 0.9,
    "repetition_penalty": 1.3,
    "do_sample": True,
}

# Perguntas de teste — cobrindo categorias diferentes
PERGUNTAS = [
    "Descreva os efeitos do aquecimento global.",
    "Escreva um poema curto sobre o outono.",
    "Quais são as vantagens e desvantagens do trabalho remoto?",
]
# ──────────────────────────────────────────────────────────────


def gerar_resposta(pergunta, tokenizer, model):
    # Mesmo formato usado no fine-tuning (finetune.py), senão o modelo
    # não "reconhece" o padrão pergunta/resposta que aprendeu.
    prompt = f"Pergunta: {pergunta}\nResposta:"
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        pad_token_id=tokenizer.eos_token_id,
        **GEN_PARAMS,
    )
    texto_completo = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # remove o prompt do início, deixando só o texto gerado depois de "Resposta:"
    resposta = texto_completo[len(prompt):].strip()
    return resposta


def main():
    print(f"Carregando modelo de: {MODEL_PATH}\n")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForCausalLM.from_pretrained(MODEL_PATH)
    model.eval()

    print("=" * 70)
    print("PARÂMETROS DE GERAÇÃO USADOS NESTE TESTE:")
    for k, v in GEN_PARAMS.items():
        print(f"  {k}: {v}")
    print("=" * 70)

    for i, pergunta in enumerate(PERGUNTAS, 1):
        resposta = gerar_resposta(pergunta, tokenizer, model)
        print(f"\n--- Exemplo {i} ---")
        print(f"PERGUNTA: {pergunta}")
        print(f"RESPOSTA: {resposta}")

    print("\n" + "=" * 70)
    print("Copie tudo acima (desde PARÂMETROS até o último exemplo)")
    print("e cole de volta na conversa com o Claude.")
    print("=" * 70)


if __name__ == "__main__":
    main()