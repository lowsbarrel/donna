# Donna dimmi command
async def cmd_donna_dimmi(message, mode, input):
    try:
        (wstools.clear_p(input).lower()).replace("donna riassumimi", "")
        wbtools.send_output(
            message,
            mode,
            waitools.response(
                input,
                "Rispondi a questa domanda iniziando con Signor Zucchiatti e dandomi del lei. La domanda è: ",
            ),
        )
    except Exception as e:
        print("Exception in command donna dimmi: " + str(e))


# Donna ricordami di command
async def cmd_donna_ricordami(message, mode, input):
    try:
        print("\nTEST")
    except Exception as e:
        print("Exception in command donna ricordami: " + str(e))


# Donna riassumimi command
async def cmd_donna_riassumimi(message, mode, input):
    try:
        wbtools.send_output(
            message,
            mode,
            waitools.response(
                input,
                "Riassumi questo testo e rispondimi iniziando con Signor Zucchiatti e dandomi del lei. Il testo da riassumere è: ",
            ),
        )
    except Exception as e:
        print("Exception in command donna ricordami: " + str(e))


# Donna salva nelle note command
async def cmd_donna_salva_note(message, mode, input):
    try:
        # INSERIRE LOGICA DI SALVATAGGIO IN UN DB DELLE NOTE
        print("CIAO")
    except Exception as e:
        print("Exception in command donna salva nelle note: " + str(e))


# Get command from input and execute it
async def get_command(input, message, mode):
    try:
        clean_input = (wstools.clear_p(input)).lower()
        if "donna dimmi" in clean_input:
            cmd_donna_dimmi(message, mode, input)
        elif "donna ricordami di" in clean_input:
            cmd_donna_ricordami(message, mode, input)
        elif "donna riassumimi" in clean_input:
            cmd_donna_riassumimi(message, mode, input)
        elif "donna salva nelle note" in clean_input:
            cmd_donna_salva_note(message, mode, input)
        else:
            wbtools.send_output(message, mode, "Error, command not recognized")
            return
    except Exception as e:
        print("Exception in command detection: " + str(e))