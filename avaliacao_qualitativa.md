# Avaliação Qualitativa do Modelo Fine-tunado

Modelo: `pierreguillou/gpt2-small-portuguese` fine-tunado no dataset *dominguesm/Canarim-Instruct-PTBR-Dataset*.

---

## Exemplos de pergunta e resposta

### Exemplo 1

**Pergunta:** Descreva os efeitos do aquecimento global.

**Resposta:**

> O aquecimento global tem um efeito profundo sobre a vida humana, levando à pobreza e envelhecimento prematuras em todo o mundo e causando destruição de habitats naturais como desertos profundos e florestas tropicais profundas. Além disso, as mudanças climáticas podem causar uma série de eventos que incluem secas extremas, inundações repentinas no mundo inteiro, extinções das espécies endêmicas, interrupção ou diminuição da biodiversidade marinha. Além desses impactos negativos ambientais, também pode levar ao aumento dos preços mais baixos para produtos farmacêuticos feitos com dióxido de carbono na atmosfera e emissões industriais globais causadas por atividades humanas relacionadas às indústrias químicas artificiais usadas nos laboratórios químicos usados pelos seres humanos

**Avaliação:**

- **Relevância:** alta na primeira metade — o modelo lista corretamente consequências reais do aquecimento global (secas, inundações, perda de biodiversidade).
- **Coerência:** boa no início, mas se desfaz no final. A frase sobre "preços mais baixos para produtos farmacêuticos feitos com dióxido de carbono" é um non-sequitur — o modelo concatena termos que aparecem juntos estatisticamente no treino (indústria, química, emissões), mas sem lógica causal real.
- **Repetição:** usa "Além disso" duas vezes como conector, e repete a ideia de "profundo/profundas" — repetição de padrão discursivo, não de token exato (por isso o `repetition_penalty` não pega).
- **Resposta cortada:** termina sem ponto final — atingiu o limite de `max_new_tokens` no meio de uma frase.

---

### Exemplo 2

**Pergunta:** Escreva um poema curto sobre o outono.

**Resposta:**

> O inverno é como uma tempestade, trazendo ventos e tempestades constantes para os céus, mas nunca as deixa sem força física. O sol brilha em torno do horizonte brilhante, criando uma atmosfera de escuridão que se estende até ao mar. No verão, a primavera tem suas raízes no oceano profundo, iluminando todas as manhãs com sua majestosa luz exuberante. O verão traz chuvas mais fortes devido à combinação da abundância das ondas oceânicas e dos efeitos climáticos extremos associados às mudanças climáticas globais recentes. Além disso, o inverno pode ser descrito por muitas pessoas simplesmente observando-se muito bem na natureza, pois não importa o tipo

**Avaliação:**

- **Relevância:** baixa. A pergunta pede um poema sobre **outono**, mas o texto fala de inverno, verão e primavera — o outono nunca é mencionado. O modelo parece ter reconhecido "estação do ano" como tema geral, mas não amarrou na estação certa.
- **Formato:** não é um poema — é um parágrafo em prosa, sem quebras de verso, métrica ou rima. Isso mostra que o fine-tuning (focado em pergunta→resposta factual) não ensinou o modelo a produzir formatos criativos estruturados.
- **Coerência:** localmente as frases fazem sentido gramatical, mas a lógica entre elas é fraca (o texto "pula" de estação em estação sem transição clara).
- **Repetição:** usa "Além disso" de novo — mesmo conector do Exemplo 1, sugerindo que é uma muleta discursiva aprendida do dataset.

---

### Exemplo 3

**Pergunta:** Quais são as vantagens e desvantagens do trabalho remoto?

**Resposta:**

> A vantagem das tarefas de trabalho remota é que os empregadores podem trabalhar com um número limitado de pessoas, permitindo aos trabalhadores trabalharem juntos em uma única empresa. Isso permite a flexibilidade para contratar mais assistentes qualificados, reduzir custos associados ao emprego e fornecer serviços personalizados eficazes. Além disso, o trabalho on-line pode proporcionar às empresas maior eficiência econômica e produtividade nas suas operações diárias devido à sua enorme capacidade técnica e financeira dos funcionários regulares. Além disso, tornando possível conexões entre membros da equipe por meio de conversas diretas ou online fornece melhores oportunidades lucrativas no local de trabalho. Além disso, tem sido descrito como essencial

**Avaliação:**

- **Relevância:** parcial. A resposta cobre bem as **vantagens** (custo, flexibilidade, produtividade), mas ignora completamente a parte de **desvantagens** pedida na pergunta — sinal de que o modelo pequeno tem dificuldade em atender perguntas com múltiplas partes.
- **Coerência:** razoável frase a frase, mas alguns trechos soam redundantes entre si (repete a ideia de "eficiência/produtividade" de formas diferentes, sem acrescentar informação nova).
- **Repetição:** o conector "Além disso" aparece **três vezes** nesta resposta — o exemplo mais claro de repetição estrutural entre os três testes.
- **Resposta cortada:** termina em "tem sido descrito como essencial", interrompida pelo limite de tokens.

---

### Exemplo 4 — Sensibilidade à formulação da pergunta

**Pergunta:** o que é ia

**Resposta:**

> e é equivalente à soma de todos os divisores e retorna a mediana total? O que é preciso usar um algoritmo eficiente? A definição mais precisa do algoritmo seria como uma função matemática, onde cada elemento em um conjunto pode ser dividido por outro elemento na mesma matriz. Esta abordagem economiza muito tempo no aprendizado de máquina devido ao custo associado com as etapas iniciais da computação. Por exemplo, se você aprende um algoritmo para encontrar as raízes das árvores usando apenas dois passos, então você precisará gastar milhões de dólares adicionais antes que ele seja concluído.

**Avaliação:**

- **Relevância:** nula. A resposta não tem nenhuma relação com "o que é IA" — o modelo divaga para um território aleatório envolvendo divisores, mediana e custo computacional, sem retomar o tema da pergunta em nenhum momento.
- **Coerência:** localmente as frases são gramaticais, mas a sequência como um todo não segue lógica alguma — é o exemplo mais claramente "quebrado" entre todos os testados.
- **Comparação reveladora:** a mesma pergunta, feita de forma completa ("O que é inteligência artificial?", ver seção de temperature acima), gerou uma resposta coerente e no tema com `temperature=0.3`. Já a versão curta e abreviada ("o que é ia") — sem pontuação, sem maiúscula, usando sigla — não deu ao modelo "sinal" suficiente para ancorar a geração no tópico certo.
- **Implicação:** o modelo é sensível à formulação exata da pergunta, não só ao tema. Isso é uma limitação relevante de modelos pequenos fine-tuned com poucos exemplos: eles generalizam mal para variações de fraseado (abreviações, informalidade, falta de pontuação) que um humano interpretaria sem problema.

---

## Padrões observados nos quatro exemplos

| Aspecto | Observação |
|---|---|
| Coerência sintática | Boa — frases individualmente bem formadas em português |
| Coerência semântica/lógica | Se degrada conforme a resposta cresce; tende a divagar após 2–3 frases |
| Relevância ao tema | Forte no início da resposta, enfraquece no final (ou ausente, quando a pergunta é curta demais) |
| Seguimento de formato (ex: poema) | Fraco — o modelo não distingue bem "responder" de "criar em formato específico" |
| Seguimento de instruções compostas (ex: "vantagens e desvantagens") | Fraco — tende a responder só uma parte |
| Repetição | Não é repetição de palavras exatas (o `repetition_penalty` resolve isso), mas repetição de conectores/estrutura discursiva ("Além disso" aparece em vários exemplos) |
| Sensibilidade à formulação | Alta — perguntas curtas, abreviadas ou sem pontuação (ex: "o que é ia") produzem respostas muito piores do que a mesma pergunta escrita de forma completa |

Isso é consistente com as limitações esperadas de um modelo pequeno (GPT-2 small) fine-tunado com um subconjunto do dataset e poucas épocas: ele aprendeu bem o *estilo* de resposta expositiva em português, mas não desenvolveu raciocínio robusto o suficiente para manter coerência em textos longos ou seguir instruções com múltiplas exigências.

---

## Parâmetros de geração usados neste teste

| Parâmetro | Valor | Por quê |
|---|---|---|
| `temperature` | 0.7 | Equilíbrio entre determinismo e diversidade. Valores muito baixos (ex: 0.2) fariam o modelo pequeno cair em loops repetitivos; valores muito altos (ex: 1.2+) gerariam texto mais desconexo. 0.7 é um meio-termo comum para geração de texto legível. |
| `top_p` | 0.9 | Nucleus sampling: a cada token, o modelo só considera o menor conjunto de palavras cuja probabilidade acumulada atinge 90%. Isso corta as opções muito improváveis/estranhas, sem restringir demais a variedade. |
| `repetition_penalty` | 1.3 | Penaliza tokens que já apareceram na resposta, reduzindo a repetição literal de palavras — um problema comum em modelos pequenos como o GPT-2. Nos testes, isso evitou repetição de palavras exatas, mas não impediu a repetição de conectores como "Além disso" (tokens diferentes a cada uso, então a penalidade não os pega). |
| `max_new_tokens` | 120 | Limite de tamanho da resposta. Escolhido para permitir respostas completas sem deixar o modelo divagar por tempo demais — mas os testes mostram que mesmo dentro desse limite a coerência já começa a cair perto do final. |

---

## Hiperparâmetros de fine-tuning (`finetune.py`)

| Parâmetro | Valor | Por quê |
|---|---|---|
| `NUM_EXEMPLOS` | 3.000 | O dataset completo tem mais de 316 mil exemplos. Usar uma fatia de 3.000 reduziu drasticamente o tempo de treinamento, viável para rodar em hardware doméstico dentro do prazo do projeto — às custas de o modelo ver uma variedade menor de instruções. |
| `NUM_EPOCHS` | 3 | Com um dataset pequeno (3.000 exemplos) e um modelo pequeno (GPT-2 small), 3 épocas foram suficientes para o modelo aprender o padrão "Pergunta: ... / Resposta: ..." sem gastar tempo de treino excessivo. Mais épocas em um dataset tão pequeno aumentaria o risco de overfitting (o modelo "decorar" respostas específicas em vez de generalizar). |
| `BLOCK_SIZE` | 128 | Tamanho dos blocos de tokens usados no treinamento. Um valor menor treina mais rápido e usa menos memória, mas limita o quanto de contexto (pergunta + resposta) cabe em uma única sequência de treino — o que pode explicar por que o modelo tem dificuldade com perguntas compostas. |
| `per_device_train_batch_size` | 2 | Batch pequeno, provavelmente limitado pela memória disponível na máquina local (sem GPU dedicada de alta capacidade). Batches pequenos tornam o treino mais lento, mas viabilizam rodar em hardware limitado. |

---

## Efeito da temperature (pergunta fixa)

**Pergunta:** O que é inteligência artificial?

| temperature | Resposta gerada |
|---|---|
| 0.3 (baixa) | Inteligência Artificial (IA) é um ramo da ciência de computação e tecnologia responsável por projetar, analisar e interpretar dados em uma forma humana. É usado para automatizar tarefas complexas como análise de linguagem natural ou previsão preditiva. É também usada na automação industrial, onde os robôs podem ser usados para processar grandes quantidades de dados sem a necessidade do uso humano. A IA pode aprender com as máquinas mais rapidamente ao detectar padrões complexos no texto dado e prever o comportamento dos seres humanos através das redes neurais artificiais usadas nas indústrias. |
| 1.3 (alta) | A IA (IA), na verdade, estuda o comportamento humano e inclui as habilidades do homem para extrair significado de dados sem se preocupar com suposições. A IA pode aprender desde muito antes da máquina humana usar seu conhecimento direto em mecanismos específicos programados até porque ela utiliza sua capacidade preditiva e julgamento inteligente e seus algoritmos sofisticados a fim de descobrir e resolvê-los rapidamente, obtendo sinais codificados por análise cladística e registros biológicos associados ao processo de colheita. |

**Avaliação:**

- **temperature = 0.3:** resposta mais "segura" e coerente — se mantém no tema (definição de IA, automação industrial, redes neurais) do início ao fim, com vocabulário consistente e frases bem formadas. É a resposta mais próxima de um texto enciclopédico correto.
- **temperature = 1.3:** começa de forma plausível, mas rapidamente introduz termos fora de contexto e sem relação real com IA — "análise cladística" (um conceito de biologia evolutiva) e "processo de colheita" aparecem sem nexo com a pergunta. O texto soa mais "criativo"/variado lexicalmente, mas à custa de coerência e precisão.
- **Confirma a expectativa teórica:** temperature baixa = mais previsível e correto; temperature alta = mais variação, com risco real de sair do assunto — exatamente o que se observou aqui.

---

## Conclusão

O modelo produziu respostas coerentes e relevantes no início, mas tendendo a genéricas ou levemente repetitivas conforme a resposta cresce, para perguntas gerais dentro de temas cobertos pela Wikipedia (o corpus de pré-treinamento). Não é confiável para fatos específicos ou perguntas compostas, já que é um modelo pequeno (GPT-2 small) fine-tuned com apenas 3.000 exemplos.

O parâmetro que teve maior impacto perceptível foi a `temperature` — a diferença entre 0.3 e 1.3 na mesma pergunta foi nítida, alterando tanto a coerência quanto a fidelidade ao tema. O `repetition_penalty` teve impacto mais sutil: evitou repetição literal de palavras, mas não impediu a repetição de padrões discursivos (como o conector "Além disso", recorrente em várias respostas).

O melhor equilíbrio encontrado foi **temperature = 0.7, top_p = 0.9, repetition_penalty = 1.3** — parâmetros que geram respostas fluentes, majoritariamente coerentes e sem repetição literal, mantendo alguma naturalidade sem cair nem no extremo "engessado" (temperature muito baixa) nem no extremo "divagante" (temperature muito alta).

O fine-tuning foi bem-sucedido em ensinar o modelo a responder no formato esperado (Pergunta/Resposta) e a produzir português fluente e gramaticalmente correto. As limitações observadas — divagação em respostas longas, dificuldade com instruções compostas, e não seguir formatos criativos como poemas — são coerentes com as escolhas feitas para viabilizar o projeto no prazo disponível (modelo pequeno, subconjunto de 3.000 exemplos, poucas épocas). Um treinamento com mais exemplos, mais épocas e/ou um modelo base maior tenderia a reduzir esses problemas, ao custo de mais tempo e recursos computacionais.
