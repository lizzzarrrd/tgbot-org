from parser_module.entrypoints.bot_handler import handle_message

print("SCRIPT STARTED")
if __name__ == "__main__":
    print(handle_message("Записаться к стоматологу 26 ноября в 14:00"))
    print("SCRIPT ENDED")