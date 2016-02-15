from Parser import Parser


class Menu:
    def __init__(self):
        pass

    def parse(self, commands, service_name, command_name):
        main_name = "main"

        parsers = {
            main_name: Parser(prog='hive')
        }

        subparsers = {
            service_name: parsers[main_name].add_subparsers(
                title=service_name,
                dest=service_name
            )
        }

        for commandName in commands:
            command = commands[commandName]
            parsers[commandName] = subparsers[service_name].add_parser(
                commandName, help=command["help"]
            )
            subparsers[commandName] = parsers[commandName].add_subparsers(
                title=command_name, dest=command_name
            )

            for subCommandName in command["commands"]:
                sub_command = command["commands"][subCommandName]
                parsers[subCommandName] = subparsers[commandName].add_parser(
                    subCommandName, help=sub_command["help"]
                )

                if "parameters" in sub_command:
                    for parameters in sub_command["parameters"]:
                        name = parameters["name"]
                        doc = parameters["help"]
                        if "nargs" in parameters:
                            parsers[subCommandName].add_argument(
                                name,
                                help=doc,
                                nargs=parameters["nargs"]
                            )
                        elif "action" in parameters:
                            parsers[subCommandName].add_argument(
                                name,
                                help=doc,
                                action=parameters["action"],
                                const=name
                            )
                        else:
                            parsers[subCommandName].add_argument(name, help=doc)

        return parsers[main_name].parse_args()
