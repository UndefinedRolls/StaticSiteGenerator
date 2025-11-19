import textnode


def main():
    new_text = textnode.TextNode("This is some anchor text", textnode.TextType.LINK, "https://www.boot.dev")
    print(new_text)


main()