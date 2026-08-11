"""
test_temperature.py — Gera a mesma pergunta com temperatures diferentes,
pra demonstrar na prática o efeito desse parâmetro (complemento rápido
à avaliação qualitativa já feita).
 
Como usar:
1. Coloque este arquivo na pasta do seu projeto (pos-ml-4)
2. Ative o venv: venv\\Scripts\\activate
3. Rode: python test_temperature.py
4. Revise a saída no terminal
"""

from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_PATH = "./modelo-chatbot"
PERGUNTA = "O que é inteligência artificial?"


def gerar(pergunta, tokenizer, model, temperature):
    prompt = f"Pergunta: {pergunta}\nResposta:"
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        pad_token_id=tokenizer.eos_token_id,
        max_new_tokens=120,
        temperature=temperature,
        top_p=0.9,
        repetition_penalty=1.3,
        do_sample=True,
    )
    texto_completo = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return texto_completo[len(prompt):].strip()


def main():
    print(f"Carregando modelo de: {MODEL_PATH}\n")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForCausalLM.from_pretrained(MODEL_PATH)
    model.eval()

    print(f"Pergunta fixa: {PERGUNTA}\n")
    print("=" * 70)

    for temp in [0.3, 1.3]:
        resposta = gerar(PERGUNTA, tokenizer, model, temperature=temp)
        print(f"\ntemperature = {temp}")
        print(f"Resposta: {resposta}")

    print("\n" + "=" * 70)
    print("Copie tudo acima para registrar o resultado do teste.")


if __name__ == "__main__":
    main()