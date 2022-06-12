bprocess import getoutput as getoutput




from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram import ForceReply

from keep_alive import keep_alive
keep_alive()

import os
import glob

from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)


def listar():
    excluir=[]
    excluir+=glob.glob('*.txt.start.txt')
    excluir+=glob.glob('requirements.txt')
    excluir+=glob.glob('cola*txt')
    lista=glob.glob('*.txt')
    for item in excluir:
        try:
          lista.remove(item)
        except:
          pass
    
    return lista


OPCION, COLA, PAUSAR, LANZAR, REANUDAR, ENCOLAR, CONSULTAR, VACIAR, BORRAR, ENVIAR = range(10)

def start(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['Enviar links', 'Controlar cola', 'Borrar serie'],['Chequear','Terminar']]

    update.message.reply_text(
        '¿Qué deseas hacer?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Seleccione una opción', resize_keyboard=True
        ),
    )

    return OPCION

def cola(update: Update, context: CallbackContext) -> int:
    reply_keyboard_cola = [['Pausar cola', 'Reanudar cola', 'Consultar cola'],['Lanzar serie', 'Encolar serie', 'Vaciar cola'],['Menú principal']]

    update.message.reply_text(
        '¿Qué deseas hacer?',
        reply_markup=ReplyKeyboardMarkup(
        reply_keyboard_cola, one_time_keyboard=True, input_field_placeholder='Seleccione una opción:', resize_keyboard=True
        ),
    )
    return COLA

def pausar(update: Update, context: CallbackContext) -> int:
    link=update.message.text
    update.message.reply_text(f'Pausando la cola')
    salida=getoutput(f'./parar.sh')
    update.message.reply_text(salida)
    return cancel(update, context)
    #return start(update, context)

def reanudar(update: Update, context: CallbackContext) -> int:
    link=update.message.text
    update.message.reply_text(f'Reanudando la cola')
    salida=getoutput(f'./reanudar.sh')
    update.message.reply_text(salida)
    return cancel(update, context)
    #return start(update, context)

def consultar(update: Update, context: CallbackContext) -> int:
    if os.path.exists('cola.txt'):
      with open('cola.txt') as c:
        cola=c.read().split('\n')

      for i in range(0, len(cola), 40): 
        update.message.reply_text('\n'.join(cola[i:i + 40]))

    else:
      update.message.reply_text('No hay nada en la cola')
    
    return start(update, context)

def vaciar(update: Update, context: CallbackContext) -> int:
    if os.path.exists('cola.txt'):
        salida=getoutput('vaciar')

    update.message.reply_text('Cola vaciada y detenida')
    return cancel(update, context)
    #return start(update, context)

def lanzar(update: Update, context: CallbackContext) -> int:
    txt=listar()
    if not txt:
        update.message.reply_text('No hay archivos que mostrar')
        return start(update, context)
    
    menu=[]
    for i in range(0, len(txt), 5): 
        menu.append(txt[i:i + 5])

    reply_keyboard_lanzar = menu+[['Menú principal']]

    update.message.reply_text(
        '¿Qué archivo quieres lanzar?',
        reply_markup=ReplyKeyboardMarkup(
        reply_keyboard_lanzar, one_time_keyboard=True, input_field_placeholder='Seleccione un archivo para lanzar:', resize_keyboard=True
        ),
    )
    return LANZAR

def lanzado(update: Update, context: CallbackContext) -> int:
    archivo=update.message.text
    update.message.reply_text(f'Lanzando archivo {archivo}, espera un momento...')
    salida=getoutput(f'./lanzar.sh "{archivo}"')
    update.message.reply_text(salida)
    return cancel(update, context)
    #return start(update, context)

def ver(update: Update, context: CallbackContext) -> int:
    salida=getoutput(f'./checar.sh')
    update.message.reply_text(salida)
    return start(update, context)

def encolar(update: Update, context: CallbackContext) -> int:
    txt=listar()
    if not txt:
        update.message.reply_text('No hay archivos que mostrar')
        return start(update, context)
   
    menu=[]
    for i in range(0, len(txt), 5): 
        menu.append(txt[i:i + 5])

    reply_keyboard_encolar = menu + [['Menú principal']]

    update.message.reply_text(
        '¿Qué archivo quieres encolar?',
        reply_markup=ReplyKeyboardMarkup(
        reply_keyboard_encolar, one_time_keyboard=True, input_field_placeholder='Seleccione un archivo para encolar:', resize_keyboard=True
        ),
    )
    return ENCOLAR

def encolado(update: Update, context: CallbackContext) -> int:
    archivo=update.message.text
    update.message.reply_text(f'Encolando archivo {archivo}, espera un momento...')
    salida=getoutput(f'./encolar.sh "{archivo}"')
    salida=salida.split('\n')
    for i in range(0, len(salida), 40): 
      update.message.reply_text('\n'.join(salida[i:i + 40]))
      
    return cancel(update, context)
    #return start(update, context)

def borrar(update: Update, context: CallbackContext) -> int:
    txt=listar()
    if not txt:
        update.message.reply_text('No hay archivos que mostrar')
        return start(update, context)

    menu=[]
    for i in range(0, len(txt), 5): 
        menu.append(txt[i:i + 5])

    reply_keyboard_borrar = menu + [['Todas','Menú principal']]

    update.message.reply_text(
        '¿Qué archivo quieres borrar?',
        reply_markup=ReplyKeyboardMarkup(
        reply_keyboard_borrar, one_time_keyboard=True, input_field_placeholder='Seleccione un archivo para borrar:', resize_keyboard=True
        ),
    )
    return BORRAR

def borrado(update: Update, context: CallbackContext) -> int:
    archivo=update.message.text
    if archivo=='Todas':
      txt=listar()
      for archivo in txt:  
        update.message.reply_text(f'Borrando archivo {archivo}, espera un momento...')
        getoutput(f'rm "{archivo}"')
    else:
      update.message.reply_text(f'Borrando archivo {archivo}, espera un momento...')
      getoutput(f'rm "{archivo}"')
    
    return start(update, context)

def enviar(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Introduzca los enlaces de la serie:',reply_markup=ForceReply(selective=False))
    return ENVIAR

def enviado(update: Update, context: CallbackContext) -> int:
    contenido=update.message.text
    import time
    nombre = time.strftime("%Y%m%d-%H%M%S")+'.txt'
    update.message.reply_text(f'Guardando enlaces en {nombre}, espera un momento...')
    with open(nombre,'w') as w:
        w.write(contenido)
    update.message.reply_text('Archivo guardado')
    return start(update, context)


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    update.message.reply_text(
        'Sesión terminada. Escribe /start para volver a empezar.', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def error(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    update.message.reply_text(
        'No estás autorizado para usarme. No hay nada que ver acá.', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    token=str(os.environ['TOKEN'])
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start, Filters.user(username=["@akuotoko","@lamakina12"])), CommandHandler('start', error)],
        states={
            OPCION: [MessageHandler(Filters.regex('^Enviar links$'), enviar),MessageHandler(Filters.regex('^Controlar cola$'), cola),MessageHandler(Filters.regex('^Borrar serie$'), borrar), MessageHandler(Filters.regex('^Chequear$'), ver), MessageHandler(Filters.regex('^Terminar$'), cancel)],
            COLA: [MessageHandler(Filters.regex('^Pausar cola$'), pausar), MessageHandler(Filters.regex('^Reanudar cola$'), reanudar), MessageHandler(Filters.regex('^Consultar cola$'), consultar), MessageHandler(Filters.regex('^Lanzar serie$'), lanzar), MessageHandler(Filters.regex('^Encolar serie$'), encolar), MessageHandler(Filters.regex('^Vaciar cola$'), vaciar),MessageHandler(Filters.regex('^Menú principal$'), start)],
            LANZAR: [MessageHandler(Filters.regex('^Menú principal$'), start), MessageHandler(Filters.text, lanzado)],
            ENCOLAR: [MessageHandler(Filters.regex('^Menú principal$'), start), MessageHandler(Filters.text, encolado)],
            BORRAR: [MessageHandler(Filters.regex('^Menú principal$'), start), MessageHandler(Filters.text, borrado)],
            ENVIAR: [MessageHandler(Filters.text, enviado)],
        },
        fallbacks=[CommandHandler('cancel', cancel), CommandHandler('start', start)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()