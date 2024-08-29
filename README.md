# Smart Shooter API Interface

Este script fornece uma interface de linha de comando para controlar câmeras conectadas ao Smart Shooter através de requisições via ZMQ. Ele permite iniciar e parar gravações de vídeo, além de baixar as gravações automaticamente.

Requisitos:

- Python 3.x
- Bibliotecas Python: zmq, argparse
- Smart Shooter configurado com as seguintes endpoints:
  - Event publisher: tcp://127.0.0.1:54543
  - Request/reply server: tcp://127.0.0.1:54544

Como usar:

Exibindo informações sobre as câmeras conectadas:

O script obtém automaticamente informações sobre as câmeras conectadas. Essa informação é necessária para iniciar/parar gravações e fazer downloads dos vídeos.

Iniciar gravação de vídeo:

Para iniciar a gravação de vídeo, utilize o parâmetro --start. Opcionalmente, você pode especificar o tempo de gravação com --time para parar a gravação automaticamente após o tempo definido.

  python smart_shooter.py --start --time 10

O exemplo acima inicia a gravação de vídeo e a para automaticamente após 10 segundos.

Parar gravação de vídeo:

Se a gravação foi iniciada sem um tempo definido, você pode pará-la manualmente com o parâmetro --stop.

  python smart_shooter.py --stop

Baixar o vídeo gravado:

Para baixar o vídeo após a gravação, utilize o parâmetro --download. O caminho padrão para salvar os vídeos é definido pelo Smart Shooter.

  python smart_shooter.py --start --time 10 --download

O exemplo acima inicia a gravação de vídeo, a para após 10 segundos, e então baixa o vídeo gravado para o diretório.

Gravação contínua:

Se você quiser gravar vídeos continuamente, utilize o parâmetro --loop. Você pode interromper a gravação contínua a qualquer momento pressionando Ctrl+C.

  python smart_shooter.py --start --loop

Parâmetros disponíveis:

--start: Inicia a gravação de vídeo.
--stop: Para a gravação de vídeo.
--download: Baixa o vídeo gravado.
--time: Tempo em segundos para gravar antes de parar automaticamente.
--loop: Grava vídeos continuamente até ser interrompido pelo usuário.

Exemplo de uso:

  python smart_shooter.py --start --time 15 --download

Este comando irá:

Iniciar a gravação de vídeo.
Parar automaticamente após 15 segundos.
Baixar o vídeo gravado para o diretório padrão.

Tratamento de erros:

O script exibe mensagens de erro claras caso ocorram problemas ao tentar se conectar com o Smart Shooter, iniciar/parar gravações ou baixar vídeos. Certifique-se de que o Smart Shooter está rodando corretamente e as configurações de endpoints estão corretas.

Notas:

- O script cria o diretório videos/shooter automaticamente se ele não existir para salvar os vídeos.
- Pressione Ctrl+C para interromper gravações contínuas iniciadas com o parâmetro --loop.
