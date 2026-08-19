# SAST2026-FuzzingMQTT

Pacote experimental para avaliação de ferramentas de fuzzing MQTT aplicadas ao Home Assistant, com uso de teste de mutação para medir a efetividade observável dos fuzzers na detecção de comportamentos incorretos introduzidos artificialmente no código do sistema alvo.

Este repositório foi organizado para apoiar a reprodução do experimento descrito no artigo submetido ao SAST/CBSoft 2026.

---

## 1. Objetivo do experimento

O objetivo do experimento é comparar ferramentas de fuzzing MQTT quanto à sua capacidade de revelar mutantes inseridos em módulos do Home Assistant relacionados ao processamento de mensagens MQTT.

Diferentemente de uma avaliação tradicional de suíte de testes unitários, os “casos de teste” deste estudo são campanhas de fuzzing e corpora de mensagens MQTT. Cada fuzzer gera entradas, essas entradas são normalizadas ou reproduzidas por um harness, e o comportamento do Home Assistant original é comparado ao comportamento do Home Assistant mutado.

A métrica principal é o `mutation score`, calculado como:

```text
Mutation Score = mutantes mortos / mutantes totais
```

Um mutante é considerado morto quando o replay do corpus produz uma divergência observável em relação ao baseline do Home Assistant original.

Neste pacote, os resultados principais são reportados no espaço de mutação observado relacionado ao cenário MQTT. Esse recorte evita interpretar como falha dos fuzzers mutantes que não foram efetivamente exercitados ou observados pelo cenário MQTT configurado.

---

## 2. Arquitetura experimental

O ambiente é composto por:

* Home Assistant executado em container Docker;
* broker MQTT Mosquitto;
* fuzzers MQTT;
* harness de integração;
* replayers semânticos;
* ferramenta de mutação `mutmut`;
* oráculo de trace baseado no estado observado via API do Home Assistant.

Fluxo simplificado:

```text
Fuzzer / Corpus
      ↓
Replayer semântico
      ↓
Broker MQTT
      ↓
Home Assistant original ou mutado
      ↓
API de estado do Home Assistant
      ↓
Trace observado
      ↓
Comparação com baseline
      ↓
Mutante morto ou sobrevivente
```

---

## 3. Fuzzers avaliados

As campanhas principais consideram:

| Fuzzer  | Papel no experimento                                    |
| ------- | ------------------------------------------------------- |
| BooFuzz | Fuzzer baseado em geração estruturada de entradas       |
| FUME    | Fuzzer MQTT especializado                               |
| Scapy   | Baseline programável para geração/envio de pacotes MQTT |

Outras ferramentas podem aparecer em scripts, diretórios locais ou resultados exploratórios, mas as campanhas principais e os resultados reportados neste pacote priorizam os fuzzers com corpus válido e reprodutível: BooFuzz, FUME e Scapy.

---

## 4. Módulos avaliados

Os módulos principais analisados foram selecionados de acordo com sua atingibilidade pelo fluxo MQTT e sua relação com pontos críticos do processamento de mensagens no Home Assistant.

| Módulo                                    | Frente experimental  | Interpretação                                                                                   |
| ----------------------------------------- | -------------------- | ----------------------------------------------------------------------------------------------- |
| `homeassistant/components/mqtt/sensor.py` | Entidade MQTT sensor | Processamento de payload, conversão de valor, expiração/disponibilidade e atualização de estado |
| `homeassistant/helpers/template.py`       | Template/Jinja2      | Transformação indireta de payload via `value_template`                                          |

O módulo `sensor.py` tem relação direta com o fluxo MQTT, pois processa mensagens recebidas em um tópico monitorado e atualiza o estado da entidade observada. O módulo `template.py` tem relação indireta com MQTT, pois é usado pelo Home Assistant para interpretar e transformar payloads por meio de templates, como `value_template`.

Outros módulos MQTT-related foram considerados durante a fase exploratória, mas não fazem parte dos resultados principais disponibilizados neste pacote de replicação.

---

## 5. Estrutura do repositório

```text
.
├── README.md
├── harness/
│   ├── adapters/                 # Adaptadores e replayers semânticos
│   ├── analysis/                 # Scripts de análise, classificação e tabelas
│   ├── config/                   # Arquivo de configuração de exemplo
│   ├── corpus/                   # Scripts de coleta e baseline semântico
│   └── coverage/                 # Instrumentação auxiliar de cobertura
├── artifact/
│   ├── data/
│   │   ├── corpus/               # Corpora finais usados no replay
│   │   └── baselines_semantic/   # Traces baseline do Home Assistant original
│   ├── mutation/
│   │   └── mqtt_observed_space/  # IDs de mutantes do espaço MQTT-observado
│   └── results/
│       ├── posthoc_mqtt_final/   # Classificação post-hoc e tabelas finais
│       └── repeated_baseline_replay/ # Controle de estabilidade do replay
└── harness/config/experimento.example.env
```

Diretórios locais que não devem ser versionados integralmente:

```text
ha_source/
ha_config/
venv/
venv_*/
resultados_mutmut/
resultados/
backups_resultados/
.mutmut-cache/
mutants/
harness/config/experimento.env
harness/config/secrets.env
FUME-Fuzzing-MQTT-Brokers/
MQTTGRAM/
SGANFuzz/
```

---

## 6. Requisitos

Ambiente recomendado:

* Ubuntu via WSL ou Linux nativo;
* Docker;
* Python 3.12;
* Git;
* Mosquitto clients;
* Home Assistant em container;
* broker MQTT Mosquitto.

Versões usadas no experimento original:

| Componente        | Versão          |
| ----------------- | --------------- |
| Home Assistant    | `2024.6.0`      |
| Eclipse Mosquitto | `2.1.2`         |
| Python            | `3.12`          |
| Mutation tool     | `mutmut==2.5.1` |

Instalação básica no Ubuntu/WSL:

```bash
sudo apt update
sudo apt install -y \
  git curl wget nano jq \
  python3 python3-venv python3-pip \
  mosquitto-clients build-essential
```

Criação do ambiente Python:

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

A versão recomendada do `mutmut` é:

```text
mutmut==2.5.1
```

Essa versão foi usada porque permite executar o modelo black-box do experimento via `--paths-to-mutate` e `--runner`.

---

## 7. Preparação do Home Assistant

O código-fonte do Home Assistant não é versionado neste repositório. Ele deve ser clonado separadamente na pasta `ha_source/`:

```bash
git clone https://github.com/home-assistant/core.git ha_source
cd ha_source
git checkout 2024.6.0
cd ..
```

O container do Home Assistant deve montar o código-fonte local:

```text
-v /home/darla/experimento/ha_source/homeassistant:/usr/src/homeassistant/homeassistant
```

Essa montagem é essencial: o `mutmut` altera arquivos no host e o container executa o código mutado.

A configuração local do Home Assistant deve conter uma entidade MQTT sensor compatível com o tópico usado no experimento:

```text
homeassistant/sensor/temp
```

A entidade observada no experimento foi:

```text
sensor.sensor_fuzzing
```

---

## 8. Configuração do experimento

Copie o arquivo de exemplo:

```bash
cp harness/config/experimento.example.env harness/config/experimento.env
nano harness/config/experimento.env
```

Exemplo de configuração:

```bash
export EXP_ROOT="/home/darla/experimento"

export HA_CONTAINER="ha-test"
export HA_BASE_URL="http://127.0.0.1:8123"
export HA_TOKEN="CHANGE_ME"
export HA_ENTITY_ID="sensor.sensor_fuzzing"

export MQTT_HOST="127.0.0.1"
export MQTT_PORT="1883"
export MQTT_TOPIC="homeassistant/sensor/temp"
export MQTT_PAYLOAD='{"temperature": 22.5}'

export BASELINE_FILE="$EXP_ROOT/baseline.json"
export RESULTS_DIR="$EXP_ROOT/resultados_mutmut"

# Use 60 for quick debugging and 86400 for the 24h campaign.
export FUZZ_DURATION=60
export FUZZ_SEED=1
export MAX_PAYLOADS=1000

export REPLAY_LIMIT=1000
export REPLAY_DELAY=0.02
export RESET_PAYLOAD='{"temperature": 22.5}'

export CHECK_CORPUS_TRACE=1
export CHECK_STATE_DURING_FUZZ=0
export CHECK_STATE_AFTER_FUZZ=0
export RESTORE_CANARY_BEFORE_STATE_CHECK=1
export STATE_SETTLE_SECONDS=3
export ORACLE_LOG_PATTERNS="__PADRAO_QUE_NUNCA_APARECE__"
```

Carregue as variáveis:

```bash
source harness/config/experimento.env
```

Teste a API do Home Assistant:

```bash
curl -s \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  "$HA_BASE_URL/api/states/$HA_ENTITY_ID" | jq
```

Teste a publicação MQTT:

```bash
mosquitto_pub -h "$MQTT_HOST" -p "$MQTT_PORT" \
  -t "$MQTT_TOPIC" \
  -m '{"temperature": 22.5}'
```

Para verificar a recepção no broker, use um subscriber em outro terminal:

```bash
mosquitto_sub -h "$MQTT_HOST" -p "$MQTT_PORT" \
  -t "$MQTT_TOPIC" -v
```

---

## 9. Execução das campanhas

O fluxo recomendado para cada módulo é:

1. coletar ou reutilizar corpus do fuzzer;
2. gerar baseline semântico no Home Assistant original;
3. executar `mutmut` no arquivo alvo;
4. replayar o corpus para cada mutante;
5. comparar trace original e trace mutado;
6. salvar resultados para análise posterior.

Exemplo conceitual para `sensor.py`:

```bash
source venv/bin/activate
source harness/config/experimento.env

./harness/run_sensor_campaign.sh scapy \
  /home/darla/experimento/harness/adapters/run_replay_sensor_corpus_semantic.py \
  1
```

O comando principal do `mutmut` segue o modelo:

```bash
mutmut run \
  --paths-to-mutate "$TARGET_FILE" \
  --runner "python -m unittest harness/test_harness_unificado.py"
```

O pacote também inclui scripts auxiliares em `harness/analysis/` para:

* construir o espaço de mutantes MQTT-observado;
* calcular mutantes mortos por campanha;
* classificar sobreviventes no post-hoc;
* gerar tabela LaTeX;
* executar o controle de baseline repetido;
* calcular scores ajustados por cobertura/atingibilidade.

---

## 10. Artefatos disponibilizados

Os resultados brutos completos das campanhas locais ficam em:

```text
resultados_mutmut/
```

Esse diretório não deve ser versionado integralmente, pois contém caches, logs e arquivos potencialmente grandes.

Para publicação acadêmica, os artefatos consolidados foram copiados para:

```text
artifact/
```

Principais artefatos versionados:

```text
artifact/data/corpus/sensor/
artifact/data/baselines_semantic/sensor/
artifact/mutation/mqtt_observed_space/
artifact/results/posthoc_mqtt_final/
artifact/results/repeated_baseline_replay/
```

Arquivos importantes:

| Arquivo                                                        | Conteúdo                                       |
| -------------------------------------------------------------- | ---------------------------------------------- |
| `artifact/mutation/mqtt_observed_space/sensor_ids.txt`         | IDs dos mutantes MQTT-related em `sensor.py`   |
| `artifact/mutation/mqtt_observed_space/template_ids.txt`       | IDs dos mutantes MQTT-related em `template.py` |
| `artifact/results/posthoc_mqtt_final/posthoc_mqtt_summary.csv` | Resumo da classificação post-hoc               |
| `artifact/results/posthoc_mqtt_final/tabela_posthoc_mqtt.tex`  | Tabela LaTeX usada no artigo                   |
| `artifact/results/repeated_baseline_replay/summary.csv`        | Resultado do controle de baseline repetido     |

---

## 11. Resultados principais

O espaço de mutação observado relacionado ao MQTT contém:

| Módulo        | Total bruto de mutantes | Mutantes MQTT-related |
| ------------- | ----------------------: | --------------------: |
| `sensor.py`   |                     126 |                    59 |
| `template.py` |                    1452 |                   602 |

Resultados ajustados ao espaço MQTT-observado:

| Módulo        | Fuzzer  | Mutantes MQTT-related | Mutantes mortos | MQTT-adjusted mutation score |
| ------------- | ------- | --------------------: | --------------: | ---------------------------: |
| `sensor.py`   | BooFuzz |                    59 |              17 |                       28.81% |
| `sensor.py`   | FUME    |                    59 |              19 |                       32.20% |
| `sensor.py`   | Scapy   |                    59 |              17 |                       28.81% |
| `template.py` | BooFuzz |                   602 |             127 |                       21.10% |
| `template.py` | FUME    |                   602 |             127 |                       21.10% |
| `template.py` | Scapy   |                   602 |             127 |                       21.10% |

O score ajustado é calculado como:

```text
MQTT-adjusted mutation score = mutantes mortos no espaço MQTT / mutantes MQTT-related
```

Exemplos:

```text
FUME em sensor.py = 19 / 59 = 32.20%
BooFuzz em sensor.py = 17 / 59 = 28.81%
Scapy em sensor.py = 17 / 59 = 28.81%

Cada fuzzer em template.py = 127 / 602 = 21.10%
```

Esses resultados devem ser interpretados como efetividade observável dentro do cenário MQTT configurado, e não como uma medida absoluta da qualidade geral de cada fuzzer.

---

## 12. Classificação post-hoc dos mutantes MQTT-related

Foi realizada uma classificação post-hoc para interpretar os mutantes MQTT-related mortos e sobreviventes.

Categorias usadas em `sensor.py`:

| Categoria | Interpretação                                    |
| --------- | ------------------------------------------------ |
| `K1`      | Mutante morto por divergência na trace semântica |
| `S1`      | Disponibilidade/expiração MQTT                   |
| `S2`      | Processamento de payload/template MQTT           |
| `S3`      | Atualização de estado MQTT                       |
| `S4`      | Tópico/subscrição MQTT                           |
| `S5`      | Schema/configuração MQTT                         |

Categorias usadas em `template.py`:

| Categoria | Interpretação                                                   |
| --------- | --------------------------------------------------------------- |
| `K1`      | Mutante morto por divergência na trace semântica                |
| `T1`      | Renderização/interpretação de `value_template`                  |
| `T2`      | Infraestrutura de template potencialmente usada pelo fluxo MQTT |

Resumo final:

| Classe                                    | `sensor.py` | `template.py` |
| ----------------------------------------- | ----------: | ------------: |
| K1: killed by semantic trace              |          19 |           127 |
| S1: MQTT availability/expiration          |          34 |             0 |
| S2: MQTT payload/template handling        |           5 |             0 |
| S3: MQTT state update                     |           1 |             0 |
| T1: value-template rendering/interpreting |           0 |           475 |
| Total MQTT-related mutants                |          59 |           602 |

A tabela LaTeX correspondente está disponível em:

```text
artifact/results/posthoc_mqtt_final/tabela_posthoc_mqtt.tex
```

---

## 13. Controle de baseline repetido

Além do controle NOOP, foi executado um controle de baseline repetido para avaliar a estabilidade do oráculo sob condições reais de replay.

Nesse controle, cada corpus válido foi replayado cinco vezes contra o Home Assistant original, sem mutantes. Antes de cada repetição, o container do Home Assistant foi reiniciado. As traces semânticas produzidas pelo mesmo corpus foram comparadas usando hash normalizado.

Resultado:

| Corpus  | Replays | Trace length | Unique hashes | Result |
| ------- | ------: | -----------: | ------------: | ------ |
| BooFuzz |       5 |           11 |             1 | stable |
| FUME    |       5 |          205 |             1 | stable |
| Scapy   |       5 |          711 |             1 | stable |

Esse resultado indica que o oráculo semântico foi estável sob replay real dos corpora, reduzindo a probabilidade de que mutantes mortos tenham sido causados por comportamento não determinístico do replay.

Os arquivos correspondentes estão disponíveis em:

```text
artifact/results/repeated_baseline_replay/
```

---

## 14. Interpretação dos resultados

Um mutante morto indica que o corpus/replayer produziu um comportamento observável diferente do baseline original.

Um mutante sobrevivente pode indicar:

* mutante equivalente;
* trecho não atingido pelo fluxo MQTT configurado;
* baixa sensibilidade do corpus;
* efeito não observável no estado monitorado;
* limitação do oráculo de trace;
* necessidade de configurações MQTT mais diversas;
* necessidade de oráculos temporais ou comportamentais mais fortes.

Assim, o mutation score deve ser interpretado como efetividade observável do fuzzer no cenário experimental, não como prova absoluta de ausência de defeitos.

---

## 15. Limitações

Este experimento depende fortemente de atingibilidade e observabilidade. Alguns mutantes podem estar em código relacionado ao MQTT, mas ainda assim não produzir alteração observável no estado da entidade monitorada. Nesses casos, mutantes sobreviventes são relevantes para a discussão metodológica, pois indicam limites do oráculo e do desenho experimental.

Também não foi realizada uma comparação direta entre os corpora derivados dos fuzzers e a suíte de testes convencional do Home Assistant no mesmo conjunto de mutantes. Portanto, a força absoluta dos mutation scores obtidos deve ser interpretada com cautela. Os resultados devem ser lidos principalmente como uma comparação entre fuzzers MQTT sob o mesmo harness, estratégia de replay e oráculo semântico.

---

## 16. Como reproduzir rapidamente

```bash
git clone https://github.com/darlagalves/SAST2026-FuzzingMQTT.git
cd SAST2026-FuzzingMQTT

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

cp harness/config/experimento.example.env harness/config/experimento.env
nano harness/config/experimento.env
```

Depois configure:

1. `ha_source/` com o código-fonte do Home Assistant `2024.6.0`;
2. `ha_config/` com a configuração da entidade MQTT;
3. container `ha-test` com volume apontando para `ha_source/`;
4. broker Mosquitto;
5. token do Home Assistant em `harness/config/experimento.env`.

Carregue a configuração:

```bash
source harness/config/experimento.env
```

Teste o broker:

```bash
mosquitto_sub -h "$MQTT_HOST" -p "$MQTT_PORT" \
  -t "$MQTT_TOPIC" -C 1 -v &
sleep 1
mosquitto_pub -h "$MQTT_HOST" -p "$MQTT_PORT" \
  -t "$MQTT_TOPIC" \
  -m '{"temperature": 22.5}'
```

Teste a API do Home Assistant:

```bash
curl -s \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  "$HA_BASE_URL/api/states/$HA_ENTITY_ID" | jq
```

---

## 17. Reproduzir análise post-hoc

Com os artefatos já versionados, a classificação post-hoc pode ser reproduzida a partir dos IDs MQTT-related:

```bash
python harness/analysis/posthoc_mqtt_classification.py \
  --sensor-dir resultados_mutmut/sensor \
  --template-dir resultados_mutmut/template \
  --sensor-ids artifact/mutation/mqtt_observed_space/sensor_ids.txt \
  --template-ids artifact/mutation/mqtt_observed_space/template_ids.txt \
  --seed 1 \
  --sensor-total 126 \
  --template-total 1452 \
  --fuzzers boofuzz fume scapy
```

Caso os resultados brutos completos não estejam disponíveis localmente, consulte os resultados consolidados já versionados em:

```text
artifact/results/posthoc_mqtt_final/
```

---

## 18. Reproduzir controle de baseline repetido

O controle de baseline repetido pode ser executado com:

```bash
SEED=1 \
REPETITIONS=5 \
REPLAY_LIMIT=1000 \
REPLAY_DELAY=0.02 \
./harness/analysis/run_repeated_baseline_replay.sh
```

Os resultados consolidados usados no artigo estão disponíveis em:

```text
artifact/results/repeated_baseline_replay/summary.csv
```

---

## 19. Licença

Definir licença antes da submissão pública.

Sugestão:

* MIT para scripts próprios deste repositório;
* manter respeito às licenças do Home Assistant e das ferramentas externas utilizadas;
* não redistribuir ferramentas externas ou cópias completas de repositórios de terceiros sem verificar suas respectivas licenças.

---

## 20. Citação

Se este pacote for utilizado, cite o artigo correspondente submetido ao SAST/CBSoft 2026 e referencie este repositório como pacote de replicação experimental.
