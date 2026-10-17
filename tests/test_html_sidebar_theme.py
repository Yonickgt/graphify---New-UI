"""graph.html carries the graphify sidebar/zones theme; GRAPHIFY_THEME=0 opts out."""
import networkx as nx

from graphify.export import to_html


def _render(tmp_path):
    G = nx.Graph()
    G.add_node("a", label="Alpha", source_file="a.py", file_type="code")
    G.add_node("b", label="Beta", source_file="b.py", file_type="code")
    G.add_edge("a", "b", relation="calls", confidence="EXTRACTED")
    out = tmp_path / "graph.html"
    to_html(G, {0: ["a", "b"]}, str(out))
    return out.read_text(encoding="utf-8")


def test_theme_injected_once(tmp_path):
    html = _render(tmp_path)
    assert html.count('id="gf-theme"') == 1
    assert html.index('id="gf-theme"') < html.rindex("</body>")


def test_theme_opt_out(tmp_path, monkeypatch):
    monkeypatch.setenv("GRAPHIFY_THEME", "0")
    assert 'id="gf-theme"' not in _render(tmp_path)
