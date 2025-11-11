# Sistema de Mapeamento de Pessoas com Deficiência (PCD)

Este projeto implementa um sistema de mapeamento de Pessoas com Deficiência (PCD) utilizando **Streamlit** para a interface de usuário, **SQLAlchemy ORM (v2.0)** para persistência de dados e **PostgreSQL** como banco de dados robusto. O sistema é modular, escalável e configurado para deploy local simplificado via **Docker Compose**.

## Estrutura do Projeto

O projeto segue uma estrutura modular para facilitar a manutenção e escalabilidade:

```
pcd_mapping_system/
├── app/
│   ├── database/
│   │   ├── __init__.py
│   │   ├── crud.py           # Funções CRUD (Create, Read, Update, Delete)
│   │   └── database.py       # Configuração do Engine e Session do SQLAlchemy
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py         # Definição dos modelos SQLAlchemy (Instituicao, PessoaPCD)
│   ├── ui/
│   │   ├── dashboard.py      # Componente de Dashboard com visualizações
│   │   ├── instituicao_manager.py # Gerenciamento de Instituições
│   │   ├── pcd_form.py       # Formulário de cadastro/edição de PCD
│   │   ├── pcd_list.py       # Lista e busca de PCDs
│   │   └── st_utils.py       # Utilitários e gerenciamento de estado do Streamlit
│   └── main.py               # Arquivo principal da aplicação Streamlit
├── .env.example              # Exemplo de variáveis de ambiente
├── .env                      # Variáveis de ambiente (para uso local)
├── Dockerfile                # Definição da imagem Docker da aplicação Streamlit
├── docker-compose.yml        # Configuração dos serviços (app e db)
└── requirements.txt          # Dependências Python
```

## Tecnologias Utilizadas

| Tecnologia | Função |
| :--- | :--- |
| **Python 3.11+** | Linguagem de programação principal. |
| **Streamlit** | Framework para criação rápida da interface web. |
| **SQLAlchemy 2.0** | ORM (Object-Relational Mapper) com tipagem para comunicação com o banco de dados. |
| **PostgreSQL** | Banco de dados relacional robusto e escalável (configurado via Docker). |
| **Docker / Docker Compose** | Ferramentas para conteinerização e orquestração do ambiente de desenvolvimento/produção. |

## Deploy Local com Docker Compose

O método recomendado para iniciar o sistema é utilizando o Docker Compose, que gerencia o contêiner do PostgreSQL e o contêiner da aplicação Streamlit.

### Pré-requisitos

Certifique-se de ter o **Docker** e o **Docker Compose** instalados em seu sistema.

### Passos para Execução

1.  **Clone o Repositório** (ou navegue até o diretório do projeto).
2.  **Configurar Variáveis de Ambiente:**
    Copie o arquivo de exemplo para criar seu arquivo de configuração:
    ```bash
    cp .env.example .env
    ```
    O arquivo `.env` já contém as configurações padrão para o PostgreSQL e a porta do Streamlit.
3.  **Iniciar os Serviços:**
    Execute o comando para construir as imagens e iniciar os contêineres em segundo plano:
    ```bash
    docker-compose up --build -d
    ```
    *Nota: Se estiver usando a versão mais recente do Docker, o comando pode ser `docker compose up --build -d`.*
4.  **Acessar a Aplicação:**
    Aguarde alguns segundos para que o banco de dados e a aplicação iniciem. A aplicação Streamlit estará acessível em:
    
    [http://localhost:8501](http://localhost:8501)

### Comandos Úteis do Docker Compose

| Comando | Descrição |
| :--- | :--- |
| `docker-compose up -d` | Inicia os contêineres em segundo plano. |
| `docker-compose down` | Para e remove os contêineres, redes e volumes (exceto o volume de dados `postgres_data`). |
| `docker-compose down -v` | Para e remove os contêineres, redes e **volumes de dados** (limpa o banco de dados). |
| `docker-compose logs -f` | Exibe os logs de todos os serviços em tempo real. |

## Execução Local (Alternativa com SQLite)

Para desenvolvimento ou teste rápido sem Docker, você pode usar o SQLite.

1.  **Instalar Dependências:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Inicializar o Banco de Dados (SQLite):**
    O arquivo `app/database/database.py` usa SQLite por padrão se a variável `DATABASE_URL` não estiver definida.
    ```bash
    PYTHONPATH=. python app/database/database.py
    ```
3.  **Executar a Aplicação Streamlit:**
    ```bash
    PYTHONPATH=. streamlit run app/main.py
    ```
    A aplicação estará acessível em [http://localhost:8501](http://localhost:8501).

## Funcionalidades da Aplicação

O sistema oferece as seguintes funcionalidades principais:

1.  **Dashboard:** Visualização de estatísticas gerais, distribuição por tipo e grau de deficiência, e mapa de localização (requer Lat/Lon preenchidos).
2.  **Gerenciamento de Instituições:** Cadastro de instituições de vínculo (ONGs, hospitais, etc.).
3.  **Cadastro de PCD:** Formulário completo para registro de novos indivíduos, incluindo dados pessoais, tipo/grau de deficiência, acessibilidade necessária e consentimento.
4.  **Lista e Busca:** Visualização tabular de todos os registros com funcionalidade de busca por nome ou tipo de deficiência.
5.  **Edição e Exclusão:** Opções para atualizar ou remover registros existentes.

---

