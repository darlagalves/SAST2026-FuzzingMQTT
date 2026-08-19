# SAST2026-FuzzingMQTT

Pacote experimental para avaliação de ferramentas de fuzzing MQTT aplicadas ao Home Assistant, com uso de teste de mutação para medir a efetividade observável dos fuzzers na detecção de comportamentos incorretos introduzidos artificialmente no código do sistema alvo.

Este repositório foi organizado para apoiar a reprodução do experimento descrito no artigo submetido ao SAST/CBSoft 2026.

---

## 1. Objetivo do experimento

O objetivo do experimento é comparar ferramentas de fuzzing MQTT quanto à sua capacidade de revelar mutantes inseridos em módulos do Home Assistant relacionados ao processamento de mensagens MQTT.

Diferentemente de uma avaliação tradicional de suíte de testes unitários, os “casos de teste” deste estudo são campanhas de fuzzing e corpus de mensagens MQTT. Cada fuzzer gera entradas, essas entradas são normalizadas ou reproduzidas por um harness, e o comportamento do Home Assistant original é comparado ao comportamento do Home Assistant mutado.

A métrica principal é o `mutation score`, calculado como:

```text
Mutation Score = mutantes mortos / mutantes totais
```

Um mutante é considerado morto quando o replay do corpus produz divergência observável em relação ao baseline do Home Assistant original.

---

## 2. Arquitetura experimental

O ambiente é composto por:

- Home Assistant executado em container Docker;
- broker MQTT Mosquitto;
- fuzzers MQTT;
- harness de integração;
- replayers semânticos;
- ferramenta de mutação `mutmut`;
- oráculo de trace baseado no estado observado via API do Home Assistant.

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

| Fuzzer | Papel no experimento |
|---|---|
| BooFuzz | Fuzzer baseado em geração estruturada de entradas |
| FUME | Fuzzer MQTT especializado |
| Scapy | Baseline programável para geração/envio de pacotes MQTT |

Outras ferramentas podem aparecer em scripts ou resultados exploratórios, mas as campanhas principais devem priorizar os fuzzers com corpus válido e reprodutível.

---

## 4. Módulos avaliados

Os módulos analisados foram selecionados de acordo com sua atingibilidade pelo fluxo MQTT e sua relação com pontos críticos do processamento de mensagens no Home Assistant.

| Módulo | Frente experimental | Interpretação |
|---|---|---|
| `homeassistant/components/mqtt/sensor.py` | Entidade MQTT sensor | Processamento de payload, conversão de valor e atualização de estado |
| `homeassistant/helpers/template.py` | Template/Jinja2 | Transformação de payload via `value_template` |
| `homeassistant/util/json.py` | Parsing JSON | Frente exploratória sobre payloads JSON válidos, inválidos e malformados |
| `homeassistant/components/mqtt/switch.py` | Entidade discreta | Frente exploratória sobre estados `on`/`off` |
| `homeassistant/components/mqtt/subscription.py` | Subscrições MQTT | Frente exploratória sobre gerenciamento de tópicos inscritos |
| `homeassistant/components/mqtt/mixins.py` | Camada comum de entidades MQTT | Frente candidata para avaliar comportamento compartilhado entre entidades |

Os resultados principais do artigo devem priorizar os módulos nos quais o oráculo observou divergências efetivas. Módulos com mutation score igual a zero são mantidos como evidência experimental de baixa observabilidade ou baixa atingibilidade no cenário configurado.

---

## 5. Estrutura recomendada do repositório

```text
.
├── README.md
├── requirements.txt
├── harness/
│   ├── adapters/                 # Adaptadores e replayers semânticos
│   ├── analysis/                 # Scripts de sumarização, tabelas e gráficos
│   ├── config/                   # Configuração de exemplo
│   └── test_harness_unificado.py # Harness/oráculo principal
├── configs_mutmut/               # Configurações auxiliares do mutmut
├── data/
│   └── corpus/                   # Corpus selecionado usado nas campanhas
├── docs/                         # Documentação complementar do protocolo
└── results/
    ├── processed/                # CSVs consolidados
    ├── raw_summaries/            # Resumos textuais das campanhas
    ├── figures/                  # Gráficos gerados
    └── tables/                   # Tabelas em LaTeX
```

Diretórios locais que não devem ser versionados:

```text
ha_source/
ha_config/
venv/
resultados_mutmut/
.mutmut-cache/
mutants/
harness/config/experimento.env
FUME-Fuzzing-MQTT-Brokers/
MQTTGRAM/
```

---

## 6. Requisitos

Ambiente recomendado:

- Ubuntu via WSL ou Linux nativo;
- Docker;
- Python 3.10+;
- Git;
- Mosquitto clients;
- Home Assistant em container;
- broker MQTT Mosquitto.

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

Versão recomendada do `mutmut`:

```text
mutmut==2.5.1
```

Essa versão é usada porque permite executar o modelo black-box do experimento via `--paths-to-mutate` e `--runner`.

---

## 7. Preparação do Home Assistant

O código-fonte do Home Assistant não é versionado neste repositório. Ele deve ser clonado separadamente na pasta `ha_source/`:

```bash
git clone https://github.com/home-assistant/core.git ha_source
```

Recomenda-se usar a mesma versão/tag do Home Assistant utilizada na campanha original.

O container do Home Assistant deve montar o código-fonte local:

```text
-v /home/darla/experimento/ha_source/homeassistant:/usr/src/homeassistant/homeassistant
```

Essa montagem é essencial: o `mutmut` altera arquivos no host e o container executa o código mutado.

---

## 8. Configuração do experimento

Copie o arquivo de exemplo:

```bash
cp harness/config/experimento.env.example harness/config/experimento.env
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

export FUZZ_DURATION=60
export REPLAY_LIMIT=100
export REPLAY_DELAY=0.05
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

---

## 9. Execução das campanhas

O fluxo recomendado para cada módulo é:

1. coletar ou reutilizar corpus do fuzzer;
2. gerar baseline semântico no Home Assistant original;
3. executar `mutmut` no arquivo alvo;
4. replayar o corpus para cada mutante;
5. comparar trace original e trace mutado;
6. salvar resultados para análise posterior.

Exemplo conceitual:

```bash
source venv/bin/activate
source harness/config/experimento.env

./harness/run_sensor_campaign.sh scapy \
  /home/darla/experimento/harness/adapters/run_replay_sensor_corpus_semantic.py \
  1
```

Para scripts sequenciais por módulo, ajuste as variáveis:

```bash
MODULE_NAME="nome_do_modulo"
TARGET_FILE="ha_source/homeassistant/caminho/do/arquivo.py"
TARGET_REL="homeassistant/caminho/do/arquivo.py"
REPLAYER="/home/darla/experimento/harness/adapters/replayer.py"
FUZZERS=("boofuzz" "fume" "scapy")
```

O comando principal do `mutmut` deve seguir o modelo:

```bash
mutmut run \
  --paths-to-mutate "$TARGET_FILE" \
  --runner "python -m unittest harness/test_harness_unificado.py"
```

---

## 10. Resultados

Os resultados brutos completos ficam em:

```text
resultados_mutmut/
```

Esse diretório não deve ser versionado integralmente, pois contém caches, logs e arquivos potencialmente grandes. Para publicação acadêmica, os artefatos consolidados devem ser copiados para:

```text
results/
```

Artefatos recomendados:

```text
results/processed/*.csv
results/raw_summaries/**/summary.txt
results/figures/*.png
results/tables/*.tex
```

---

## 11. Interpretação dos resultados

Um mutante morto indica que o corpus/replayer produziu um comportamento observável diferente do baseline original. Um mutante sobrevivente pode indicar:

- mutante equivalente;
- trecho não atingido pelo fluxo MQTT configurado;
- baixa sensibilidade do corpus;
- efeito não observável no estado monitorado;
- limitação do oráculo de trace.

Assim, o mutation score deve ser interpretado como efetividade observável do fuzzer no cenário experimental, não como prova absoluta de ausência de defeitos.

---

## 12. Limitações

Este experimento depende fortemente de atingibilidade e observabilidade. Alguns módulos podem ser carregados pelo Home Assistant, mas suas mutações podem não produzir alteração no estado da entidade observada. Nesses casos, resultados com mutation score igual a zero são relevantes para discussão metodológica, pois indicam limites do oráculo e do desenho experimental.

---

## 13. Como reproduzir rapidamente

```bash
git clone https://github.com/darlagalves/SAST2026-FuzzingMQTT.git
cd SAST2026-FuzzingMQTT

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp harness/config/experimento.env.example harness/config/experimento.env
nano harness/config/experimento.env
```

Depois configure:

1. `ha_source/` com o código-fonte do Home Assistant;
2. `ha_config/` com a configuração da entidade MQTT;
3. container `ha-test` com volume apontando para `ha_source/`;
4. broker Mosquitto;
5. token do Home Assistant em `experimento.env`.

---

## 14. Licença

Definir licença antes da submissão pública. Sugestão: MIT para scripts próprios, mantendo respeito às licenças do Home Assistant e das ferramentas externas utilizadas.
