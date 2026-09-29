import os
import re
from pathlib import Path

from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput


EXTENSOES = {
    ".pdf",
    ".doc",
    ".docx",
    ".htm",
    ".html",
    ".txt",
}


def nome_legivel(nome):
    nome = Path(nome).stem
    nome = nome.replace("_", " ")
    nome = re.sub(r"\s+", " ", nome)
    return nome.strip()


def chave_ordenacao(texto):
    partes = re.split(r"(\d+)", texto.casefold())
    return [
        int(parte) if parte.isdigit() else parte
        for parte in partes
    ]


class BibliotecaCasais(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(8),
            **kwargs
        )

        self.categoria = "principais"

        self.pasta_biblioteca = (
            Path(os.path.abspath(__file__)).parent
            / "biblioteca"
        )

        # TÍTULO
        titulo = Label(
            text="[b]BIBLIOTECA DE CASAIS[/b]",
            markup=True,
            font_size="22sp",
            size_hint_y=None,
            height=dp(50),
        )

        self.add_widget(titulo)

        # SUBTÍTULO
        subtitulo = Label(
            text="Estudos para casamento, família e aconselhamento",
            font_size="13sp",
            size_hint_y=None,
            height=dp(30),
        )

        self.add_widget(subtitulo)

        # BOTÕES DE CATEGORIA
        categorias = BoxLayout(
            size_hint_y=None,
            height=dp(52),
            spacing=dp(8),
        )

        botao_principais = Button(
            text="PRINCIPAIS"
        )

        botao_principais.bind(
            on_release=lambda *_:
            self.mudar_categoria("principais")
        )

        categorias.add_widget(
            botao_principais
        )

        botao_complementares = Button(
            text="COMPLEMENTARES"
        )

        botao_complementares.bind(
            on_release=lambda *_:
            self.mudar_categoria("complementares")
        )

        categorias.add_widget(
            botao_complementares
        )

        self.add_widget(
            categorias
        )

        # CAMPO DE PESQUISA
        self.busca = TextInput(
            hint_text="Pesquisar documento...",
            multiline=False,
            size_hint_y=None,
            height=dp(48),
        )

        self.busca.bind(
            text=lambda *_:
            self.mostrar_documentos()
        )

        self.add_widget(
            self.busca
        )

        # STATUS
        self.status = Label(
            text="",
            font_size="13sp",
            size_hint_y=None,
            height=dp(30),
        )

        self.add_widget(
            self.status
        )

        # ÁREA ROLÁVEL
        self.scroll = ScrollView(
            do_scroll_x=False
        )

        self.lista = GridLayout(
            cols=1,
            spacing=dp(7),
            size_hint_y=None,
            padding=(
                0,
                dp(4),
                0,
                dp(10)
            ),
        )

        self.lista.bind(
            minimum_height=
            self.lista.setter("height")
        )

        self.scroll.add_widget(
            self.lista
        )

        self.add_widget(
            self.scroll
        )

        # RODAPÉ
        rodape = Label(
            text="Toque em um documento para selecioná-lo",
            font_size="12sp",
            size_hint_y=None,
            height=dp(30),
        )

        self.add_widget(
            rodape
        )

        self.mostrar_documentos()

    def mudar_categoria(
        self,
        categoria
    ):

        self.categoria = categoria

        self.busca.text = ""

        self.mostrar_documentos()

    def localizar_documentos(
        self
    ):

        pasta = (
            self.pasta_biblioteca
            / self.categoria
        )

        if not pasta.exists():
            return []

        arquivos = []

        for arquivo in pasta.iterdir():

            if not arquivo.is_file():
                continue

            if (
                arquivo.suffix.lower()
                not in EXTENSOES
            ):
                continue

            arquivos.append(
                arquivo
            )

        arquivos.sort(
            key=lambda arquivo:
            chave_ordenacao(
                arquivo.name
            )
        )

        return arquivos

    def mostrar_documentos(
        self
    ):

        self.lista.clear_widgets()

        documentos = (
            self.localizar_documentos()
        )

        termo = (
            self.busca.text
            .strip()
            .casefold()
        )

        if termo:

            documentos = [
                arquivo
                for arquivo
                in documentos

                if termo
                in nome_legivel(
                    arquivo.name
                ).casefold()
            ]

        if (
            self.categoria
            == "principais"
        ):
            titulo_categoria = (
                "Principais"
            )
        else:
            titulo_categoria = (
                "Complementares"
            )

        self.status.text = (
            f"{titulo_categoria}: "
            f"{len(documentos)} "
            f"documento(s)"
        )

        if not documentos:

            aviso = Label(
                text=(
                    "Nenhum documento "
                    "encontrado."
                ),
                size_hint_y=None,
                height=dp(60),
            )

            self.lista.add_widget(
                aviso
            )

            return

        for arquivo in documentos:

            botao = Button(
                text=nome_legivel(
                    arquivo.name
                ),
                size_hint_y=None,
                height=dp(62),
                halign="left",
                valign="middle",
            )

            botao.bind(
                width=
                self.ajustar_texto
            )

            botao.bind(
                on_release=
                lambda _botao,
                caminho=arquivo:
                self.abrir_documento(
                    caminho
                )
            )

            self.lista.add_widget(
                botao
            )

    def ajustar_texto(
        self,
        botao,
        largura
    ):

        botao.text_size = (
            largura - dp(24),
            None
        )

    def documento_selecionado(
        self,
        caminho
    ):

        caixa = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(10),
        )

        texto = Label(
            text=(
                "[b]Documento encontrado:[/b]\n\n"
                + nome_legivel(
                    caminho.name
                )
                + "\n\n"
                + caminho.suffix.upper()
            ),
            markup=True,
            halign="center",
            valign="middle",
        )

        texto.bind(
            size=lambda widget, tamanho:
            setattr(
                widget,
                "text_size",
                tamanho
            )
        )

        caixa.add_widget(
            texto
        )

        abrir = Button(
            text="ABRIR DOCUMENTO",
            size_hint_y=None,
            height=dp(48),
        )

        abrir.bind(
            on_release=lambda *_:
            self.abrir_documento(
                caminho
            )
        )

        caixa.add_widget(
            abrir
        )

        fechar = Button(
            text="FECHAR",
            size_hint_y=None,
            height=dp(48),
        )

        caixa.add_widget(
            fechar
        )

        popup = Popup(
            title="Biblioteca de Casais",
            content=caixa,
            size_hint=(0.9, 0.48),
            auto_dismiss=False,
        )

        fechar.bind(
            on_release=
            popup.dismiss
        )

        popup.open()

    def abrir_documento(
        self,
        caminho
    ):
        try:
            import shutil

            from jnius import autoclass

            PythonActivity = autoclass(
                "org.kivy.android.PythonActivity"
            )

            Intent = autoclass(
                "android.content.Intent"
            )

            File = autoclass(
                "java.io.File"
            )

            FileProvider = autoclass(
                "androidx.core.content.FileProvider"
            )

            activity = (
                PythonActivity.mActivity
            )

            cache_android = Path(
                str(
                    activity
                    .getCacheDir()
                    .getAbsolutePath()
                )
            )

            pasta_documentos = (
                cache_android
                / "documents"
            )

            pasta_documentos.mkdir(
                parents=True,
                exist_ok=True
            )

            destino = (
                pasta_documentos
                / caminho.name
            )

            shutil.copy2(
                str(caminho),
                str(destino)
            )

            arquivo_java = File(
                str(destino)
            )

            autoridade = (
                str(
                    activity.getPackageName()
                )
                + ".fileprovider"
            )

            uri = (
                FileProvider
                .getUriForFile(
                    activity,
                    autoridade,
                    arquivo_java
                )
            )

            tipos = {
                ".pdf":
                "application/pdf",

                ".doc":
                "application/msword",

                ".docx":
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",

                ".htm":
                "text/html",

                ".html":
                "text/html",

                ".txt":
                "text/plain",
            }

            mime = tipos.get(
                caminho.suffix.lower(),
                "*/*"
            )

            intent = Intent(
                Intent.ACTION_VIEW
            )

            intent.setDataAndType(
                uri,
                mime
            )

            intent.addFlags(
                Intent.FLAG_GRANT_READ_URI_PERMISSION
            )

            activity.startActivity(
                intent
            )

        except Exception as erro:

            caixa = BoxLayout(
                orientation="vertical",
                padding=dp(12),
                spacing=dp(10),
            )

            mensagem = Label(
                text=(
                    "[b]Não foi possível "
                    "abrir o documento.[/b]\n\n"
                    + str(erro)
                ),
                markup=True,
                halign="center",
                valign="middle",
            )

            mensagem.bind(
                size=lambda widget, tamanho:
                setattr(
                    widget,
                    "text_size",
                    tamanho
                )
            )

            caixa.add_widget(
                mensagem
            )

            fechar = Button(
                text="FECHAR",
                size_hint_y=None,
                height=dp(48),
            )

            caixa.add_widget(
                fechar
            )

            popup = Popup(
                title="Biblioteca de Casais",
                content=caixa,
                size_hint=(0.9, 0.5),
                auto_dismiss=False,
            )

            fechar.bind(
                on_release=
                popup.dismiss
            )

            popup.open()


class BibliotecaCasaisApp(App):

    def build(self):

        self.title = (
            "Biblioteca de Casais"
        )

        return BibliotecaCasais()


if __name__ == "__main__":
    BibliotecaCasaisApp().run()
