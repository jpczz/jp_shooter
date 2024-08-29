import json
import argparse
import zmq
import time
import os

def get_camera_info(socket):
    """
    Envia um request para obter informações sobre todas as câmeras conectadas.
    Retorna a resposta JSON decodificada.
    """
    req = {
        "msg_type": "Request",
        "msg_id": "GetCamera",
        "msg_seq_num": 1,  # Número único para identificar o request
        "CameraSelection": "All"
    }
    socket.send_string(json.dumps(req))
    rep = socket.recv()
    json_msg = json.loads(rep.decode("utf-8"))
    return json_msg

def start_video_recording(socket, camera_key):
    """
    Envia um request para iniciar a gravação de vídeo em uma câmera específica.
    
    Parâmetros:
    - socket: O socket ZMQ configurado para se comunicar com o Smart Shooter.
    - camera_key: O identificador único da câmera na qual iniciar a gravação de vídeo.
    
    Retorna:
    - A resposta JSON decodificada do Smart Shooter.
    """
    req = {
        "msg_type": "Request",
        "msg_id": "EnableVideo",
        "msg_seq_num": 2,  # Número único para identificar o request
        "CameraSelection": "Single",
        "CameraKey": camera_key,
        "Enable": True  # Inicia a gravação de vídeo
    }
    socket.send_string(json.dumps(req))
    rep = socket.recv()
    json_msg = json.loads(rep.decode("utf-8"))
    return json_msg

def stop_video_recording(socket, camera_key):
    """
    Envia um request para parar a gravação de vídeo em uma câmera específica.
    
    Parâmetros:
    - socket: O socket ZMQ configurado para se comunicar com o Smart Shooter.
    - camera_key: O identificador único da câmera na qual parar a gravação de vídeo.
    
    Retorna:
    - A resposta JSON decodificada do Smart Shooter.
    """
    req = {
        "msg_type": "Request",
        "msg_id": "EnableVideo",
        "msg_seq_num": 3,  # Número único para identificar o request
        "CameraSelection": "Single",
        "CameraKey": camera_key,
        "Enable": False  # Para a gravação de vídeo
    }
    socket.send_string(json.dumps(req))
    rep = socket.recv()
    json_msg = json.loads(rep.decode("utf-8"))
    return json_msg

def download_video(socket, camera_key, download_path):
    """
    Envia um request para baixar o vídeo gravado para um diretório específico.
    
    Parâmetros:
    - socket: O socket ZMQ configurado para se comunicar com o Smart Shooter.
    - camera_key: O identificador único da câmera que contém o vídeo.
    - download_path: O caminho onde o vídeo será salvo.
    
    Retorna:
    - A resposta JSON decodificada do Smart Shooter.
    """
    req = {
        "msg_type": "Request",
        "msg_id": "Download",
        "msg_seq_num": 5,  # Número único para identificar o request
        "CameraSelection": "Single",
        "CameraKey": camera_key,
        "PhotoSelection": "All",  # Seleciona todas as fotos/vídeos
        "DownloadPath": download_path
    }
    socket.send_string(json.dumps(req))
    rep = socket.recv()
    json_msg = json.loads(rep.decode("utf-8"))
    return json_msg

def main():
    context = zmq.Context()

    req_socket = context.socket(zmq.REQ)
    req_socket.connect("tcp://127.0.0.1:54544")

    parser = argparse.ArgumentParser(description="Smart Shooter API Interface")

    parser.add_argument("--start", help="Start video recording", action="store_true")
    parser.add_argument("--stop", help="Stop video recording", action="store_true")
    parser.add_argument("--download", help="Download the video after recording", action="store_true")
    parser.add_argument("--time", type=int, help="Time in seconds to record before stopping automatically")
    parser.add_argument("--loop", help="Continuously record videos until interrupted", action="store_true")

    args = parser.parse_args()

    # Obtendo a CameraKey automaticamente
    camera_info = get_camera_info(req_socket)
    if camera_info["msg_result"]:
        if "CameraInfo" in camera_info and camera_info["CameraInfo"]:
            camera_key = camera_info["CameraInfo"][0]["CameraKey"]

            try:
                while True:
                    if args.start:
                        video_recording_result = start_video_recording(req_socket, camera_key)
                        if video_recording_result["msg_result"]:
                            print("rec_start")

                            if args.time:
                                time.sleep(args.time)
                                stop_result = stop_video_recording(req_socket, camera_key)
                                if stop_result["msg_result"]:
                                    print("rec_stop")
                                    if args.download:
                                        print("down_start")
                                        # Definindo o caminho de download
                                        download_path = os.path.join("videos", "shooter")
                                        os.makedirs(download_path, exist_ok=True)

                                        # Baixando o vídeo
                                        download_result = download_video(req_socket, camera_key, download_path)
                                        if download_result["msg_result"]:
                                            print(f"down_done")
                                        else:
                                            print("Falha ao baixar o vídeo")
                                else:
                                    print("Falha ao interromper a gravação de vídeo automaticamente")

                            if not args.loop:
                                break

                    if args.stop:
                        video_recording_result = stop_video_recording(req_socket, camera_key)
                        if video_recording_result["msg_result"]:
                            print("Gravação de vídeo interrompida com sucesso")

                            if args.download:
                                # Definindo o caminho de download
                                download_path = os.path.join("videos", "shooter")
                                os.makedirs(download_path, exist_ok=True)

                                # Baixando o vídeo
                                download_result = download_video(req_socket, camera_key, download_path)
                                if download_result["msg_result"]:
                                    print(f"Vídeo baixado com sucesso para {download_path}")
                                else:
                                    print("Falha ao baixar o vídeo")
                        else:
                            print("Falha ao interromper a gravação de vídeo")
                        break
            except KeyboardInterrupt:
                print("Gravação contínua interrompida pelo usuário.")

        else:
            print("Nenhuma câmera conectada")
    else:
        print(f"Erro ao obter informações da câmera: {camera_info['msg_error']}")

if __name__ == "__main__":
    main()
