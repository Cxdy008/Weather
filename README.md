# Weather

Aplicação desenvolvida para o NASA Space Apps Challenge para gerar previsões climáticas a partir de dados históricos da NASA e modelos de machine learning.

## Visão geral

Este projeto combina dados meteorológicos do NASA POWER (temperatura, precipitação e velocidade do vento) com um modelo de regressão Random Forest para prever condições climáticas em uma localização geográfica específica.

A aplicação expõe uma API REST em Python utilizando FastAPI, permitindo consultar a previsão para uma data e coordenadas geográficas informadas.

## Funcionalidades

- Consulta de coordenadas geográficas (latitude e longitude)
- Geração de previsões horárias para um dia específico
- Uso de dados históricos da NASA
- Treinamento de modelos de machine learning para:
  - temperatura
  - precipitação
  - velocidade do vento
- Exposição de endpoints via FastAPI

## Arquitetura

```text
Weather/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── weather.py
│   ├── services/
│   │   └── ml.py
│   └── __init__.py
├── Procfile
├── README.md
├── requirements.txt
├── runtime.txt
├── server.py
└── .gitignore
```

### Componentes principais

- `server.py`: inicializa a aplicação FastAPI e registra as rotas da API.
- `app/api/weather.py`: define os endpoints HTTP.
- `app/services/ml.py`: faz a coleta dos dados da NASA, treina os modelos e gera as previsões.

## API

A API principal é montada com prefixo `/api` e, em seguida, o módulo de clima inclui as rotas com prefixo `/weather`.

### Endpoint de previsão

`GET /api/weather/previsao`

Parâmetros:

- `lat`: latitude
- `lon`: longitude
- `day`: dia
- `month`: mês
- `year`: ano

Exemplo:

```bash
curl "http://localhost:8000/api/weather/previsao?lat=-23.55&lon=-46.63&day=15&month=10&year=2026"
```

Resposta esperada:

```json
{
  "inputs": {
    "lat": -23.55,
    "lon": -46.63,
    "dia": 15,
    "mes": 10,
    "ano": 2026
  },
  "previsoes": [
    {
      "hora": 0,
      "temp": 24.5,
      "prec": 0.2,
      "vento": 4.1
    }
  ],
  "medias": {
    "temp": 23.8,
    "prec": 0.4,
    "vento": 4.5
  }
}
```

## Tecnologias utilizadas

- Python
- FastAPI
- Pandas
- scikit-learn
- Joblib
- Requests
- NASA POWER API

## Como executar localmente

1. Crie um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Inicie a aplicação:

```bash
uvicorn server:app --reload
```

4. Acesse a documentação automática da API em:

```text
http://localhost:8000/docs
```

## Observações

Este projeto foi pensado como uma solução de previsão meteorológica utilizando dados abertos da NASA, com foco em acessibilidade e facilidade de integração via API. Ele demonstra a combinação de dados climáticos, aprendizado de máquina e serviços web em um único sistema.

## Descrição do desafio

O projeto foi desenvolvido para participar do NASA Space Apps Challenge, com o objetivo de aplicar ciência de dados e tecnologia para entender melhor o clima e apoiar a análise de condições ambientais em diferentes regiões.
