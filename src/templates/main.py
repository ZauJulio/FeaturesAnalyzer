import argparse  # noqa: INP001

from jinja2 import Template

# Template para gerar a classe
CLASS_TEMPLATE = """
class {{ class_name }}:
    def __init__(self, *args, **kwargs):
        pass

    def __repr__(self):
        return f"<{{ class_name }} instance>"
"""


def generate_class(class_name: str) -> str:
    """
    Gera uma classe Python a partir de um template.

    Args:
        class_name (str): O nome da classe.

    Returns:
        str: O código da classe gerado.

    """
    template = Template(CLASS_TEMPLATE)
    return template.render(class_name=class_name)


def main() -> None:
    """Temp."""
    # Configura o parser de argumentos da CLI
    parser = argparse.ArgumentParser(description="Gerador de classes Python.")
    parser.add_argument(
        "class_name",
        type=str,
        help="O nome da classe a ser gerada.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Arquivo de saída para salvar a classe gerada (opcional).",
    )

    args = parser.parse_args()

    # Gera o código da classe
    class_code = generate_class(args.class_name)

    if args.output:
        # Salva em um arquivo
        with open(args.output, "w", encoding="utf-8") as file:  # noqa: FURB103, PTH123
            file.write(class_code)

        print(f"Classe gerada e salva em {args.output}")  # noqa: T201
    else:
        # Imprime no terminal
        print("Classe gerada:")  # noqa: T201
        print(class_code)  # noqa: T201


if __name__ == "__main__":
    main()
