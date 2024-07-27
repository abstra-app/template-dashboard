from flask import Blueprint
from pathlib import Path
from json import loads
from nbconvert import HTMLExporter, export
from nbclient import execute
from nbformat import from_dict
from abstra_internals.settings import Settings

def render_notebook(name: str):
    notebook_path = Path(__file__).parent / f'{name}.ipynb'
    if not notebook_path.exists():
        return f"Notebook {name} not found"

    nb_content = notebook_path.read_text()
    nb_dict = loads(nb_content)
    nb_node = from_dict(nb_dict)

    # Setup abstra_internals.settings.Settings.root_path
    nb_node.cells.insert(0, from_dict({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "from abstra_internals.settings import Settings",
            f"\nSettings.set_root_path('{Settings.root_path}')"
        ]
    }))

    # Normalize cell source
    for cell in nb_node.cells:
        if isinstance(cell.source, list):
            cell.source = ''.join(cell.source)

    nb_node = execute(nb_node)

    output, _ = export(HTMLExporter, nb_node, exclude_input=True, exclude_output_prompt=True)
    
    return output



def notebooks_bp():
    bp = Blueprint('notebooks', __name__, url_prefix='/notebooks')
    
    @bp.route('/<notebook_name>')
    def _index(notebook_name):
        return render_notebook(notebook_name)
    
    return bp
