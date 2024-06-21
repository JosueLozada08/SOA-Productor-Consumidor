import pika
import smtplib

# ConfiguraciÃ³n de conexiÃ³n con RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declarar una cola
channel.queue_declare(queue='correo')

def callback(ch, method, properties, body):
    # Enviar el mensaje por correo electrÃ³nico
    mensaje = body.decode('utf-8')
    destinatario = 'ejemplo@dominio.com'
    remitente = 'remitente@dominio.com'
    asunto = 'Mensaje recibido desde la cola'

    # ConfiguraciÃ³n de SMTP
    servidor_smtp = 'smtp.ejemplo.com'
    puerto_smtp = 587

    # Crear mensaje
    cuerpo_mensaje = f'Asunto: {asunto}\n\n{mensaje}'

    # Enviar correo electrÃ³nico
    with smtplib.SMTP(servidor_smtp, puerto_smtp) as servidor:
        servidor.starttls()
        servidor.login('usuario@dominio.com', 'contraseÃ±a')
        servidor.sendmail(remitente, destinatario, cuerpo_mensaje)

    print(f"Mensaje enviado por correo electrÃ³nico: {mensaje}")

# Consumir mensajes de la cola
channel.basic_consume(queue='correo', on_message_callback=callback, auto_ack=True)

print('Esperando mensajes. Presiona CTRL+C para salir.')
channel.start_consuming()