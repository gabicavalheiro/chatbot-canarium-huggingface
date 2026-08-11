"""
finetune.py — Fine-tuning de um GPT-2 pré-treinado em português para virar um
chatbot de perguntas e respostas, usando um dataset de instruções do Hugging Face Hub.

O que este script faz, em ordem:
1. Carrega um modelo pré-treinado (já sabe português, mas não sabe "responder como chatbot")
2. Carrega o dataset de instruções direto do Hugging Face Hub (Canarim-Instruct-PTBR)
3. Formata cada exemplo como "Pergunta: ... Resposta: ..." e tokeniza
4. Ajusta (fine-tune) o modelo nesses dados
5. Salva o modelo ajustado numa pasta local

Uso:
    python finetune.py
"""

from datasets import load_dataset
from transformers import (
    GPT2LMHeadModel,
    GPT2TokenizerFast,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
)

# ---- Configurações que você pode/deve ajustar ----
MODEL_NAME = "pierreguillou/gpt2-small-portuguese"          # modelo pré-treinado (a "base")
DATASET_NAME = "dominguesm/Canarim-Instruct-PTBR-Dataset"    # dataset direto do HF Hub
NUM_EXEMPLOS = 3000                                           # fatia do dataset (ele tem 300k+ linhas; não precisamos de tudo)
OUTPUT_DIR = "modelo-chatbot"                                 # onde o modelo ajustado será salvo
BLOCK_SIZE = 128                                              # tamanho dos "pedaços" de texto pro treino
NUM_EPOCHS = 3                                                 # quantas vezes o modelo revisa o dataset inteiro


def main():
    print("1) Carregando tokenizer e modelo pré-treinado...")
    tokenizer = GPT2TokenizerFast.from_pretrained(MODEL_NAME)
    tokenizer.pad_token = tokenizer.eos_token  # GPT-2 não tem pad_token por padrão
    model = GPT2LMHeadModel.from_pretrained(MODEL_NAME)

    print(f"2) Carregando dataset '{DATASET_NAME}' do Hugging Face Hub...")
    raw_dataset = load_dataset(DATASET_NAME, split=f"train[:{NUM_EXEMPLOS}]")

    print("3) Formatando pares pergunta/resposta e tokenizando...")
    def formatar_e_tokenizar(exemplos):
        textos = [
            f"Pergunta: {instrucao}\nResposta: {saida}{tokenizer.eos_token}"
            for instrucao, saida in zip(exemplos["instruction"], exemplos["output"])
        ]
        return tokenizer(textos)

    dataset_tokenizado = raw_dataset.map(
        formatar_e_tokenizar, batched=True, remove_columns=raw_dataset.column_names
    )

    # Junta tudo numa sequência única e corta em blocos de tamanho fixo.
    # Isso é necessário porque o modelo espera sequências de tamanho consistente.
    def agrupar_em_blocos(exemplos):
        concatenado = sum(exemplos["input_ids"], [])
        total_length = (len(concatenado) // BLOCK_SIZE) * BLOCK_SIZE
        blocos = [
            concatenado[i : i + BLOCK_SIZE]
            for i in range(0, total_length, BLOCK_SIZE)
        ]
        return {"input_ids": blocos, "labels": blocos.copy()}

    dataset_final = dataset_tokenizado.map(
        agrupar_em_blocos, batched=True, remove_columns=dataset_tokenizado.column_names
    )

    # mlm=False porque GPT-2 prevê "o próximo token" (autoregressivo),
    # diferente do BERT que prevê tokens mascarados no meio da frase (masked LM).
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=NUM_EPOCHS,
        per_device_train_batch_size=2,
        save_steps=200,
        save_total_limit=2,
        logging_steps=20,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=dataset_final,
    )

    print("4) Iniciando fine-tuning (pode demorar alguns minutos)...")
    trainer.train()

    print(f"5) Salvando modelo ajustado em '{OUTPUT_DIR}'...")
    trainer.save_model(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print("Concluído! Use este diretório no app.py para conversar com o chatbot.")


if __name__ == "__main__":
    main()