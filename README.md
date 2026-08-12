# Chatbot em Português — Fine-tuning com Hugging Face Transformers

Projeto da Prova Substitutiva — Fase 4 (Machine Learning Engineering, FIAP).

Chatbot de perguntas e respostas em português, construído a partir de um
GPT-2 pré-treinado, ajustado (fine-tuned) com um dataset de instruções e
publicado como um playground interativo no Streamlit.

---

## Estratégia

- **Tema:** chatbot de perguntas e respostas em português.
- **Modelo pré-treinado:** [`pierreguillou/gpt2-small-portuguese`](https://huggingface.co/pierreguillou/gpt2-small-portuguese) — GPT-2 já adaptado para português, pequeno o suficiente para treinar sem GPU dedicada.
- **Dataset:** [`dominguesm/Canarim-Instruct-PTBR-Dataset`](https://huggingface.co/datasets/dominguesm/Canarim-Instruct-PTBR-Dataset), carregado direto do Hugging Face Hub — mais de 300 mil pares de instrução/resposta em português. Foi usada uma fatia de 3.000 exemplos (ajustável em `NUM_EXEMPLOS`, dentro de `finetune.py`).
- **Fine-tuning:** o modelo é ajustado nos pares `Pergunta: ... / Resposta: ...` usando a `Trainer` API do Hugging Face, por 3 épocas.
- **Geração:** o app Streamlit permite ajustar `temperature`, `top_p` e o tamanho máximo da resposta, para controlar o equilíbrio entre criatividade e coerência.
- **Modelo publicado:** o modelo ajustado está hospedado no Hugging Face Hub em [`gabifcavalheiro/chatbot-canarim-ptbr`](https://huggingface.co/gabifcavalheiro/chatbot-canarim-ptbr) — o `app.py` carrega diretamente de lá, o que permite rodar tanto localmente quanto no deploy do Streamlit Cloud sem depender de arquivos pesados no repositório.

---

## Estrutura do projeto

| Arquivo | O que faz |
|---|---|
| `finetune.py` | Roda uma vez: baixa o modelo base e o dataset, faz o fine-tuning, e salva o resultado localmente em `modelo-chatbot/`. |
| `publicar_modelo.py` | Publica o modelo salvo localmente no Hugging Face Hub. |
| `app.py` | Playground Streamlit: carrega o modelo do Hugging Face Hub e expõe a interface de perguntas e respostas. |
| `requirements.txt` | Dependências fixadas do projeto. |
| `avaliacao_qualitativa.md` / `.pdf` | Avaliação da qualidade das respostas geradas, incluindo exemplos, análise crítica e o efeito dos parâmetros de geração. |

---

## Como rodar localmente

### 1. Preparar o ambiente

Este projeto precisa de **Python 3.11 ou 3.12** (o ecossistema Hugging Face ainda não tem suporte estável a versões mais novas, como o 3.14).

Se ainda não tiver, instale em https://www.python.org/downloads/ — marque **"Add python.exe to PATH"** durante a instalação.

Crie e ative o ambiente virtual dentro da pasta do projeto:

```
py -3.12 -m venv venv
venv\Scripts\activate
```

(troque `3.12` por `3.11` se preferir essa versão)

Você deve ver `(venv)` no início da linha do terminal — isso confirma que o ambiente isolado está ativo.

### 2. Instalar as dependências

```
pip install -r requirements.txt
```

### 3. (Opcional) Treinar o modelo do zero

O repositório já usa o modelo publicado no Hugging Face Hub, então este passo **não é necessário** para rodar o app. Ele só é preciso se você quiser re-treinar ou ajustar os hiperparâmetros:

```
python finetune.py
```

Isso baixa o modelo base e o dataset, treina, e salva o resultado em `modelo-chatbot/` (pasta ignorada no `.gitignore`, por ser pesada demais para o GitHub).

Para publicar um novo modelo treinado no Hugging Face Hub:

```
python publicar_modelo.py
```

(exige uma conta no Hugging Face e um token de escrita — veja instruções dentro do próprio script)

### 4. Rodar o app

```
streamlit run app.py
```

---

## Avaliação

A avaliação completa — com exemplos de pergunta/resposta, análise de coerência, relevância e repetição, e o efeito prático dos parâmetros de geração (`temperature`, `top_p`, `repetition_penalty`) e de treino (`NUM_EXEMPLOS`, `NUM_EPOCHS`, `BLOCK_SIZE`) — está documentada em [`avaliacao_qualitativa.md`](./avaliacao_qualitativa.md) (também disponível em PDF).

**Resumo:** o modelo produz respostas coerentes e relevantes no início, mas tende a divagar em respostas longas, tem dificuldade em seguir instruções compostas ou formatos criativos específicos (como poemas), e é sensível à forma como a pergunta é escrita — perguntas curtas ou informais geram respostas piores do que a mesma pergunta formulada de maneira completa. Essas limitações são esperadas para um modelo pequeno (GPT-2 small) fine-tuned com um subconjunto reduzido do dataset. O melhor equilíbrio de parâmetros encontrado foi `temperature = 0.7`, `top_p = 0.9`, `repetition_penalty = 1.3`.

---

## Deploy

O app está publicado no Streamlit Community Cloud, conectado a este repositório e apontando para `app.py`.

Como o modelo é carregado diretamente do Hugging Face Hub (e não de uma pasta local), o deploy não depende de nenhum arquivo pesado versionado no GitHub.

---

## Entrega

- **Repositório GitHub:** https://github.com/gabicavalheiro/chatbot-canarium-huggingface
- **Repositório Hugging Face:** https://huggingface.co/gabifcavalheiro/chatbot-canarim-ptbr
- **App publicado (Streamlit):** https://chatbot-canarium-huggingface-dfrpfzkg2gf7yocox5vjz3.streamlit.app/
- **Vídeo (mín. 5 min):** https://drive.google.com/file/d/1v0oA5xky2RbPGgholL90auO4kyqwufeY/view?usp=sharing