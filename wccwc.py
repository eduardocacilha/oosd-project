import json
import sys
import traceback 
from pathlib import Path
import os
import s3fs



# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))
from service_essentials.utils.logger import Logger
from service_essentials.queue_manager.queue_manager_factory import QueueManagerFactory

config_trigger = Path(__file__).parent.parent / "sisregCirurgias.json"
output_queue = "sisregCirurgias_collector"

# criando um mensagem para cada mês e ano fornecido e passando dados da fonte (neste caso, um bucket do S3)
def generate_messages(config_file):
    with open(config_file, 'r') as file:
        config = json.load(file)

    year_list = config.get("year", [])
    month_list = config.get("month", [])
    day_list = config.get("day", [])  

    date_list = []

    for year in year_list:
        if not month_list:
            month_list = range(1, 13)
        for month in month_list:
            if not day_list:
                day_list = [1] 
            for day in day_list:
                date_list.append([year, month, day])

    messages = []
    for year, month, day in date_list:
        messages.append({
            "url_s3": "https://s3.ceos.ufsc.br",
            "bucket": "mpsc",
            "prefix": "teste/",
            "format": ".parquet",
            "date": f"{year}_{month:02d}_{day:02d}"  
        })

    return messages


def gerar_mensagens_dinamicas(url, bucket, prefix, format_ext):
    fs = s3fs.S3FileSystem(
        client_kwargs={"endpoint_url": url},
        key=os.getenv("access_key"),
        secret=os.getenv("secret_key")
    )

    # Lista todos os arquivos
    arquivos = fs.ls(f"{bucket}/{prefix}")

    mensagens = []
    for path in arquivos:
        nome = path.split("/")[-1]

        # Só pega arquivos parquet
        if nome.endswith(format_ext):
            # Extrai a data do nome do arquivo
            # fat_lista_espera_cirurgia_completa_2025_03_29.parquet
            data_str = nome.replace("fat_lista_espera_cirurgia_completa_", "").replace(format_ext, "")

            mensagens.append({
                "url_s3": url,
                "bucket": bucket,
                "prefix": prefix,
                "format": format_ext,
                "date": data_str
            })

    return mensagens

# Bloco Principal de Execução e tratamento de erros
if __name__ == '__main__':
    print(f"--- INICIANDO TRIGGER ---")
    print(f"Tentando carregar configuração de: {config_trigger}")
    logger = Logger(log_to_console=True)
    try:
        # Verifica se o arquivo JSON existe antes de tentar abrir
        if not config_trigger.is_file():
             print(f"ERRO FATAL: Arquivo de configuração NÃO ENCONTRADO em {config_trigger}")
             sys.exit(1)

        messages = generate_messages(config_trigger)
  

        if not messages:
            logger.warning(f"Nenhuma mensagem gerada. Verifique '{config_trigger}'.")
            sys.exit(0)

        logger.info(f"Geradas {len(messages)} mensagens.")
        print(f"DEBUG: Mensagens geradas: {messages}") # Veja se as mensagens estão corretas

        # --- Verificação das Variáveis de Ambiente ---
        print("\n--- VERIFICANDO VARIÁVEIS RABBITMQ ---")
        print(f"RABBITMQ_HOST: {os.getenv('RABBITMQ_HOST')}")
        print(f"RABBITMQ_USER: {os.getenv('RABBITMQ_USER')}")
        # NÃO imprima a senha em produção! Apenas para debug local.
        # print(f"RABBITMQ_PASS: {os.getenv('RABBITMQ_PASS')}")
        print(f"Output Queue Target: {output_queue}")
        print("-------------------------------------\n")
        # ---------------------------------------------

        # 2. Conexão com a Fila
        print("DEBUG: Tentando obter QueueManager...")
        queue_manager = None # Inicializa como None
        try:
            queue_manager = QueueManagerFactory.get_queue_manager()
            print(f"DEBUG: QueueManager obtido: {queue_manager}")
            print("DEBUG: Tentando conectar...")
            queue_manager.connect()
            print("DEBUG: Conexão bem-sucedida.")
            logger.info(f"Conectado. Declarando fila: {output_queue}...")
            queue_manager.declare_queue(output_queue)
            logger.info("Fila declarada/verificada.")
            print("DEBUG: Fila declarada/verificada.")

        except Exception as e_connect:
            print(f"\n--- ERRO FATAL NA CONEXÃO/DECLARAÇÃO DA FILA ---")
            print(f"Erro: {e_connect}")
            print(traceback.format_exc())
            print("-------------------------------------------------")
            sys.exit(1) # Sai se não conseguir conectar/declarar

        # 3. Publicação de Mensagens
        print("\n--- INICIANDO PUBLICAÇÃO ---")
        for i, message in enumerate(messages):
            try:
                msg_json = json.dumps(message)
                print(f"DEBUG: Publicando msg {i+1} para '{output_queue}': {msg_json}")
                queue_manager.publish_message(output_queue, msg_json)
                logger.info(f"Mensagem #{i+1} enviada para {output_queue}: [data: {message['date']}]")
                print(f"DEBUG: Mensagem {i+1} publicada com sucesso.")
            except Exception as e_publish:
                 print(f"\n--- ERRO AO PUBLICAR MENSAGEM {i+1} ---")
                 print(f"Mensagem: {message}")
                 print(f"Erro: {e_publish}")
                 print(traceback.format_exc())
                 # Decide se continua para a próxima mensagem ou para
                 # continue # Para tentar as próximas
                 break # Para se encontrar um erro de publicação

        logger.info("Publicação de mensagens concluída (ou interrompida por erro).")
        print("--- PUBLICAÇÃO CONCLUÍDA (ou interrompida) ---")

    except FileNotFoundError:
        # O print inicial já deve ter pego isso, mas mantém por segurança
        logger.error(f"ERRO CRÍTICO: O arquivo '{config_trigger}' não foi encontrado.")
        print(f"ERRO CRÍTICO: Arquivo '{config_trigger}' não encontrado.")
    except Exception as e:
        tb_str = traceback.format_exc()
        logger.error(f"Ocorreu um erro fatal no trigger: {e}\nTRACEBACK:\n{tb_str}")
        print(f"\n--- ERRO FATAL INESPERADO NO TRIGGER ---")
        print(f"Erro: {e}")
        print(tb_str)
        print("---------------------------------------")



