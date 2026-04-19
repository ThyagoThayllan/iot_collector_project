# IoT Collector Project

Projeto em Python para coletar dados de dispositivos IoT de uma API externa, validar e normalizar os dados, e persisti-los no banco.

## O que foi feito no projeto

- Integração com API externa para consumo de três tipos de dispositivos:
  - Inversor (`/inversor`)
  - Relé de Proteção (`/rele-protecao`)
  - Estação Solarimétrica (`/estacao-solarimetrica`)
- Fluxo de coleta com tentativas de retry em caso de falha de resposta e dados inválidos.
- Regras de normalização e validação por tipo de equipamento.
- Persistência com `SQLAlchemy` em SQLite, incluindo:
  - Tabela de dispositivos.
  - Tabelas de leituras por dispositivo.
- Coletas agendadas com `APScheduler` para executar a cada 5 minutos.
- Tempo total de execução de coletas: 1 hora.

## Estrutura principal

- `api/simulator_iot_data.py`: API simuladora para onde as requisições são feitas.
- `db/db.db`: banco SQLite.
- `iot_collector/collector.py`: classes de coleta por endpoint.
- `iot_collector/collector_control.py`: validação, normalização e persistência.
- `iot_collector/database.py`: conexão com SQLite e inicialização do schema.
- `iot_collector/models/models.py`: modelos ORM (dispositivos e leituras).
- `main.py`: orquestração da execução dos coletores.

## Banco de dados

- Arquivo SQLite: `db/db.db`.
- Tabelas principais:
  - `device`
  - `inverter_reading`
  - `protection_relay_reading`
  - `solar_monitoring_station_reading`

## Dependências

As dependências estão em `requirements.txt`:

- `APScheduler`: agendamento periódico da coleta.
- `Flask`: usado para rodar a API simuladora localmente.
- `requests`: consumo dos endpoints da API.
- `SQLAlchemy`: modelagem e persistência no banco.

## Requisitos

- Desenvolvido em `Python 3.14`.
- `pip`.

## Como instalar

No diretório raiz do projeto:

```bash
python -m venv .venv
```

### Ative o ambiente virtual:

Windows (PowerShell):

```bash
.\.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### Instale as dependências:

```bash
pip install -r requirements.txt
```

## Como rodar o projeto

O sistema possui duas partes: API simuladora local e o coletor.

### 1) Subir a API simuladora

```bash
python api/simulator_iot_data.py
```

A API será iniciada em `http://127.0.0.1:5050`.

Teste rápido:

```bash
curl http://127.0.0.1:5050/health
```

### 2) Executar o coletor

Em outro terminal (com o ambiente virtual ativo):

```bash
python main.py
```

Comportamento padrão atual:

- Coleta imediata ao iniciar.
- Nova coleta a cada 5 minutos.
- Execução total por 1 hora.
- Ao final, o processo encerra com a mensagem `Collection completed!`.

## Pontos de melhoria

- Criar uma tabela (ou campos dedicados) para rastrear cada execução de coleta, registrando:
  - horário de início;
  - horário de término;
  - status da execução;
  - tipo de coletor executado;
  - mensagem de erro (quando houver).
- Padronizar exceções por categoria (rede, timeout, payload inválido, erro de persistência), facilitando observabilidade e troubleshooting.
- Tornar a URL da API e o intervalo de coleta configuráveis por variáveis de ambiente, reduzindo acoplamento com valores fixos no código.

## Observações importantes

- Para facilitar a visualização da persistência dos dados no banco, a extensão SQLite Viwer pode ser utilizada.
- A API simuladora gera tanto cenários válidos quanto cenários de erro (aprox. 20%), útil para testar a robustez da validação.
- Se quiser alterar periodicidade e janela de execução, ajuste `COLLECTION_INTERVAL` e `TIME_LIMIT` em `main.py`.
