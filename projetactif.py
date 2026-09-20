import flet as ft
import os
import webbrowser
import json
from datetime import datetime
import locale

try:
    import pyperclip
except ImportError:
    pyperclip = None

# --- CONFIGURATION ---
CONFIG_FILE = "config_odoo.json"
BASE_PATH_DEFAULT = "/home/mahjoub/Documents/local"
ODOO_SOURCE_ROOT = "/home/mahjoub/Documents/odoo_source"


def main(page: ft.Page):
    # page.window.full_screen = True
    page.title = "OdooSwitch Ultimate v7.1"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#1a1c23"
    page.padding = 15
    page.window_maximized = True
    page.window_minimized = True

    # Initialisation du service Presse-papiers pour Flet 1.0+
    if not any(isinstance(s, ft.Clipboard) for s in page.services):
        page.services.append(ft.Clipboard())

    page.update()
    try:
        locale.setlocale(locale.LC_TIME, "fr_FR.utf8")
    except:
        pass

    async def on_keyboard(e: ft.KeyboardEvent):
        if e.key == "F" or e.key == "Escape":
            page.window.full_screen = not page.window.full_screen
            page.update()
        if e.key == "Q":
            import inspect
            try:
                if hasattr(page, "window_destroy"):
                    res = page.window_destroy()
                    if inspect.isawaitable(res):
                        await res
                elif hasattr(page, "window"):
                    if hasattr(page.window, "destroy"):
                        res = page.window.destroy()
                        if inspect.isawaitable(res):
                            await res
                    elif hasattr(page.window, "close"):
                        res = page.window.close()
                        if inspect.isawaitable(res):
                            await res
            except Exception as ex:
                print(f"Error quitting app: {ex}")

    page.on_keyboard_event = on_keyboard

    # --- NOUVELLE MÉTHODE SNACKBAR ---
    def show_msg(text, color="#c678dd"):
        sb = ft.SnackBar(ft.Text(text), bgcolor=color)
        page.overlay.append(sb)
        sb.open = True
        page.update()

    # --- CHARGEMENT DES DONNÉES ---
    def get_odoo_versions():
        """Détecte les versions d'Odoo dans le dossier source sans passer par le JSON."""
        # On utilise la variable globale définie au début du fichier
        if os.path.exists(ODOO_SOURCE_ROOT):
            try:
                items = os.listdir(ODOO_SOURCE_ROOT)
                versions = [
                    d
                    for d in items
                    if os.path.isdir(os.path.join(ODOO_SOURCE_ROOT, d))
                       and d.startswith("odoo_")
                ]
                versions.sort()
                return versions if versions else ["odoo_15"]
            except:
                pass
        return ["odoo_14", "odoo_15", "odoo_16", "odoo_17", "odoo_18"]

    def load_config():
        config = {
            "roots": [BASE_PATH_DEFAULT],
            "versions": get_odoo_versions(),
            "tokens": [{"name": "", "key": ""} for _ in range(5)],
        }
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    saved = json.load(f)
                    config["roots"] = saved.get("roots", [BASE_PATH_DEFAULT])
                    # Charger les tokens du JSON s'ils existent
                    if "tokens" in saved:
                        config["tokens"] = saved["tokens"]

                    # Charger le reste
                    for k, v in saved.items():
                        if k not in ["versions", "roots", "tokens"]:
                            config[k] = v
            except:
                pass

        # S'assurer qu'on a toujours 5 tokens
        while len(config["tokens"]) < 5:
            config["tokens"].append({"name": "", "key": ""})
        config["tokens"] = config["tokens"][:5]

        return config

    state = load_config()
    initial_tokens = state["tokens"]

    # --- LOGIQUE MÉTIER ---

    def save_all(e=None):
        # Récupérer les tokens actuels depuis l'UI
        current_tokens = []
        try:
            for row in token_rows.controls:
                n_val = row.controls[0].value or ""
                k_val = row.controls[1].value or ""
                current_tokens.append({"name": n_val.strip(), "key": k_val.strip()})
        except:
            current_tokens = state.get("tokens", [])

        config_data = {
            "roots": state.get("roots", [BASE_PATH_DEFAULT]),
            "tokens": current_tokens,
        }
        try:
            config_data["last_parent"] = combo_parent.value
            config_data["last_sub"] = combo_sub.value
            config_data["last_ver"] = combo_ver.value
            config_data["chk_commu"] = chk_commu.value
            config_data["chk_ent"] = chk_ent.value
            config_data["txt_template"] = txt_template.value
        except Exception:
            config_data.update(
                {
                    "last_parent": state.get("last_parent"),
                    "last_sub": state.get("last_sub"),
                    "last_ver": state.get("last_ver"),
                    "chk_commu": state.get("chk_commu", False),
                    "chk_ent": state.get("chk_ent", False),
                    "txt_template": state.get(
                        "txt_template",
                        "[options]\nadmin_passwd = admin@21\naddons_path = \ndb_host = False\ndb_name = False\ndb_password = mahjoub\ndb_port = False\ndb_user = mahjoub\nhttp_port = 8069\ndbfilter = .*$",
                    ),
                }
            )

        with open(CONFIG_FILE, "w") as f:
            json.dump(config_data, f, indent=4)

        # On met à jour l'état local aussi
        state.update(config_data)

    def sync_subs(e=None):
        parent = combo_parent.value
        combo_sub.options = []
        combo_sub.value = None
        if parent and os.path.exists(parent):
            try:
                items = os.listdir(parent)
                subs = [
                    d
                    for d in items
                    if os.path.isdir(os.path.join(parent, d)) and not d.startswith(".")
                ]
                subs.sort()
                combo_sub.options = [ft.dropdown.Option(s) for s in subs]
                if subs:
                    combo_sub.value = subs[0]
                    generate_infos()
            except:
                pass
        save_all()
        page.update()

    def generate_infos(e=None):
        p = combo_sub.value
        if p:
            now = datetime.now().strftime("%d_%B_%H_%M")
            txt_db.value = f"base_{p}_{now}"
            txt_scaf.value = f"python3 odoo-bin scaffold custom_{p} ./addons"
        save_all()
        page.update()

    def run_odoo_process(e):
        p = combo_sub.value
        v = combo_ver.value
        parent = combo_parent.value

        save_all()  # Update JSON with current selection
        b_filter = p

        if not p or not v or not parent:
            show_msg("Sélection incomplète !", "red")
            return

        conf_path = os.path.join(ODOO_SOURCE_ROOT, v, "odoo.conf")
        if not os.path.exists(conf_path):
            show_msg(f"Fichier config introuvable : {conf_path}", "red")
            return

        try:
            all_items = sorted(
                [
                    d
                    for d in os.listdir(parent)
                    if os.path.isdir(os.path.join(parent, d))
                ]
            )
            http_port = 8060 + all_items.index(p)
        except:
            http_port = 8069

        with open(conf_path, "r") as f:
            lines = f.readlines()

        with open(conf_path, "w") as f:
            for line in lines:
                if "addons_path" in line:
                    ln = line
                    if chk_commu.value:
                        ln = ln.replace("enterprise,", "odoo/addons,")
                    elif chk_ent.value:
                        ln = ln.replace("odoo/addons,", "enterprise,")

                    # On sépare la ligne par le '='
                    if "=" in ln:
                        prefix, paths_str = ln.split("=", 1)
                        path_list = [p_item.strip() for p_item in paths_str.split(",") if p_item.strip()]

                        # Chemin complet du projet sélectionné
                        new_project_path = os.path.join(parent, p)

                        # Filtrer pour garder uniquement les chemins odoo_source
                        # et ajouter à la fin notre nouveau chemin projet
                        final_paths = []
                        for path in path_list:
                            # On garde les chemins qui sont dans ODOO_SOURCE_ROOT
                            # On ignore TOUT ce qui n'est pas dans odoo_source pour le remplacer par le nouveau chemin complet
                            if ODOO_SOURCE_ROOT in path:
                                final_paths.append(path)

                        # Ajouter le chemin complet du projet (Dossier Parent + Projet)
                        if new_project_path not in final_paths:
                            final_paths.append(new_project_path)

                        f.write(f"{prefix.strip()} = {', '.join(final_paths)}\n")
                    else:
                        f.write(ln)
                elif "dbfilter" in line:
                    parts = line.split(".*")
                    f.write(line.replace(parts[-2], b_filter))
                elif "http_port" in line:
                    parts = line.split("=")
                    f.write(line.replace(parts[-1], f" {http_port}\n"))
                else:
                    f.write(line)

        txt_url.value = f"localhost:{http_port}"
        show_msg(f"Config {v} OK (Port {http_port})", "#10B981")
        page.update()

    # --- UI COMPONENTS (USAGE DE ft.Button POUR ÉVITER LES WARNINGS) ---

    combo_parent = ft.Dropdown(
        label="Dossier Parent", expand=True, on_select=lambda _: sync_subs()
    )
    combo_sub = ft.Dropdown(
        label="Projet Détecté", expand=True, on_select=generate_infos
    )
    combo_ver = ft.Dropdown(label="Version Odoo", width=200, on_select=generate_infos)

    chk_commu = ft.Checkbox(
        label="Communautaire", value=state.get("chk_commu", False), on_change=save_all
    )
    chk_ent = ft.Checkbox(
        label="Enterprise", value=state.get("chk_ent", False), on_change=save_all
    )

    token_rows = ft.Column()

    def copy_token(e, val):
        if not val.value:
            show_msg("Le champ est vide !", "red")
            return

        success = False
        # Strategy 1: Flet 1.0+ Service method
        try:
            if hasattr(page, "clipboard") and page.clipboard:
                page.clipboard.set_data(val.value)
                success = True
        except Exception:
            pass

        # Strategy 2: Legacy Flet set_clipboard method
        if not success:
            try:
                if hasattr(page, "set_clipboard"):
                    page.set_clipboard(val.value)
                    success = True
            except Exception:
                pass

        # Strategy 3: Pyperclip fallback (Very reliable on Linux/OSX/Windows)
        if not success and pyperclip:
            try:
                pyperclip.copy(val.value)
                success = True
            except Exception:
                pass

        if success:
            show_msg(f"Copié : {val.label} !", "#10B981")
        else:
            msg = "Erreur : Presse-papiers non disponible"
            if not pyperclip:
                msg += " (installez 'pyperclip')"
            show_msg(msg, "red")

    for i in range(5):
        n = ft.TextField(
            label="Nom", width=150, value=initial_tokens[i]["name"], bgcolor="#2c313a"
        )
        k = ft.TextField(
            label="Token",
            expand=True,
            value=initial_tokens[i]["key"],
            password=True,
            can_reveal_password=True,
            bgcolor="#2c313a",
        )
        n.on_change = save_all
        k.on_change = save_all
        btn_cp = ft.TextButton(
            "📋",
            on_click=lambda e, val=k: copy_token(e, val),
        )
        token_rows.controls.append(ft.Row([n, k, btn_cp]))

    txt_url = ft.TextField(label="URL", value="localhost:8069", expand=True)
    txt_db = ft.TextField(label="Base de données", expand=True)
    txt_scaf = ft.TextField(label="Scaffold Command", multiline=True, min_lines=2)

    # --- VUES ---
    workspace_view = ft.Column(
        [
            ft.Row(
                [
                    combo_parent,
                    ft.Row(
                        [
                            combo_sub,
                            ft.Button(
                                "▶️ RUN",
                                bgcolor="#10B981",
                                color="white",
                                on_click=run_odoo_process,
                            ),
                        ],
                        expand=True,
                    ),
                    combo_ver,
                ]
            ),
            ft.Row(
                [
                    ft.Container(
                        content=ft.Row([chk_commu, chk_ent]),
                        bgcolor="#252a34",
                        padding=10,
                        border_radius=10,
                    )
                ]
            ),
            ft.Container(
                content=token_rows, padding=15, bgcolor="#282c34", border_radius=10
            ),
            ft.Row(
                [
                    txt_url,
                    ft.Button(
                        "🌐 CHROME",
                        on_click=lambda _: webbrowser.open(f"http://{txt_url.value}"),
                    ),
                ]
            ),
            ft.Row(
                [
                    txt_db,
                    ft.Button(
                        "🔄 RÉ-GÉNÉRER BD",
                        on_click=generate_infos,
                        bgcolor="#8B5CF6",
                        color="white",
                    ),
                ]
            ),
            txt_scaf,
            ft.Button(
                "🔄 SCAN PROJETS",
                bgcolor="#3b82f6",
                color="white",
                expand=True,
                height=60,
                on_click=sync_subs,
            ),
        ],
        visible=True,
        scroll="auto",
    )

    txt_new_root = ft.TextField(label="Nouveau Chemin", expand=True)
    roots_list = ft.Column()

    txt_template = ft.TextField(
        label="Template odoo.conf",
        multiline=True,
        min_lines=8,
        value=state.get(
            "txt_template",
            "[options]\nadmin_passwd = admin@21\naddons_path = \ndb_host = False\ndb_name = False\ndb_password = mahjoub\ndb_port = False\ndb_user = mahjoub\nhttp_port = 8069\ndbfilter = .*$",
        ),
        on_change=save_all,
    )
    combo_ver_template = ft.Dropdown(label="Version Odoo", width=200)

    def refresh_ui():
        combo_parent.options = [ft.dropdown.Option(r) for r in state["roots"]]
        combo_ver.options = [ft.dropdown.Option(v) for v in state["versions"]]
        combo_ver_template.options = [ft.dropdown.Option(v) for v in state["versions"]]
        combo_ver.value = state.get("last_ver")
        if state["roots"]:
            if not combo_parent.value:
                combo_parent.value = state.get("last_parent") or state["roots"][0]
            sync_subs()
            if state.get("last_sub"):
                combo_sub.value = state.get("last_sub")
                generate_infos()

        roots_list.controls = []
        for r in state["roots"]:
            roots_list.controls.append(
                ft.Row(
                    [
                        ft.Text(r, expand=True),
                        ft.Button(
                            "🗑️",
                            color="red",
                            on_click=lambda e, p=r: [
                                state["roots"].remove(p),
                                save_all(),
                                refresh_ui(),
                            ],
                        ),
                    ]
                )
            )
        page.update()

    def add_root(e):
        if txt_new_root.value:
            state["roots"].append(txt_new_root.value)
            txt_new_root.value = ""
            save_all()
            refresh_ui()

    def paste_template(e):
        v = combo_ver_template.value
        if not v:
            show_msg("Veuillez sélectionner une version", "red")
            return
        conf_path = os.path.join(ODOO_SOURCE_ROOT, v, "odoo.conf")
        try:
            with open(conf_path, "w") as f:
                f.write(txt_template.value)
            show_msg(f"Template collé dans {conf_path}", "green")
        except Exception as ex:
            show_msg(f"Erreur : {ex}", "red")

    combo_ver_template.on_select = paste_template
    btn_paste_template = ft.Button(
        "PASTE", on_click=paste_template, bgcolor="#10B981", color="white"
    )

    # --- PARAMÈTRES GLOBAUX ---
    txt_source_root = ft.TextField(
        label="Racine Sources Odoo", value=ODOO_SOURCE_ROOT, expand=True
    )

    def update_paths(e):
        global ODOO_SOURCE_ROOT
        ODOO_SOURCE_ROOT = txt_source_root.value
        state["versions"] = get_odoo_versions()
        refresh_ui()
        show_msg("Chemins mis à jour (non persistants)", "blue")

    settings_view = ft.Column(
        [
            ft.Text("CHEMINS ET RÉGLAGES", size=20, weight="bold"),
            ft.Row([txt_source_root]),
            ft.Row(
                [
                    ft.Button("ACTUALISER CHEMINS", on_click=update_paths),
                ]
            ),
            ft.Divider(),
            ft.Text("GESTION DES RACINES PROJETS", size=20, weight="bold"),
            ft.Row([txt_new_root, ft.Button("➕", on_click=add_root)]),
            roots_list,
            ft.Divider(),
            ft.Text("TEMPLATE ODOO.CONF", size=20, weight="bold"),
            txt_template,
            ft.Row([combo_ver_template, btn_paste_template]),
        ],
        visible=False,
        scroll="auto",
    )

    def switch_view(to_work):
        workspace_view.visible = to_work
        settings_view.visible = not to_work
        page.update()

    async def quit_app(e):
        import inspect

        try:
            if hasattr(page, "window_destroy"):
                res = page.window_destroy()
                if inspect.isawaitable(res):
                    await res
            elif hasattr(page, "window"):
                if hasattr(page.window, "destroy"):
                    res = page.window.destroy()
                    if inspect.isawaitable(res):
                        await res
                elif hasattr(page.window, "close"):
                    res = page.window.close()
                    if inspect.isawaitable(res):
                        await res
        except Exception as ex:
            print(f"Error quitting app: {ex}")

    page.add(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            "SHAZLER ODOO PRO",
                            size=32,
                            weight="bold",
                            color="#c678dd",
                            expand=True,
                        ),
                        ft.Button(
                            "❌ QUITTER",
                            on_click=quit_app,
                            bgcolor="#ef4444",
                            color="white",
                        ),
                    ]
                ),
                ft.Row(
                    [
                        ft.Button("🚀 TRAVAIL", on_click=lambda _: switch_view(True)),
                        ft.Button("⚙️ RÉGLAGES", on_click=lambda _: switch_view(False)),
                    ]
                ),
                ft.Divider(),
                workspace_view,
                settings_view,
            ],
            expand=True,
        )
    )

    refresh_ui()


if __name__ == "__main__":
    ft.run(main)
